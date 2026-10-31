# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-29 (reference run); 2026-10-31 (scoring of stored responses)
# TIME TAKEN   : ~30 min for 336 calls; scoring ~10 s
# DESCRIPTION  : Experiment E1, ledger task (preregistration/e1_structures_prereg_en.md). The same 48 seeded
#                drafts as S1 go to each evaluation structure: three independent reviews by the main model
#                (REV1-3), one review by a smaller model (REVH), a review with a field checklist (TGT), and
#                independent reproduction + comparison + resolution (REPRO: the model writes the ledger from
#                the documents without the draft, code lists the rows on which the two versions differ, and a
#                second call decides each differing row from the documents with the versions unlabeled).
#                --score-only skips all model calls and scores the responses already in <out>/responses/.
# INPUT FILES  : data/ledgers/drafts/*, data/ledgers/packets/*
# OUTPUT FILES : <out>/responses/*.txt, <out>/calls.jsonl, <scores>/rows.csv
# USAGE        : python src/11_run_e1_ledger.py --out <dir> [--model-main claude-cli:claude-sonnet-5-5]
#                    [--model-small claude-cli:claude-haiku-5-5]
#                python src/11_run_e1_ledger.py --out runs/e1_ledger --score-only --scores <dir>
# ============================================================
import argparse
import csv
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ledger_task as lt  # noqa: E402
from lib import models, paths  # noqa: E402

lock = threading.Lock()

REVIEW = ("An AI system has drafted this month's ledger. Rows marked FLAGGED are ones the AI is less sure "
          "about. Check the draft against the documents and correct it.")
TARGETED = (REVIEW + " Before anything else, go through every row and compare its date and its pay channel "
            "(CASH, MOBILE or BANK) with the source document; then check the account and the amount.")
AUTHOR = ("Build this month's ledger yourself from the documents. Record every transaction exactly once as CSV "
          "with the header doc_ids,date,account,pay,amount,confidence, where confidence is your probability, "
          "from 0 to 100, that the whole row is correct. Return only the CSV.\n")
RESOLVE = ("Two bookkeepers recorded the rows below differently. For each row number, check the documents and "
           "decide the correct values. Return CSV with the header row,action,doc_ids,date,account,pay,amount, "
           "one line per row number below, action EDIT (or DELETE if the row should not exist). Return only the CSV.\n")

# arm -> (model role, kind)
ARMS = {"REV1": ("main", "review"), "REV2": ("main", "review"), "REV3": ("main", "review"),
        "REVH": ("small", "review"), "TGT": ("main", "targeted"), "REPRO": ("main", "author")}


def prompt_for(p, kind):
    if kind == "author":
        return lt.head(p) + AUTHOR + "DOCUMENTS:\n" + p["docs"]
    brief = REVIEW if kind == "review" else TARGETED
    return (lt.head(p) + brief + "\n\n" + lt.EDIT_FORMAT + "Return only the CSV.\n\nDOCUMENTS:\n" + p["docs"]
            + "\n\nDRAFT LEDGER:\n" + lt.draft_table(p["rows"], "N"))


def touched_and_final(p, text):
    """Rows the reviewer changed (edit or delete) and the final ledger, using the content parser."""
    final, unplaced, n_edit = lt.apply_edits_v2(p["rows"], text)
    before = {i: (r["doc_ids"], r["date"], r["account"], r["pay"], float(r["amount"])) for i, r in enumerate(p["rows"], 1)}
    tmp = {i: dict(r) for i, r in enumerate(p["rows"], 1)}
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("```")]
    by_doc = {}
    for i, r in enumerate(p["rows"], 1):
        for d in r["doc_ids"].split("|"):
            by_doc.setdefault(d, i)
    touched = set()
    for parts in csv.reader(lines):
        got = lt.read_line(parts)
        if not got:
            continue
        act, row, vals = got
        if act == "ADD":
            continue
        if row is None or row not in tmp:
            ids = (vals["doc_ids"] if isinstance(vals, dict) else (vals or "")).split("|")
            row = next((by_doc[d] for d in ids if d in by_doc), None)
        if row is None:
            continue
        if act == "DELETE":
            touched.add(row)
        elif (vals["doc_ids"], vals["date"], vals["account"], vals["pay"], float(vals["amount"])) != before[row]:
            touched.add(row)
    return touched, final, unplaced


def key_of(r):
    return (r["date"], r["account"], r["pay"], round(float(r["amount"]), 2))


# ★ CORE LOGIC: the comparison unit in the ledger task is the row. A draft row is in dispute when the
# independent ledger records its first document with different values or a different document grouping.
def diff_rows(p, author_text):
    A, _ = lt.parse_ledger(author_text)
    a_by = {}
    for r in A:
        for d in str(r["doc_ids"]).split("|"):
            a_by[d.strip()] = r
    flagged = []
    for i, r in enumerate(p["rows"], 1):
        a = a_by.get(r["doc_ids"].split("|")[0])
        if a is None or key_of(a) != key_of(r) or set(str(a["doc_ids"]).split("|")) != set(r["doc_ids"].split("|")):
            flagged.append((i, a))
    return flagged


def resolve_prompt(p, flagged):
    lines = ["row,version,doc_ids,date,account,pay,amount"]
    rng = random.Random(p["tag"] + p["fmt"] + "-resolve")
    for i, a in flagged:
        r = p["rows"][i - 1]
        v_draft = f"{r['doc_ids']},{r['date']},{r['account']},{r['pay']},{r['amount']}"
        v_auth = (f"{a['doc_ids']},{a['date']},{a['account']},{a['pay']},{a['amount']:g}" if a else "(not recorded)")
        pair = [v_draft, v_auth]
        rng.shuffle(pair)  # neither version is labeled as the draft
        lines += [f"{i},1,{pair[0]}", f"{i},2,{pair[1]}"]
    return lt.head(p) + RESOLVE + "\nDOCUMENTS:\n" + p["docs"] + "\n\nROWS IN DISPUTE:\n" + "\n".join(lines)


def call(prompt, spec):
    text, meta = models.text_call(prompt, spec)
    return text, float(meta.get("cost_usd") or 0), meta.get("model_used", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model-main", default="claude-cli:claude-sonnet-5-5")
    ap.add_argument("--model-small", default="claude-cli:claude-haiku-5-5")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cap", type=float, default=25.0, help="stop when the client-reported cost passes this (USD)")
    ap.add_argument("--mock", action="store_true", help="pipeline test: reuse stored S1 responses, no calls")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--scores", default=None, help="where to write rows.csv (default: --out)")
    a = ap.parse_args()
    out = Path(a.out)
    P = lt.packets()
    if a.score_only:
        score(P, out, Path(a.scores or out))
        return
    if out.exists() and any(out.iterdir()) and not a.resume:
        sys.exit(f"{out} is not empty")
    (out / "responses").mkdir(parents=True, exist_ok=True)
    spec = {"main": a.model_main, "small": a.model_small}
    spent = [0.0]
    if (out / "calls.jsonl").exists():
        spent[0] = sum(json.loads(line).get("cost", 0) for line in open(out / "calls.jsonl"))
    s1dir = paths.RUN_S1 / "responses"

    def run(p, arm):
        rp = out / "responses" / f"{p['tag']}_{p['fmt']}_{arm}.txt"
        if rp.exists():
            return
        role, kind = ARMS[arm]
        model = spec[role]
        if a.mock:  # S1 stand-ins: arm N for reviews, arm A for the author
            text = (s1dir / f"{p['tag']}_{p['fmt']}_{'A' if kind == 'author' else 'N'}.txt").read_text()
            cost = 0.0
        else:
            with lock:
                if spent[0] > a.cap:
                    raise RuntimeError("cost cap reached")
            text, cost, used = call(prompt_for(p, kind), model)
        rp.write_text(text)
        with lock:
            spent[0] += cost
            with open(out / "calls.jsonl", "a") as f:
                f.write(json.dumps(dict(tag=p["tag"], fmt=p["fmt"], arm=arm, model=models.model_name(model), cost=cost,
                                        finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"))) + "\n")
        if arm == "REPRO":  # second stage: resolve the disputed rows
            flagged = diff_rows(p, text)
            rp2 = out / "responses" / f"{p['tag']}_{p['fmt']}_RESOLVE.txt"
            if not flagged:
                rp2.write_text("row,action,doc_ids,date,account,pay,amount\n")
                return
            if a.mock:
                t2, c2 = "row,action,doc_ids,date,account,pay,amount\n", 0.0
            else:
                t2, c2, _ = call(resolve_prompt(p, flagged), spec["main"])
            rp2.write_text(t2)
            with lock:
                spent[0] += c2
                with open(out / "calls.jsonl", "a") as f:
                    f.write(json.dumps(dict(tag=p["tag"], fmt=p["fmt"], arm="RESOLVE", model=models.model_name(spec["main"]),
                                            cost=c2, n_flagged=len(flagged),
                                            finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"))) + "\n")

    jobs = [(p, arm) for p in P for arm in ARMS]
    random.Random("e1L-order").shuffle(jobs)
    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(run, p, arm) for p, arm in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                fu.result()
            except Exception as e:
                print("FAILED:", repr(e)[:150], flush=True)
            if i % 24 == 0:
                print(f"{i}/{len(jobs)} {time.strftime('%H:%M:%S')}", flush=True)
    score(P, out, Path(a.scores or out))


# ★ CORE LOGIC: one row per (packet, draft row) with, for each structure, whether a seeded error was detected
# (row changed or deleted, or listed as a disagreement) and whether the row's transaction is correct in that
# structure's final ledger.
def score(P, out, scores_dir):
    rows = []
    for p in P:
        by_doc = {d: k for k in p["key"] for d in k["doc_ids"].split("|")}
        res = {}
        for arm in ARMS:
            f = out / "responses" / f"{p['tag']}_{p['fmt']}_{arm}.txt"
            if not f.exists():
                continue
            if arm == "REPRO":
                flagged = {i for i, _ in diff_rows(p, f.read_text())}
                f2 = out / "responses" / f"{p['tag']}_{p['fmt']}_RESOLVE.txt"
                if not f2.exists():
                    continue
                _, final, _ = touched_and_final(p, f2.read_text())
                res[arm] = (flagged, final)
            else:
                t, final, _ = touched_and_final(p, f.read_text())
                res[arm] = (t, final)
        for i, r in enumerate(p["rows"], 1):
            k = by_doc.get(r["doc_ids"].split("|")[0])
            if k is None:
                continue
            draft_ok = lt.txn_correct(k, [dict(x, amount=float(x["amount"])) for x in p["rows"]])
            cls = "seeded" if r["seeded"] else ("correct" if draft_ok else "natural")
            row = dict(tag=p["tag"], fmt=p["fmt"], row=i, cls=cls, kind=r["seeded"],
                       flagged_in_draft=int(int(r["confidence"]) < 90))
            for arm, (t, final) in res.items():
                row[f"det_{arm}"] = int(i in t)
                row[f"ok_{arm}"] = int(lt.txn_correct(k, final))
            rows.append(row)
    cols = sorted({c for r in rows for c in r}, key=lambda c: (c.startswith(("det_", "ok_")), c))
    scores_dir.mkdir(parents=True, exist_ok=True)
    with open(scores_dir / "rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"scored rows {len(rows)}")


if __name__ == "__main__":
    main()
