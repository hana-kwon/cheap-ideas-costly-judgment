# ============================================================
# START DATE   : 2026-10-28
# CODE RUN DATE: 2026-10-28 (reference run); 2026-10-31 (scoring of stored responses)
# TIME TAKEN   : ~20 min for 240 calls; scoring ~5 s
# DESCRIPTION  : Accountability experiment S1 (preregistration/s1_accountability_prereg_en.md). Each of the 48
#                seeded drafts is checked by the same model under five arrangements (A, N, B, C, D; see
#                src/lib/s1_accountability.py). Scores every stored response with the parser fixed in the plan
#                (reads fields by position); src/09 rescores with the content-based parser.
#                --score-only skips all model calls and scores the responses already in <out>/responses/.
# INPUT FILES  : data/ledgers/drafts/*, data/ledgers/packets/*
# OUTPUT FILES : <out>/seeded/*, <out>/responses/*, <out>/calls.jsonl, <scores>/packet_scores.csv,
#                <scores>/error_scores.csv
# USAGE        : python src/08_run_s1.py --out <dir> --model claude-cli:claude-sonnet-5-5
#                python src/08_run_s1.py --out runs/s1 --score-only --scores <dir>
# ============================================================
import argparse
import csv
import hashlib
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
from lib import models  # noqa: E402
from lib import s1_accountability as s1  # noqa: E402

lock = threading.Lock()


def write_scores(P, resp_dir, scores_dir, parser):
    pk_rows, err_rows = [], []
    for p in P:
        for arm in s1.ARMS:
            rp = Path(resp_dir) / f"{p['tag']}_{p['fmt']}_{arm}.txt"
            if not rp.exists():
                continue
            s, per = s1.score(p, arm, rp.read_text(), parser=parser)
            pk_rows.append(s)
            err_rows += per
    Path(scores_dir).mkdir(parents=True, exist_ok=True)
    for name, rows in (("packet_scores.csv", pk_rows), ("error_scores.csv", err_rows)):
        if rows:
            with open(Path(scores_dir) / name, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(rows)
    print(f"scored {len(pk_rows)} responses ({parser} parser); missing {len(P) * len(s1.ARMS) - len(pk_rows)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="claude-cli:claude-sonnet-5-5", help="or mock:any for a pipeline test")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--score-only", action="store_true")
    ap.add_argument("--scores", default=None, help="where to write scores (default: --out)")
    a = ap.parse_args()
    out = Path(a.out)
    P = lt.packets()
    if a.score_only:
        write_scores(P, out / "responses", a.scores or out, "locked")
        return
    if out.exists() and any(out.iterdir()) and not a.resume:
        sys.exit(f"{out} is not empty; choose a new folder or pass --resume.")
    (out / "responses").mkdir(parents=True, exist_ok=True)
    (out / "seeded").mkdir(exist_ok=True)
    for p in P:
        with open(out / "seeded" / f"{p['tag']}_{p['fmt']}_seeded.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["doc_ids", "date", "account", "pay", "amount", "confidence", "seeded"])
            w.writerows([[r["doc_ids"], r["date"], r["account"], r["pay"], r["amount"], r["confidence"], r["seeded"]]
                         for r in p["rows"]])
    jobs = [(p, arm) for p in P for arm in s1.ARMS]
    random.Random("s1-order").shuffle(jobs)  # arms interleaved in time, so a slow hour does not hit one arm
    if a.limit:
        jobs = jobs[:a.limit]

    def run(job):
        p, arm = job
        rpath = out / "responses" / f"{p['tag']}_{p['fmt']}_{arm}.txt"
        if rpath.exists():
            return "skipped"
        prompt = s1.prompt_for(p, arm)
        t0 = time.time()
        if models.parse_model(a.model)[0] == "mock":
            text, meta = s1.mock_checker(p, arm, random.Random(f"{p['tag']}-{p['fmt']}-{arm}"))
        else:
            text, meta = models.text_call(prompt, a.model)
        tmp = rpath.with_suffix(".part")
        tmp.write_text(text)
        tmp.rename(rpath)
        with lock, open(out / "calls.jsonl", "a") as f:
            f.write(json.dumps(dict(tag=p["tag"], fmt=p["fmt"], arm=arm, seconds=round(time.time() - t0, 1),
                                    finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                    prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), **meta)) + "\n")
        return "done"

    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(run, j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                fu.result()
            except Exception as e:  # a failed call stays missing and is reported, never filled in
                print("FAILED:", repr(e)[:200], flush=True)
            if i % 20 == 0:
                print(f"{i}/{len(jobs)} {time.strftime('%H:%M:%S')}", flush=True)
    write_scores(P, out / "responses", a.scores or out, "locked")


if __name__ == "__main__":
    main()
