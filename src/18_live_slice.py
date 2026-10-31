# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1-5 min, depending on the model
# DESCRIPTION  : Optional live check. Sends a small slice of the reference items to a model of the user's choice
#                under the single-review structure of E1, scores the answers with the same code, and sets them
#                next to the stored reference decisions for the same items. Ledger items: the smallest packets
#                first. Report items: one method-flawed report with the right conclusion, one correct report, one
#                wrong-conclusion report, and so on.
# INPUT FILES  : data/ledgers/*, data/reports/*, runs/e1_ledger/rows.csv, runs/e1_reports/verdicts.csv
# OUTPUT FILES : <out>/ledger/*.txt, <out>/reports/<id>/, <out>/live_summary.json, <out>/live_items.csv
# USAGE        : python src/18_live_slice.py --out <empty dir> --model claude-cli:claude-haiku-5-5
#                    [--n-ledger 2] [--n-reports 2]
#                Other models: --model anthropic:<name> | openai:<name> (OPENAI_BASE_URL for local servers)
# ============================================================
import argparse
import csv
import importlib.util
import json
import os
import shutil
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import ledger_task as lt  # noqa: E402
from lib import models, paths  # noqa: E402
from lib.report_prompts import VER_SYSTEM, VER_TASK  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


eL = _load("eL", "11_run_e1_ledger.py")
LEDGER_ORDER = ["KEN_40tx_a_local", "USA_40tx_a_standard", "NGA_40tx_a_local", "IND_40tx_a_standard"]
REPORT_ORDER = ["p01_V2_omit_prior", "p01_V0_correct", "p05_V1_collider", "p03_V3_no_controls"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--n-ledger", type=int, default=2)
    ap.add_argument("--n-reports", type=int, default=2)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    (out / "ledger").mkdir(parents=True)
    (out / "reports").mkdir()
    ref_rows = list(csv.DictReader(open(paths.RUN_E1_LEDGER / "rows.csv")))
    ref_verd = {f"{r['dataset']}_{r['variant']}": r for r in csv.DictReader(open(paths.RUN_E1_REPORTS / "verdicts.csv"))}
    items = []
    P = {f"{p['tag']}_{p['fmt']}": p for p in lt.packets()}
    for pid in LEDGER_ORDER[:a.n_ledger]:
        p = P[pid]
        t0 = time.time()
        text, meta = models.text_call(eL.prompt_for(p, "review"), a.model)
        (out / "ledger" / f"{pid}_REVIEW.txt").write_text(text)
        touched, final, _ = eL.touched_and_final(p, text)
        by_doc = {d: k for k in p["key"] for d in k["doc_ids"].split("|")}
        seeded = [(i, by_doc[r["doc_ids"].split("|")[0]]) for i, r in enumerate(p["rows"], 1) if r["seeded"]]
        passed = sum(1 - int(lt.txn_correct(k, final)) for _, k in seeded)
        ref = [r for r in ref_rows if f"{r['tag']}_{r['fmt']}" == pid and r["cls"] == "seeded"]
        items.append(dict(task="ledger", item=pid, model=a.model, seconds=round(time.time() - t0, 1),
                          planted_errors=len(seeded), detected=sum(i in touched for i, _ in seeded), left_wrong=passed,
                          reference_left_wrong_REV1=sum(1 - int(r["ok_REV1"]) for r in ref),
                          reference_left_wrong_REV2=sum(1 - int(r["ok_REV2"]) for r in ref),
                          reference_left_wrong_REV3=sum(1 - int(r["ok_REV3"]) for r in ref)))
        print(json.dumps(items[-1]), flush=True)
    for rid in REPORT_ORDER[:a.n_reports]:
        b = ref_verd[rid]
        wd = out / "reports" / rid / "work"
        wd.mkdir(parents=True)
        for f in ("data.csv", "codebook.md", "report.md", "final_answer.json", "analysis.py"):
            shutil.copy(paths.REPORT_BANK / rid / f, wd)
        truth = json.load(open(paths.REPORT_TRUTH / f"{b['dataset']}_truth.json"))
        _, cost, _, dt = models.agent_call(str(wd), VER_SYSTEM, VER_TASK.format(question=truth["question"]), a.model,
                                           str(out / "reports" / rid / "transcript.jsonl"))
        v = models.read_json(wd / "verdict.json") or {}
        (wd / "data.csv").unlink()
        items.append(dict(task="report", item=rid, model=a.model, seconds=round(dt, 1), flaw=b["flaw"] or "none",
                          report_conclusion_wrong=int(b["conclusion_wrong"]),
                          decision=str(v.get("decision", "")).strip().lower() or "missing", reason=v.get("reason"),
                          reference_REV1=b["dec_REV1"], reference_REV2=b["dec_REV2"], reference_REV3=b["dec_REV3"]))
        print(json.dumps(items[-1]), flush=True)
    with open(out / "live_items.csv", "w", newline="") as f:
        cols = sorted({c for r in items for c in r})
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(items)
    (out / "live_summary.json").write_text(json.dumps(dict(model=a.model, items=items), indent=1) + "\n")


if __name__ == "__main__":
    main()
