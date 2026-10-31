# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 hour (original), ~10 min (repository version)
# DESCRIPTION  : Ledger task, document side. Synthetic monthly source documents for a small retail shop in
#                Kenya, Nigeria, India or the United States: transactions, the documents that record them
#                (statement lines, mobile-money messages, notebook entries, and supplier receipts that
#                duplicate some purchases), two renderings of the same content (local informal text and a
#                standardized table), the answer key, the scoring rule, and a check that every rendered
#                line lets a reader recover the true transaction. Used by src/03 and the ledger runners.
# INPUT FILES  : none (synthetic data, fixed seeds)
# OUTPUT FILES : none (functions only; src/03_make_ledger_packets.py writes the files)
# ============================================================
import csv
import random
import re
from datetime import date, timedelta

WORKLOADS = (40, 100, 160)
VERSIONS = ("a", "b")
PERIOD = "October 2025"  # stated to participants and to the model; notes without a year belong to it
ACCOUNTS = ["SALES", "PURCHASES", "RENT", "TRANSPORT", "AIRTIME", "WAGES", "UTILITIES", "BANKFEE", "DRAWINGS"]
CATEGORY_WEIGHTS = [("SALES", 55), ("PURCHASES", 18), ("TRANSPORT", 8), ("AIRTIME", 6),
                    ("BANKFEE", 5), ("DRAWINGS", 3), ("WAGES", 3), ("UTILITIES", 1), ("RENT", 1)]
COUNTRY = {
    "KEN": dict(sale=(150, 3500), scale=1.0, vat=0.16),
    "NGA": dict(sale=(1500, 45000), scale=12.0, vat=0.075),
    "IND": dict(sale=(60, 2500), scale=0.6, vat=0.18),
    "USA": dict(sale=(8, 250), scale=0.03, vat=0.0),
}
SUPPLIERS = {
    "KEN": ["MAMA MBOGA STORES", "WHOLESALE HUB EASTLEIGH", "NAIVAS DISTRIBUTORS"],
    "NGA": ["Mama Nkechi Provisions", "Alaba Wholesale Ltd", "Ojota Distributors"],
    "IND": ["Sharma Kirana Wholesale", "Balaji Traders", "Metro Cash and Carry"],
    "USA": ["Sysco Supply", "Costco Business Center", "Restaurant Depot"],
}
PERSONS = {"KEN": ["JOHN KAMAU", "MARY WANJIKU", "PETER OTIENO"], "NGA": ["Chidi Okafor", "Bisi Adeyemi", "Musa Bello"],
           "IND": ["Ramesh Kumar", "Sunita Devi", "Arjun Patel"], "USA": ["Jake M.", "Maria G.", "Tom R."]}
LOCAL_WORDS = {
    "KEN": dict(SALES="mauzo", PURCHASES="stock unga+sukari", RENT="kodi ya duka", TRANSPORT="nauli",
                AIRTIME="bundles", WAGES="mshahara", UTILITIES="stima KPLC", BANKFEE="charges", DRAWINGS="pesa ya nyumbani"),
    "NGA": dict(SALES="sales", PURCHASES="goods from market", RENT="shop rent", TRANSPORT="transport money",
                AIRTIME="recharge card", WAGES="salary for boy", UTILITIES="NEPA light bill", BANKFEE="charges",
                DRAWINGS="money for house"),
    "IND": dict(SALES="bikri", PURCHASES="maal kharida", RENT="dukaan ka kiraya", TRANSPORT="auto kiraya",
                AIRTIME="recharge", WAGES="ladke ki tankhwah", UTILITIES="bijli bill", BANKFEE="charges",
                DRAWINGS="ghar ke liye"),
    "USA": dict(SALES="sales", PURCHASES="restock", RENT="shop rent", TRANSPORT="gas for deliveries",
                AIRTIME="phone bill", WAGES="paid helper", UTILITIES="electric", BANKFEE="fee", DRAWINGS="took out for home"),
}
CHANNEL = {"KEN": dict(MOBILE="M-PESA", BANK="Equity Bank"), "NGA": dict(MOBILE="OPay", BANK="GTBank"),
           "IND": dict(MOBILE="UPI", BANK="HDFC Bank NEFT"), "USA": dict(MOBILE="Venmo", BANK="Chase")}
CASH_FMT = {"KEN": lambda a: f"{a:,}/=", "NGA": lambda a: f"N{a:,}", "IND": lambda a: f"Rs {a:,}/-", "USA": lambda a: f"${a:,}"}
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def short_date(cty, d):
    """Handwritten date as people write it locally: month/day in the US, day/month elsewhere."""
    return f"{d.month}/{d.day}" if cty == "USA" else f"{d.day}/{d.month}"


def make_transactions(cty, n, rng):
    cfg = COUNTRY[cty]
    cats = [c for c, w in CATEGORY_WEIGHTS for _ in range(w)]
    txns = []
    for i in range(n):
        cat = rng.choice(cats)
        if cat == "SALES":
            amt = rng.randint(*cfg["sale"])
        else:
            lo, hi = {"PURCHASES": (2000, 25000), "TRANSPORT": (100, 600), "AIRTIME": (50, 500), "BANKFEE": (10, 60),
                      "DRAWINGS": (1000, 6000), "WAGES": (6000, 12000), "UTILITIES": (1500, 4000),
                      "RENT": (12000, 20000)}[cat]
            amt = max(1, round(rng.randint(lo, hi) * cfg["scale"]))
        pay = "MOBILE" if cat == "BANKFEE" else rng.choices(["CASH", "MOBILE", "BANK"], weights=[40, 45, 15])[0]
        txns.append(dict(txn_id=f"T{i + 1:03d}", date=date(2025, 10, 1) + timedelta(days=rng.randrange(31)),
                         amount=amt, account=cat, pay=pay,
                         party=rng.choice(SUPPLIERS[cty]) if cat == "PURCHASES" else ""))
    txns.sort(key=lambda t: (t["date"], t["txn_id"]))
    # ★ IMPORTANT: a supplier receipt shows party, item cue, date, total and channel. It is only
    # issued when no other transaction shares all of these, so the true link is recoverable.
    visible = {}
    for t in txns:
        visible.setdefault(link_signature(t), []).append(t["txn_id"])
    docs = []
    for t in txns:
        docs.append((f"D{len(docs) + 1:03d}", t, "primary"))
        if t["account"] == "PURCHASES" and t["pay"] != "CASH" and rng.random() < 0.35 \
                and len(visible[link_signature(t)]) == 1:
            docs.append((f"D{len(docs) + 1:03d}", t, "duplicate"))
    return docs


def link_signature(t):
    return (t["party"], t["account"], t["date"], t["amount"], t["pay"])


def render_standard(docs):
    """The 'input-cleaning support' version: one structured row per document."""
    rows = [["doc_id", "date", "description", "counterparty", "amount", "payment_channel", "document_type"]]
    desc = dict(SALES="Customer sale", PURCHASES="Stock purchase", RENT="Shop rent", TRANSPORT="Delivery transport",
                AIRTIME="Phone and data", WAGES="Helper wage", UTILITIES="Electricity bill",
                BANKFEE="Transaction fee", DRAWINGS="Owner withdrawal")
    for doc_id, t, kind in docs:
        rows.append([doc_id, t["date"].isoformat(), desc[t["account"]], t["party"], str(t["amount"]),
                     t["pay"].lower(), "supplier receipt" if kind == "duplicate" else "statement line"])
    return rows


def render_local(cty, docs, rng):
    """Same content, informal presentation. Exact amounts, channel words and dates are always kept."""
    words, ch, cash = LOCAL_WORDS[cty], CHANNEL[cty], CASH_FMT[cty]
    lines = []
    for doc_id, t, kind in docs:
        d, a, w = t["date"], t["amount"], words[t["account"]]
        inflow = t["account"] == "SALES"
        who = t["party"] or rng.choice(PERSONS[cty])
        if kind == "duplicate":
            lines.append(f"[{doc_id}] receipt (handwritten): {t['party'].title()} - {w} - "
                         f"{short_date(cty, d)}/25 - total {cash(a)} paid {ch[t['pay']]}")
        elif t["pay"] == "CASH":
            lines.append(f"[{doc_id}] notebook {short_date(cty, d)}: {w} {cash(a)} cash")
        elif cty == "KEN":
            code = "".join(rng.choice("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789") for _ in range(10))
            verb = f"received from {who}" if inflow else f"paid to {who}."
            src = "M-PESA" if t["pay"] == "MOBILE" else "Equity Bank"
            lines.append(f"[{doc_id}] {src} SMS: {code} Confirmed. Ksh{a:,}.00 {verb} on {d.day}/{d.month}/25 -- owner note: {w}")
        elif cty == "NGA":
            if t["pay"] == "MOBILE":
                lines.append(f"[{doc_id}] OPay: {'You received' if inflow else 'You sent'} N{a:,}.00 "
                             f"{'from' if inflow else 'to'} {who} {d.day:02d}/{d.month:02d}/2025 -- note: {w}")
            else:
                lines.append(f"[{doc_id}] GTBank alert: Acct:***{rng.randint(1000, 9999)} Amt:NGN{a:,}.00 "
                             f"{'CR' if inflow else 'DR'} Desc:TRF/{w} Date:{d.day:02d}-{MONTHS[d.month - 1]}-25")
        elif cty == "IND":
            if t["pay"] == "MOBILE":
                lines.append(f"[{doc_id}] UPI SMS: Rs.{a:,}.00 {'credited' if inflow else 'debited'} "
                             f"{'from' if inflow else 'to'} {who} on {d.day:02d}-{d.month:02d}-25 note: {w}")
            else:
                lines.append(f"[{doc_id}] HDFC Bank NEFT: INR {a:,}.00 {'credited' if inflow else 'debited'} "
                             f"on {d.day:02d}-{d.month:02d}-25 ref {rng.randint(10**8, 10**9)} remark: {w}")
        else:  # USA informal
            if t["pay"] == "MOBILE":
                lines.append(f"[{doc_id}] Venmo: {'You received' if inflow else 'You paid'} ${a:,}.00 "
                             f"{'from' if inflow else 'to'} {who} ({d.month}/{d.day}) note: {w}")
            else:
                lines.append(f"[{doc_id}] Chase alert: {'deposit' if inflow else 'payment'} of ${a:,}.00 "
                             f"on {d.month}/{d.day}/25, memo: {w}")
    return lines


def answer_key(docs):
    ids = {}
    for doc_id, t, _ in docs:
        ids.setdefault(t["txn_id"], []).append(doc_id)
    return [dict(txn_id=t["txn_id"], doc_ids="|".join(ids[t["txn_id"]]), date=t["date"].isoformat(),
                 amount=t["amount"], account=t["account"], pay=t["pay"])
            for doc_id, t, kind in docs if kind == "primary"]


# ★ KEY FUNCTION: v3 scoring. Full credit needs the exact document set, account, channel, date and
# amount to the cent. Duplicate rows, merged rows and malformed response lines all count as wrong rows:
# the primary ledger accuracy is full / (transactions in key + extra rows + malformed lines).
def score(key, submission, malformed=0):
    by_doc = {d: k for k in key for d in k["doc_ids"].split("|")}
    credited, extra, merged = set(), 0, 0
    full = acct_ok = amt_ok = link_ok = date_ok = 0
    for s in submission:
        ids = {x.strip() for x in str(s.get("doc_ids", "")).split("|") if x.strip()}
        txns = {by_doc[x]["txn_id"] for x in ids if x in by_doc}
        if len(txns) != 1:
            extra += 1
            merged += len(txns) > 1
            continue
        k = next(by_doc[x] for x in ids if x in by_doc)
        if k["txn_id"] in credited:
            extra += 1
            continue
        credited.add(k["txn_id"])
        link = ids == set(k["doc_ids"].split("|"))
        a = s.get("account") == k["account"] and s.get("pay") == k["pay"]
        try:
            m = abs(float(s.get("amount")) - float(k["amount"])) < 0.005
        except (TypeError, ValueError):
            m = False
        dt = str(s.get("date", "")).strip() == k["date"]
        link_ok += link
        acct_ok += a
        amt_ok += m
        date_ok += dt
        full += link and a and m and dt
    n = len(key)
    return dict(n_key=n, recall=len(credited) / n, extra_rows=extra, merged_rows=merged, malformed_lines=malformed,
                link_accuracy=link_ok / n, account_accuracy=acct_ok / n, amount_accuracy=amt_ok / n,
                date_accuracy=date_ok / n, ledger_accuracy=full / (n + extra + malformed))


DATE_PATTERNS = [  # (regex, group order) tried in turn on the local line
    (re.compile(r"Date:(\d{2})-([A-Z]{3})-25\b"), "d-mon"),
    (re.compile(r"\b(\d{2})/(\d{2})/2025\b"), "dm"),
    (re.compile(r"\bon (\d{2})-(\d{2})-25\b"), "dm"),
    (re.compile(r"\((\d{1,2})/(\d{1,2})\)"), "md"),
    (re.compile(r"\b(\d{1,2})/(\d{1,2})/25\b"), "local"),
    (re.compile(r"notebook (\d{1,2})/(\d{1,2}):"), "local"),
]


def visible_date(cty, line):
    """Read the date a person would read from the line, assuming the stated period's year."""
    for rx, order in DATE_PATTERNS:
        m = rx.search(line)
        if not m:
            continue
        a, b = m.groups()
        try:
            if order == "d-mon":
                return date(2025, MONTHS.index(b) + 1, int(a))
            if order == "local":
                order = "md" if cty == "USA" else "dm"
            day, month = (int(a), int(b)) if order == "dm" else (int(b), int(a))
            return date(2025, month, day)
        except ValueError:
            return None
    return None


# ★ KEY FUNCTION: recoverability check. Compares the rendered lines with the full document list,
# not a zip of whatever was passed, and reports every failure type separately.
def parity_check(cty, docs, lines):
    f = dict(count=0, id=0, amount=0, channel=0, cue=0, date=0, ambiguous_link=0)
    if len(lines) != len(docs):
        f["count"] = abs(len(lines) - len(docs)) or 1
    seen = [re.match(r"^\[(D\d+)\] ", ln) for ln in lines]
    seen = [m.group(1) if m else None for m in seen]
    if seen != [d for d, _, _ in docs[:len(seen)]] or len(set(seen)) != len(seen):
        f["id"] += 1
    primaries = [t for _, t, kind in docs if kind == "primary"]
    for (doc_id, t, kind), line in zip(docs, lines):
        # Whole-number match outside the date: "1,200" must not pass inside "11,200", and an amount
        # of 25 must not pass on the "25" of a date such as 01-10-25.
        undated = line
        for rx, _ in DATE_PATTERNS:
            undated = rx.sub(" ", undated)
        f["amount"] += not re.search(r"(?<![\d,])" + re.escape(f"{t['amount']:,}") + r"(?!,?\d)", undated)
        f["channel"] += ("cash" not in line) if t["pay"] == "CASH" else (CHANNEL[cty][t["pay"]] not in line)
        f["cue"] += LOCAL_WORDS[cty][t["account"]] not in line
        f["date"] += visible_date(cty, line) != t["date"]
        if kind == "duplicate":
            f["ambiguous_link"] += sum(link_signature(p) == link_signature(t) for p in primaries) != 1
    return f


def parity_failures(f):
    return sum(f.values())
