# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-29 (reference run); 2026-10-31 (collection of stored verdicts)
# TIME TAKEN   : ~1 hour for 168 agent sessions; collection ~1 s
# DESCRIPTION  : Experiment E1, report task (preregistration/e1_structures_prereg_en.md). The 30 bank reports
#                (6 correct, 24 flawed) go to: three independent reviews by the main model (REV1-3), one review
#                by a smaller model (REVH), a review with a checklist (TGT), a fixed rule list without a model
#                (CHK), and independent reanalysis without the report (REPRO1-3 per dataset; a report is approved
#                when its conclusion equals the reanalysis conclusion). Reviewers may run Python in a folder that
#                holds only the data, codebook, report, final answer and analysis script.
#                --collect-only skips all model calls and tabulates the verdicts already in <out>/runs/.
# INPUT FILES  : data/reports/bank/*, data/reports/datasets/*, data/reports/truth/*_truth.json
# OUTPUT FILES : <out>/runs/<id>/ (transcript.jsonl, work/, done.json), <out>/calls.jsonl, <scores>/verdicts.csv
# USAGE        : python src/12_run_e1_reports.py --out <dir> [--model-main ...] [--model-small ...]
#                python src/12_run_e1_reports.py --out runs/e1_reports --collect-only --scores <dir>
# ============================================================
import argparse
import csv
import json
import os
import random
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import models, paths  # noqa: E402
from lib.report_data import STORIES  # noqa: E402
from lib.report_prompts import GEN_SYSTEM, GEN_TASK, ORG_LINE, TGT_LINE, VER_SYSTEM, VER_TASK  # noqa: E402

REVIEW_ARMS = {"REV1": "main", "REV2": "main", "REV3": "main", "REVH": "small", "TGT": "main"}
lock = threading.Lock()


def bank(bank_dir=None):
    return list(csv.DictReader(open(os.path.join(bank_dir or paths.REPORT_BANK, "bank.csv"))))


# ★ KEY FUNCTION: fixed rule list (no model). Reads only the codebook and the structured specification. It was
# written with knowledge of the four planted flaws and serves as a benchmark, not as a candidate structure.
def checklist(b, datasets=None, truth_dir=None):
    did = b["dataset"]
    cb = open(os.path.join(datasets or paths.REPORT_DATASETS, did, "codebook.md")).read()
    late = [ln.split("|")[1].strip() for ln in cb.splitlines() if ln.startswith("|") and "2023" in ln]
    truth = json.load(open(os.path.join(truth_dir or paths.REPORT_TRUTH, f"{did}_truth.json")))
    s = STORIES[truth["story"]]
    ctrl_cols = {"none": [], "size_age": [s["z_size"][0], s["z_age"][0]],
                 "confounders": [s["z_size"][0], s["z_age"][0], s["z_prior"][0]],
                 "conf_plus_m": [s["z_size"][0], s["z_age"][0], s["z_prior"][0], s["m"][0]]}[b["controls"]]
    post = [c for c in ctrl_cols if c in late]
    prior_missing = s["z_prior"][0] not in ctrl_cols
    sub = b["sample"] != "all"
    return "reject" if (post or prior_missing or sub) else "approve"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model-main", default="claude-cli:claude-sonnet-5-5")
    ap.add_argument("--model-small", default="claude-cli:claude-haiku-5-5")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--cap", type=float, default=30.0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--collect-only", action="store_true")
    ap.add_argument("--scores", default=None, help="where to write verdicts.csv (default: --out)")
    a = ap.parse_args()
    out = a.out
    B = bank()
    if a.collect_only:
        collect(B, out, a.scores or out)
        return
    if os.path.exists(out) and os.listdir(out) and not a.resume:
        sys.exit(f"{out} is not empty")
    os.makedirs(os.path.join(out, "runs"), exist_ok=True)
    spec = {"main": a.model_main, "small": a.model_small}
    spent = [0.0]
    if os.path.exists(os.path.join(out, "calls.jsonl")):
        spent[0] = sum(json.loads(line).get("cost", 0) for line in open(os.path.join(out, "calls.jsonl")))
    jobs = [("review", b, arm) for b in B for arm in REVIEW_ARMS]
    jobs += [("repro", {"dataset": d}, f"REPRO{k}") for d in sorted({b["dataset"] for b in B}) for k in (1, 2, 3)]
    random.Random("e1R-order").shuffle(jobs)
    if a.limit:
        jobs = jobs[:a.limit]

    def run(kind, b, arm):
        rid = f"{b['dataset']}_{b.get('variant', 'data')}_{arm}"
        rdir = os.path.join(out, "runs", rid)
        if os.path.exists(os.path.join(rdir, "done.json")):
            return
        with lock:
            if spent[0] > a.cap:
                raise RuntimeError("cost cap reached")
        if os.path.exists(rdir):
            shutil.rmtree(rdir)  # an unfinished call leaves no partial verdict behind
        os.makedirs(rdir)
        wd = os.path.join(rdir, "work")
        os.makedirs(wd)
        truth = json.load(open(os.path.join(paths.REPORT_TRUTH, f"{b['dataset']}_truth.json")))
        if kind == "review":
            src = os.path.join(paths.REPORT_BANK, f"{b['dataset']}_{b['variant']}")
            for f in ("data.csv", "codebook.md", "report.md", "final_answer.json", "analysis.py"):
                shutil.copy(os.path.join(src, f), wd)
            task = VER_TASK.format(question=truth["question"]) + (TGT_LINE if arm == "TGT" else "")
            model = spec[REVIEW_ARMS[arm]]
            res, cost, _, dt = models.agent_call(wd, VER_SYSTEM, task, model, os.path.join(rdir, "transcript.jsonl"))
            v = models.read_json(os.path.join(wd, "verdict.json")) or {}
            outcome = str(v.get("decision", "")).strip().lower() or "missing"
        else:
            for f in ("data.csv", "codebook.md"):
                shutil.copy(os.path.join(paths.REPORT_DATASETS, b["dataset"], f), wd)
            task = GEN_TASK.format(question=truth["question"], pressure="", org=ORG_LINE["A0"])
            model = spec["main"]
            res, cost, _, dt = models.agent_call(wd, GEN_SYSTEM, task, model, os.path.join(rdir, "transcript.jsonl"))
            fa = models.read_json(os.path.join(wd, "final_answer.json")) or {}
            outcome = str(fa.get("conclusion", "")).strip().lower() or "missing"
        p = os.path.join(wd, "data.csv")  # keep the run folder small; the data are in data/reports/datasets/
        if os.path.exists(p):
            os.remove(p)
        rec = dict(id=rid, kind=kind, dataset=b["dataset"], variant=b.get("variant", ""), arm=arm,
                   model=models.model_name(model), outcome=outcome, cost=cost, seconds=round(dt, 1),
                   finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        json.dump(rec, open(os.path.join(rdir, "done.json"), "w"))
        with lock:
            spent[0] += cost
            with open(os.path.join(out, "calls.jsonl"), "a") as f:
                f.write(json.dumps(rec) + "\n")

    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(run, *j) for j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                fu.result()
            except Exception as e:
                print("FAILED:", repr(e)[:150], flush=True)
            if i % 10 == 0:
                print(f"{i}/{len(jobs)} {time.strftime('%H:%M:%S')}", flush=True)
    collect(B, out, a.scores or out)


# ★ CORE LOGIC: one row per report with each structure's decision. REPROk approves a report when the report's
# conclusion equals reanalysis k's conclusion (the comparison unit is the conclusion); CHK is the rule list.
def collect(B, out, scores_dir):
    done = {}
    for d in os.listdir(os.path.join(out, "runs")):
        f = os.path.join(out, "runs", d, "done.json")
        if os.path.exists(f):
            r = json.load(open(f))
            done[(r["dataset"], r["variant"], r["arm"])] = r["outcome"]
    rows = []
    for b in B:
        row = dict(b)
        for arm in REVIEW_ARMS:
            row[f"dec_{arm}"] = done.get((b["dataset"], b["variant"], arm), "")
        for k in (1, 2, 3):
            rc = done.get((b["dataset"], "", f"REPRO{k}"), "")
            row[f"repro{k}_concl"] = rc
            row[f"dec_REPRO{k}"] = "" if not rc else ("approve" if rc == b["report_conclusion"] else "reject")
        row["dec_CHK"] = checklist(b)
        rows.append(row)
    os.makedirs(scores_dir, exist_ok=True)
    with open(os.path.join(scores_dir, "verdicts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print("collected", len(rows))


if __name__ == "__main__":
    main()
