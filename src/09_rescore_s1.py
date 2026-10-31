# ============================================================
# START DATE   : 2026-10-28
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~5 s
# DESCRIPTION  : Rescores the S1 responses with the content-based edit parser. This rescoring was decided after
#                the S1 results were seen (recorded in the S1 plan's change log): the parser fixed in the plan
#                read fields by position and silently dropped edits sent without an action column, without a row
#                number, or with the action before the row and no header. Responses and scoring rules are
#                otherwise unchanged. E1, E2 and E3 used the content-based parser from the start.
# INPUT FILES  : <run>/responses/*.txt, data/ledgers/drafts/*, data/ledgers/packets/*
# OUTPUT FILES : <out>/packet_scores.csv, <out>/error_scores.csv
# USAGE        : python src/09_rescore_s1.py --run runs/s1 --out <empty dir>
# ============================================================
import argparse
import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ledger_task as lt  # noqa: E402
from lib import paths  # noqa: E402

_spec = importlib.util.spec_from_file_location("run_s1", os.path.join(os.path.dirname(os.path.abspath(__file__)), "08_run_s1.py"))
run_s1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run_s1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=str(paths.RUN_S1))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    run_s1.write_scores(lt.packets(), Path(a.run) / "responses", out, "content")


if __name__ == "__main__":
    main()
