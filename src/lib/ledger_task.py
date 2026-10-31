# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~3 hours (original modules), ~30 min (merged repository version)
# DESCRIPTION  : Ledger task, evaluation side. Everything the ledger experiments share:
#                  - the drafting prompt and the strict ledger parser (used to read AI drafts and authored ledgers);
#                  - seeding: one plausible error in 8 percent of draft rows, with review flags fixed by design;
#                  - packets(): the 48 seeded drafts with their documents and answer keys;
#                  - prompts of the accountability experiment (S1) and the edit-list format;
#                  - two edit parsers: the parser fixed in the S1 plan (reads fields by position) and the
#                    content-based parser (recognizes each field by its content), used from E1 on;
#                  - transaction scoring against the answer key.
#                The functions are unchanged from the code fixed in the preregistrations; only file locations are
#                now arguments, and modules that were separate files are merged here.
# INPUT FILES  : data/ledgers/drafts/{TAG}_{FMT}_r0.csv (AI drafts), data/ledgers/packets/* (documents, keys)
# OUTPUT FILES : none (functions only)
# ============================================================
import csv
import io
import math
import random
import re
from datetime import date, timedelta
from pathlib import Path

from . import ledger_packets as pk
from . import paths

# ---------------------------------------------------------------------------------------------------------
# Drafting prompt and strict ledger parser
# ---------------------------------------------------------------------------------------------------------
HEADER = ["doc_ids", "date", "account", "pay", "amount", "confidence"]
DRAFT_PROMPT = (
    "You are the bookkeeper for a small retail shop in {country}. All documents are from {period}. "
    "Each document below has an ID in brackets. "
    "Record every transaction exactly once as CSV with the header doc_ids,date,account,pay,amount,confidence. "
    "date is YYYY-MM-DD. amount is a plain number without currency or thousands separators. "
    "account must be one of: {accounts}. pay must be one of: CASH, MOBILE, BANK. "
    "If two documents describe the same transaction, list both IDs joined by | in one row. "
    "confidence is your probability, from 0 to 100, that the whole row is correct. "
    "Return only the CSV.\n\nDOCUMENTS:\n{documents}"
)
AMOUNT_RE = re.compile(r"^-?(\d+|\d{1,3}(,\d{3})+)(\.\d+)?$")


def parse_ledger(text):
    """Strict parser with a sixth field, confidence. A non-numeric confidence keeps the row for scoring but
    leaves its confidence missing."""
    rows, bad = [], 0
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith("```")]
    for parts in csv.reader(io.StringIO("\n".join(lines))):
        parts = [x.strip() for x in parts]
        if [p.lower() for p in parts] == HEADER:
            continue
        if len(parts) != 6:
            bad += 1
            continue
        raw = re.sub(r"^(\$|ksh|ngn|n|inr|rs\.?)\s*", "", parts[4], flags=re.I)
        if not AMOUNT_RE.match(raw) or not math.isfinite(float(raw.replace(",", ""))):
            bad += 1
            continue
        try:
            conf = float(parts[5].rstrip("%"))
            conf = conf if math.isfinite(conf) and 0 <= conf <= 100 else None
        except ValueError:
            conf = None
        rows.append(dict(doc_ids=parts[0], date=parts[1], account=parts[2].upper(), pay=parts[3].upper(),
                         amount=float(raw.replace(",", "")), confidence=conf))
    return rows, bad


def load_draft(path):
    rows, bad = parse_ledger(Path(path).read_text())
    if bad:
        print(f"warning: {bad} malformed draft lines were dropped")
    return [dict(r, amount=f"{r['amount']:g}") for r in rows]


# ---------------------------------------------------------------------------------------------------------
# Seeding errors into the AI drafts
# ---------------------------------------------------------------------------------------------------------
THRESHOLD = 90
ERROR_RATE = 0.08
OWNER = {"KEN": "Grace Achieng", "NGA": "Mrs. Ngozi Okafor", "IND": "Mr. Rakesh Sharma", "USA": "Linda Park"}
# Plausible account confusions a bookkeeper or a model could make.
CONFUSE = {"SALES": "DRAWINGS", "PURCHASES": "DRAWINGS", "DRAWINGS": "WAGES", "WAGES": "DRAWINGS",
           "TRANSPORT": "PURCHASES", "AIRTIME": "UTILITIES", "UTILITIES": "AIRTIME", "BANKFEE": "AIRTIME", "RENT": "UTILITIES"}
KINDS = ["account", "amount", "date", "channel", "split_duplicate"]


def swap_digits(a, rng):
    s = str(int(a))
    pairs = [i for i in range(len(s) - 1) if s[i] != s[i + 1]]
    if not pairs:
        return int(s + "0")
    i = rng.choice(pairs)
    return int(s[:i] + s[i + 1] + s[i] + s[i + 2:])


# ★ CORE LOGIC: seed one plausible error into a fixed share of rows of the real AI draft, then fix the review
# flags by design: half of the seeded errors plus an equal number of correct rows are flagged (confidence
# 55-85) and every other row gets 91-99, so an unflagged error looks as confident as a correct row.
# Note: the "split_duplicate" kind needs a linked row; the draw never picked one, so those draws became
# account errors (reported in the appendix).
def seed(draft, tag, rate=ERROR_RATE):
    rng = random.Random(tag + "-seed")
    rows = [dict(r) for r in draft]
    n_err = max(1, round(rate * len(rows)))
    linked = [i for i, r in enumerate(rows) if "|" in r["doc_ids"]]
    picks = rng.sample(range(len(rows)), n_err)
    log, out_rows = [], []
    kinds = {}
    for j, i in enumerate(picks):
        kind = KINDS[j % len(KINDS)]
        if kind == "split_duplicate" and i not in linked:
            kind = "account"
        kinds[i] = kind
    for i, r in enumerate(rows):
        if i not in kinds:
            out_rows.append(dict(r, seeded=""))
            continue
        k, before = kinds[i], dict(r)
        if k == "account":
            r["account"] = CONFUSE[r["account"]]
        elif k == "amount":
            r["amount"] = str(swap_digits(float(r["amount"]), rng))
        elif k == "date":
            d = date.fromisoformat(r["date"])
            d2 = d + timedelta(days=1) if d.day < 31 else d - timedelta(days=1)
            r["date"] = d2.isoformat()
        elif k == "channel":
            r["pay"] = {"MOBILE": "BANK", "BANK": "MOBILE", "CASH": "MOBILE"}[r["pay"]]
        if k == "split_duplicate":  # the receipt is booked again as its own row: an extra, wrong row
            a, b = r["doc_ids"].split("|", 1)
            out_rows.append(dict(r, doc_ids=a, seeded=k))
            out_rows.append(dict(r, doc_ids=b, seeded=k))
        else:
            out_rows.append(dict(r, seeded=k))
        log.append(dict(doc_ids=before["doc_ids"], kind=k, before={f: before[f] for f in ("date", "account", "pay", "amount")},
                        after={f: r[f] for f in ("date", "account", "pay", "amount")}))
    err_idx = [i for i, r in enumerate(out_rows) if r["seeded"]]
    ok_idx = [i for i, r in enumerate(out_rows) if not r["seeded"]]
    flag_err = set(rng.sample(err_idx, math.ceil(len(err_idx) / 2)))
    flag_ok = set(rng.sample(ok_idx, min(len(ok_idx), len(flag_err))))
    for i, r in enumerate(out_rows):
        r["confidence"] = rng.randint(55, 85) if i in flag_err | flag_ok else rng.randint(91, 99)
    meta = dict(tag=tag, rate=rate, rows_in_draft=len(out_rows), seeded_rows=len(err_idx), seeded_errors=log,
                flagged_error_rows=len(flag_err), flagged_correct_rows=len(flag_ok), threshold=THRESHOLD,
                note="flags fixed by design, not by the model's confidence")
    return out_rows, meta


# ---------------------------------------------------------------------------------------------------------
# Packets and prompts
# ---------------------------------------------------------------------------------------------------------
COUNTRY = {"KEN": "Kenya", "NGA": "Nigeria", "IND": "India", "USA": "the United States"}

COMMON = ("You are the bookkeeper for a small retail shop in {country}. All documents are from {period}. "
          "Each document below has an ID in brackets. A correct ledger records every transaction exactly once, "
          "with date YYYY-MM-DD, account one of: {accounts}, pay one of: CASH, MOBILE, BANK, and amount as a plain "
          "number. If two documents describe the same transaction, they belong in one row with both IDs joined by |.\n\n")

EDIT_FORMAT = ("Return your changes only, as CSV with the header row,action,doc_ids,date,account,pay,amount. "
               "action is EDIT (replace draft row number `row` with the values given), DELETE (remove draft row "
               "`row`; leave the other fields empty) or ADD (a new row; leave `row` empty). Rows you do not list "
               "stay as drafted. If you change nothing, return only the header.\n")


def packets(drafts_dir=None, packets_dir=None):
    """The 48 seeded drafts (24 document sets x 2 formats) with documents and answer keys."""
    drafts_dir = Path(drafts_dir or paths.LEDGER_DRAFTS)
    packets_dir = Path(packets_dir or paths.LEDGER_PACKETS)
    out = []
    for f in sorted(drafts_dir.glob("*_r0.csv")):
        tag, fmt = re.match(r"(.+)_(local|standard)_r0\.csv$", f.name).groups()
        draft = load_draft(f)
        rows, meta = seed(draft, f"{tag}_{fmt}")
        with open(packets_dir / f"{tag}_answer_key.csv") as fh:
            key = list(csv.DictReader(fh))
        docs = (packets_dir / (f"{tag}_local.txt" if fmt == "local" else f"{tag}_standard.csv")).read_text()
        out.append(dict(tag=tag, fmt=fmt, cty=tag.split("_")[0], rows=rows, meta=meta, key=key, docs=docs,
                        draft_file=f))
    return out


def head(p):
    return COMMON.format(country=COUNTRY[p["cty"]], period=pk.PERIOD, accounts=", ".join(pk.ACCOUNTS))


def draft_table(rows, arm):
    lines = ["row,doc_ids,date,account,pay,amount,status"]
    for i, r in enumerate(rows, 1):
        low = int(r["confidence"]) < THRESHOLD
        st = ("OPEN" if low else "CONFIRMED") if arm == "D" else ("FLAGGED" if low else "")
        lines.append(f"{i},{r['doc_ids']},{r['date']},{r['account']},{r['pay']},{r['amount']},{st}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------------------------------------
# Edit parsers
# ---------------------------------------------------------------------------------------------------------
def apply_edits_locked(rows, text):
    """The parser fixed in the S1 plan (with its one pre-scoring fix): reads fields by position, or by header
    names when a header is present. Malformed or out-of-range edits are counted and ignored, never guessed."""
    final = {i: dict(r) for i, r in enumerate(rows, 1)}
    added, bad, n_edit = [], 0, 0
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("```")]
    cols = ["row", "action", "doc_ids", "date", "account", "pay", "amount"]
    order = list(range(7))
    for parts in csv.reader(lines):
        parts = [x.strip() for x in parts]
        # Fix recorded before any scoring: some replies reorder the header columns, so map fields by header
        # names when a header is present instead of assuming the requested order.
        if parts and {p.lower() for p in parts} == set(cols):
            order = [[p.lower() for p in parts].index(c) for c in cols]
            continue
        if not parts:
            continue
        parts += [""] * (7 - len(parts))
        parts = [parts[j] if j < len(parts) else "" for j in order]
        if len(parts) < 2:
            bad += 1
            continue
        act = parts[1].upper()
        parts += [""] * (7 - len(parts))
        try:
            idx = int(parts[0]) if parts[0] else None
        except ValueError:
            bad += 1
            continue
        if act == "DELETE" and idx in final:
            final.pop(idx)
            n_edit += 1
        elif act in ("EDIT", "ADD"):
            raw = re.sub(r"[^\d.\-]", "", parts[6])
            try:
                amt = float(raw)
            except ValueError:
                bad += 1
                continue
            new = dict(doc_ids=parts[2], date=parts[3], account=parts[4].upper(), pay=parts[5].upper(), amount=amt)
            if act == "EDIT" and idx in final:
                final[idx] = dict(final[idx], **new)
                final[idx]["edited"] = True
                n_edit += 1
            elif act == "ADD":
                added.append(dict(new, edited=True))
                n_edit += 1
            else:
                bad += 1
        else:
            bad += 1
    out = [dict(r, amount=float(r["amount"])) for r in final.values()] + added
    return out, bad, n_edit


DOC = re.compile(r"^D\d{3}(\|D\d{3})*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTS = {"EDIT", "DELETE", "ADD"}


# ★ KEY FUNCTION: content-based parser. Reads one edit line by content and returns (action, row or None, values
# or None), or None for a line that is not an edit (header, prose). The row number is the integer before the
# document IDs; the amount is the number after the pay channel, so the two integers cannot be confused.
def read_line(parts):
    parts = [p.strip().strip("*`") for p in parts]
    up = [p.upper() for p in parts]
    act = next((u for u in up if u in ACTS), None)
    di = next((i for i, p in enumerate(parts) if DOC.match(p)), None)
    row = next((int(p) for i, p in enumerate(parts) if p.isdigit() and (di is None or i < di)), None)
    if act == "DELETE":
        if row is None and di is None:
            return None
        return "DELETE", row, (parts[di] if di is not None else None)
    if di is None:
        return None
    rest = parts[di + 1:]
    dt = next((p for p in rest if DATE.match(p)), None)
    acct = next((p.upper() for p in rest if p.upper() in pk.ACCOUNTS), None)
    pi = next((i for i, p in enumerate(rest) if p.upper() in ("CASH", "MOBILE", "BANK")), None)
    if dt is None or acct is None or pi is None:
        return None
    amt = next((p for p in rest[pi + 1:] if re.sub(r"[^\d.]", "", p)), None)
    if amt is None:
        return None
    vals = dict(doc_ids=parts[di], date=dt, account=acct, pay=rest[pi].upper(),
                amount=float(re.sub(r"[^\d.\-]", "", amt)))
    return (act or "EDIT"), row, vals


def apply_edits_v2(rows, text):
    final = {i: dict(r) for i, r in enumerate(rows, 1)}
    by_doc = {}
    for i, r in enumerate(rows, 1):
        for d in r["doc_ids"].split("|"):
            by_doc.setdefault(d, i)
    added, n_edit, unplaced = [], 0, 0
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("```")]
    for parts in csv.reader(lines):
        got = read_line(parts)
        if got is None:
            continue
        act, row, vals = got
        if act == "ADD":
            added.append(dict(vals, edited=True))
            n_edit += 1
            continue
        if row is None or row not in final:
            # no usable row number: place the edit on the draft row that holds its first document ID
            ids = (vals["doc_ids"] if isinstance(vals, dict) else (vals or "")).split("|")
            row = next((by_doc[d] for d in ids if d in by_doc and by_doc[d] in final), None)
            if row is None and act != "ADD":
                unplaced += 1
                continue
        if act == "DELETE":
            final.pop(row, None)
        else:
            final[row] = dict(final[row], **vals, edited=True)
        n_edit += 1
    return [dict(r, amount=float(r["amount"])) for r in final.values()] + added, unplaced, n_edit


# ---------------------------------------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------------------------------------
def txn_correct(k, rows):
    """A transaction is correct when exactly one final row touches its documents and that row is fully right."""
    ids = set(k["doc_ids"].split("|"))
    hits = [r for r in rows if ids & {x.strip() for x in str(r["doc_ids"]).split("|")}]
    if len(hits) != 1:
        return False
    s = hits[0]
    return ({x.strip() for x in str(s["doc_ids"]).split("|")} == ids and s["account"] == k["account"]
            and s["pay"] == k["pay"] and abs(float(s["amount"]) - float(k["amount"])) < 0.005 and s["date"] == k["date"])
