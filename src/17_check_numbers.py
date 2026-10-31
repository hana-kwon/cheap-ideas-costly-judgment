# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 s
# DESCRIPTION  : Recomputes every number cited in the proposal and appendix that comes from these experiments
#                (config/proposal_numbers.csv lists each number, where it appears, and the expression that
#                computes it from the analysis outputs), formats it as printed, and marks whether it matches.
# INPUT FILES  : config/proposal_numbers.csv and, under <results>: e1/e1_analysis.json, e2e3/e2e3_analysis.json,
#                s1_content/analysis.json, s1_locked/analysis.json, e1_ledger/rows.csv, e1_reports/verdicts.csv,
#                pilot/runs_scored.csv; call logs in <runs>/{e1_ledger,e1_reports,e2e3}/calls.jsonl
# OUTPUT FILES : <results>/proposal_numbers_check.csv
# USAGE        : python src/17_check_numbers.py <results dir> [<runs dir>]
# ============================================================
import csv
import json
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import paths  # noqa: E402


def main(results, runs):
    R, U = Path(results), Path(runs)
    ns = dict(
        E1=json.load(open(R / "e1" / "e1_analysis.json")),
        E23=json.load(open(R / "e2e3" / "e2e3_analysis.json")),
        S1R=json.load(open(R / "s1_content" / "analysis.json")),
        S1L=json.load(open(R / "s1_locked" / "analysis.json")),
        ROWS=pd.read_csv(R / "e1_ledger" / "rows.csv"),
        VERD=pd.read_csv(R / "e1_reports" / "verdicts.csv"),
        PILOT=pd.read_csv(R / "pilot" / "runs_scored.csv"),
        N_CALLS_E1_E23=sum(sum(1 for _ in open(U / d / "calls.jsonl")) for d in ("e1_ledger", "e1_reports", "e2e3")),
        max=max, len=len,
    )
    rows = []
    for spec in csv.DictReader(open(paths.CONFIG / "proposal_numbers.csv")):
        # ★ IMPORTANT: expressions come from the repository's own config file, never from user input.
        val = eval(spec["expr"], {"__builtins__": {}}, ns)
        shown = spec["fmt"].format(float(val))
        if shown == "-0" or shown.startswith("-0.") and float(shown) == 0:
            shown = shown.lstrip("-")
        rows.append(dict(id=spec["id"], where=spec["where"], statement=spec["statement"], stated=spec["stated"],
                         recomputed=shown, raw=repr(float(val)), match=int(shown == spec["stated"]),
                         note=spec.get("note", "")))
    with open(R / "proposal_numbers_check.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if not r["match"]]
    print(f"proposal numbers: {len(rows) - len(bad)} of {len(rows)} match")
    for r in bad:
        print("MISMATCH", r["id"], r["statement"], "stated", r["stated"], "recomputed", r["recomputed"], r["note"])
    # A mismatch explained in the config (note starting with ROUNDING) is reported but does not fail the run.
    return sum(1 for r in bad if not r["note"].startswith("ROUNDING"))


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else paths.RUNS) else 0)
