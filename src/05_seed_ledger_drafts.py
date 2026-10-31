# ============================================================
# START DATE   : 2026-10-28
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 s
# DESCRIPTION  : Writes the 48 seeded drafts that every ledger structure received: the AI draft with one
#                planted error in 8 percent of rows and review flags fixed by design (seed tag = packet tag and
#                format). The experiments rebuild these in memory with the same function; this script writes
#                them out so they can be inspected and compared with data/ledgers/seeded/.
# INPUT FILES  : data/ledgers/drafts/*_r0.csv, data/ledgers/packets/*
# OUTPUT FILES : <out>/{TAG}_{FMT}_seeded.csv, <out>/seed_logs.json
# USAGE        : python src/05_seed_ledger_drafts.py --out <empty dir>
# ============================================================
import argparse
import csv
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ledger_task as lt  # noqa: E402
from lib import paths  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--drafts", default=str(paths.LEDGER_DRAFTS))
    ap.add_argument("--packets", default=str(paths.LEDGER_PACKETS))
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    out.mkdir(parents=True, exist_ok=True)
    P = lt.packets(a.drafts, a.packets)
    logs = {}
    for p in P:
        with open(out / f"{p['tag']}_{p['fmt']}_seeded.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["doc_ids", "date", "account", "pay", "amount", "confidence", "seeded"])
            w.writerows([[r["doc_ids"], r["date"], r["account"], r["pay"], r["amount"], r["confidence"], r["seeded"]]
                         for r in p["rows"]])
        logs[f"{p['tag']}_{p['fmt']}"] = p["meta"]
    (out / "seed_logs.json").write_text(json.dumps(logs, indent=1) + "\n")
    n_rows = sum(len(p["rows"]) for p in P)
    n_seed = sum(p["meta"]["seeded_rows"] for p in P)
    print(f"packets {len(P)} | draft rows {n_rows} | seeded rows {n_seed}")


if __name__ == "__main__":
    main()
