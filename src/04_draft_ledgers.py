# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-25 (reference drafts); repository version not rerun
# TIME TAKEN   : ~15 min for 48 calls
# DESCRIPTION  : Model step. Asks a model to write the ledger for each of the 48 packets (24 document sets x
#                local or standardized documents) with a per-row confidence. These AI drafts are the starting
#                point of the ledger task: src/05 seeds errors into them. The reference drafts in
#                data/ledgers/drafts/ came from claude-sonnet-5-5; their call records are in
#                data/ledgers/drafts/drafting_calls.jsonl.
# INPUT FILES  : data/ledgers/packets/{TAG}_{local.txt, standard.csv}
# OUTPUT FILES : <out>/{TAG}_{FMT}_r0.csv, <out>/calls.jsonl
# USAGE        : python src/04_draft_ledgers.py --out <empty dir> --model claude-cli:claude-sonnet-5-5
# ============================================================
import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ledger_packets as pk  # noqa: E402
from lib import models, paths  # noqa: E402
from lib.ledger_task import DRAFT_PROMPT  # noqa: E402

COUNTRY_NAME = {"KEN": "KEN", "NGA": "NGA", "IND": "IND", "USA": "USA"}  # the reference prompt used the code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="claude-cli:claude-sonnet-5-5")
    ap.add_argument("--packets", default=str(paths.LEDGER_PACKETS))
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(f"{c}_{n}tx_{v}", fmt) for c in pk.COUNTRY for n in pk.WORKLOADS for v in pk.VERSIONS
            for fmt in ("standard", "local")]
    if a.limit:
        jobs = jobs[:a.limit]
    lock = threading.Lock()

    def run(job):
        tag, fmt = job
        docs = (Path(a.packets) / (f"{tag}_local.txt" if fmt == "local" else f"{tag}_standard.csv")).read_text()
        # ★ IMPORTANT: the reference drafts passed the three-letter country code as {country}.
        prompt = DRAFT_PROMPT.format(country=COUNTRY_NAME[tag[:3]], period=pk.PERIOD,
                                     accounts=", ".join(pk.ACCOUNTS), documents=docs)
        t0 = time.time()
        text, meta = models.text_call(prompt, a.model)
        (out / f"{tag}_{fmt}_r0.csv").write_text(text)
        with lock, open(out / "calls.jsonl", "a") as f:
            f.write(json.dumps(dict(tag=tag, fmt=fmt, repeat=0, seconds=round(time.time() - t0, 1),
                                    prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                                    model=models.model_name(a.model), **meta)) + "\n")

    with ThreadPoolExecutor(a.workers) as ex:
        for fu in as_completed([ex.submit(run, j) for j in jobs]):
            try:
                fu.result()
            except Exception as e:  # a failed call stays missing and is reported, never filled in
                print("FAILED:", repr(e)[:200], flush=True)
    print("drafts written:", len(list(out.glob("*_r0.csv"))))


if __name__ == "__main__":
    main()
