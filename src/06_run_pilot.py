# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-25 (reference run); repository version not rerun
# TIME TAKEN   : ~2 hours for 48 organizations
# DESCRIPTION  : Model step, pilot (appendix A7). One run = one AI analyst analyzing one dataset, followed by
#                0, 1 or 3 AI reviewers under a fixed approval rule (A0 solo, A1 single reviewer, A2 any of three,
#                A3 all of three), with at most one resubmission. The pilot found no analyst errors, which led to
#                the planted-error design of S1, E1, E2 and E3.
# INPUT FILES  : config/pilot_design.json, data/reports/datasets/<id>/{data.csv, codebook.md},
#                data/reports/truth/<id>_truth.json (question text only)
# OUTPUT FILES : <out>/<run_id>/... (all transcripts), <out>/ledger.jsonl
# USAGE        : python src/06_run_pilot.py --out <dir> [--model claude-cli:claude-sonnet-5-5] [--only RUN_ID]
# ============================================================
import argparse
import glob
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import models, paths  # noqa: E402
from lib.report_prompts import (GEN_SYSTEM, GEN_TASK, N_REVIEWERS, ORG_LINE, PRESSURE, PROMPT_SHA,  # noqa: E402
                                REVISE_MSG, VER_SYSTEM, VER_TASK)


def run_one(design, run, rdir, model, datasets, truth_dir):
    truth = json.load(open(os.path.join(truth_dir, run["dataset"] + "_truth.json")))
    dsrc = os.path.join(datasets, run["dataset"])
    os.makedirs(rdir, exist_ok=False)  # ★ IMPORTANT: a run folder is written once, never reused
    gdir = os.path.join(rdir, "gen")
    os.makedirs(gdir)
    for f in ("data.csv", "codebook.md"):
        shutil.copy(os.path.join(dsrc, f), gdir)
    task = GEN_TASK.format(question=truth["question"],
                           pressure=PRESSURE[run["pressure"]].format(hypothesis=truth["hypothesis"]),
                           org=ORG_LINE[run["org"]])
    rec = {"run_id": run["run_id"], "dataset": run["dataset"], "org": run["org"], "pressure": run["pressure"],
           "model": models.model_name(model), "prompt_sha256": PROMPT_SHA, "rounds": [], "cost_usd": 0.0,
           "start": time.time()}
    res, cost, sid, dt = models.agent_call(gdir, GEN_SYSTEM, task, model, os.path.join(rdir, "gen_transcript.jsonl"))
    rec["cost_usd"] += cost
    released = False
    for rnd in (1, 2):
        ans = models.read_json(os.path.join(gdir, "final_answer.json"))
        rinfo = {"round": rnd, "gen_seconds": round(dt, 1), "gen_cost": cost, "answer": ans, "verdicts": []}
        k = N_REVIEWERS[run["org"]]
        if k == 0:
            released = True
        else:
            for j in range(k):
                vdir = os.path.join(rdir, f"ver_r{rnd}_{j + 1}")
                os.makedirs(vdir)
                for f in glob.glob(os.path.join(gdir, "*")):
                    b = os.path.basename(f)
                    if b in ("data.csv", "codebook.md", "report.md", "final_answer.json") or b.endswith(".py"):
                        shutil.copy(f, vdir)
                vres, vcost, _, vdt = models.agent_call(vdir, VER_SYSTEM, VER_TASK.format(question=truth["question"]),
                                                        model, os.path.join(rdir, f"ver_r{rnd}_{j + 1}_transcript.jsonl"))
                rec["cost_usd"] += vcost
                v = models.read_json(os.path.join(vdir, "verdict.json")) or {}
                dec = str(v.get("decision", "")).strip().lower()
                rinfo["verdicts"].append({"reviewer": j + 1, "decision": dec or "missing",
                                          "reason": v.get("reason"), "cost": vcost, "seconds": round(vdt, 1)})
            approvals = sum(1 for v in rinfo["verdicts"] if v["decision"] == "approve")
            # ★ CORE LOGIC: approval rules (Sah-Stiglitz polyarchy vs hierarchy)
            released = approvals >= 1 if run["org"] in ("A1", "A2") else approvals == k
        rec["rounds"].append(rinfo)
        if released or rnd == 2:
            break
        res, cost, sid2, dt = models.agent_call(gdir, GEN_SYSTEM, REVISE_MSG, model,
                                                os.path.join(rdir, "gen_transcript.jsonl"), resume=sid)
        sid = sid2 or sid
        rec["cost_usd"] += cost
    final_ans = models.read_json(os.path.join(gdir, "final_answer.json"))
    rec["released"] = released
    rec["final_conclusion"] = (final_ans or {}).get("conclusion") if released else "withheld"
    rec["final_answer"] = final_ans
    rec["end"] = time.time()
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--design", default=str(paths.CONFIG / "pilot_design.json"))
    ap.add_argument("--model", default=None, help="default: the model named in the design file (Claude Code CLI)")
    ap.add_argument("--datasets", default=str(paths.REPORT_DATASETS))
    ap.add_argument("--truth", default=str(paths.REPORT_TRUTH))
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    design = json.load(open(a.design))
    model = a.model or design["model"]
    os.makedirs(a.out, exist_ok=True)
    ledger = os.path.join(a.out, "ledger.jsonl")
    done, spent = set(), 0.0
    if os.path.exists(ledger):
        for line in open(ledger):
            r = json.loads(line)
            done.add(r["run_id"])
            spent += r["cost_usd"]
    for run in design["runs"]:
        if run["run_id"] in done or (a.only and run["run_id"] != a.only):
            continue
        # ★ IMPORTANT: hard cost cap. Stop before a run that could cross it.
        if spent + design["max_cost_per_run_usd"] > design["cost_cap_usd"]:
            print(f"STOP cost cap: spent {spent:.2f}")
            break
        rec = run_one(design, run, os.path.join(a.out, run["run_id"]), model, a.datasets, a.truth)
        spent += rec["cost_usd"]
        with open(ledger, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        print(json.dumps({"run": rec["run_id"], "org": rec["org"], "final": rec["final_conclusion"],
                          "rounds": len(rec["rounds"]), "cost": round(rec["cost_usd"], 3)}), flush=True)


if __name__ == "__main__":
    main()
