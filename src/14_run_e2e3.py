# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-29 (reference run); 2026-10-31 (collection of stored responses)
# TIME TAKEN   : ~1.5 hours for 324 calls; collection ~5 s
# DESCRIPTION  : Experiments E2 and E3 (preregistration/e2e3_prereg_en.md), main model only.
#                E2, report task, own analysis then review (PTR1-3): a reviewer that first analyzed the dataset
#                on its own (the E1 reanalyses REPRO1-3, reused as inputs) reviews the analyst's report with its
#                own analysis at hand. Same model and information as E1 review; only the order differs.
#                E3, both tasks, role panel (ROLE1-3): three reviewers with different role instructions, compared
#                with E1's same-instruction panel (REV1-3).
#                Calls blocked by a usage limit are recorded as failed_cap (not as a decision) and rerun with
#                --resume. --collect-only skips all model calls and tabulates the stored responses.
# INPUT FILES  : <e1 reports run>/runs/*_REPRO*/work/ (own analyses), data/reports/*, data/ledgers/*
# OUTPUT FILES : <out>/R/runs/<id>/, <out>/L/responses/, <out>/calls.jsonl, <scores>/R_verdicts.csv,
#                <scores>/L_rows.csv
# USAGE        : python src/14_run_e2e3.py --out <dir> [--model-main ...] [--e1-reports runs/e1_reports]
#                python src/14_run_e2e3.py --out runs/e2e3 --collect-only --scores <dir>
# ============================================================
import argparse
import csv
import importlib.util
import json
import os
import random
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lib import ledger_task as lt  # noqa: E402
from lib import models, paths  # noqa: E402
from lib.report_prompts import PTR_TASK, ROLES_R, VER_SYSTEM, VER_TASK  # noqa: E402


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, file))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


eL = _load("eL", "11_run_e1_ledger.py")
eR = _load("eR", "12_run_e1_reports.py")
lock = threading.Lock()

ROLES_L = {
    "ROLE1": " Work row by row: for each draft row, find its source document and compare every field.",
    "ROLE2": " Assume the draft contains several errors and hunt for them.",
    "ROLE3": " Work from the documents: go through the documents in order and check that each one is recorded correctly in the draft.",
}


def run_R(job, out, spent, cap, model, e1r):
    kind, b, arm, k = job
    rid = f"{b['dataset']}_{b['variant']}_{arm}"
    rdir = os.path.join(out, "R", "runs", rid)
    if os.path.exists(os.path.join(rdir, "done.json")):
        return
    with lock:
        if spent[0] > cap:
            raise RuntimeError("cost cap reached")
    if os.path.exists(rdir):
        shutil.rmtree(rdir)
    wd = os.path.join(rdir, "work")
    os.makedirs(wd)
    truth = json.load(open(os.path.join(paths.REPORT_TRUTH, f"{b['dataset']}_truth.json")))
    src = os.path.join(paths.REPORT_BANK, f"{b['dataset']}_{b['variant']}")
    for f in ("data.csv", "codebook.md", "report.md", "final_answer.json", "analysis.py"):
        shutil.copy(os.path.join(src, f), wd)
    if kind == "ptr":
        own = os.path.join(e1r, "runs", f"{b['dataset']}_data_REPRO{k}", "work")
        for f in os.listdir(own):
            if f.endswith(".py") or f in ("report.md", "final_answer.json"):
                shutil.copy(os.path.join(own, f), os.path.join(wd, "own_" + f))
        task = PTR_TASK.format(question=truth["question"])
    else:
        task = VER_TASK.format(question=truth["question"]) + ROLES_R[arm]
    res, cost, _, dt = models.agent_call(wd, VER_SYSTEM, task, model, os.path.join(rdir, "transcript.jsonl"))
    v = models.read_json(os.path.join(wd, "verdict.json")) or {}
    outcome = str(v.get("decision", "")).strip().lower() or "missing"
    tr = open(os.path.join(rdir, "transcript.jsonl")).read()
    if "Spending cap reached" in tr:
        outcome = "failed_cap"  # infrastructure failure, not a judgment; rerun with --resume
    os.remove(os.path.join(wd, "data.csv"))
    rec = dict(task="R", id=rid, dataset=b["dataset"], variant=b["variant"], arm=arm, outcome=outcome, cost=cost,
               seconds=round(dt, 1), finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
    if outcome != "failed_cap":
        json.dump(rec, open(os.path.join(rdir, "done.json"), "w"))
    with lock:
        spent[0] += cost
        with open(os.path.join(out, "calls.jsonl"), "a") as f:
            f.write(json.dumps(rec) + "\n")


def run_L(job, out, spent, cap, model):
    p, arm = job
    rp = os.path.join(out, "L", "responses", f"{p['tag']}_{p['fmt']}_{arm}.txt")
    if os.path.exists(rp):
        return
    with lock:
        if spent[0] > cap:
            raise RuntimeError("cost cap reached")
    prompt = (lt.head(p) + eL.REVIEW + ROLES_L[arm] + "\n\n" + lt.EDIT_FORMAT + "Return only the CSV.\n\nDOCUMENTS:\n"
              + p["docs"] + "\n\nDRAFT LEDGER:\n" + lt.draft_table(p["rows"], "N"))
    text, cost, _ = eL.call(prompt, model)  # raises on a failed call (including a usage limit); --resume reruns
    open(rp, "w").write(text)
    with lock:
        spent[0] += cost
        with open(os.path.join(out, "calls.jsonl"), "a") as f:
            f.write(json.dumps(dict(task="L", tag=p["tag"], fmt=p["fmt"], arm=arm, cost=cost,
                                    finished=time.strftime("%Y-%m-%dT%H:%M:%S%z"))) + "\n")


def collect(out, scores_dir):
    B = eR.bank()
    done = {}
    for d in os.listdir(os.path.join(out, "R", "runs")):
        f = os.path.join(out, "R", "runs", d, "done.json")
        if os.path.exists(f):
            r = json.load(open(f))
            done[(r["dataset"], r["variant"], r["arm"])] = r["outcome"]
    rows = []
    for b in B:
        row = dict(b)
        for arm in ["PTR1", "PTR2", "PTR3", "ROLE1", "ROLE2", "ROLE3"]:
            row[f"dec_{arm}"] = done.get((b["dataset"], b["variant"], arm), "")
        rows.append(row)
    os.makedirs(scores_dir, exist_ok=True)
    with open(os.path.join(scores_dir, "R_verdicts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # ledger task: detection and final correctness for the role arms, same scoring as E1
    P = lt.packets()
    lrows = []
    for p in P:
        by_doc = {d: k for k in p["key"] for d in k["doc_ids"].split("|")}
        res = {}
        for arm in ROLES_L:
            f = os.path.join(out, "L", "responses", f"{p['tag']}_{p['fmt']}_{arm}.txt")
            if os.path.exists(f):
                t, final, _ = eL.touched_and_final(p, open(f).read())
                res[arm] = (t, final)
        for i, r in enumerate(p["rows"], 1):
            k = by_doc.get(r["doc_ids"].split("|")[0])
            if k is None:
                continue
            draft_ok = lt.txn_correct(k, [dict(x, amount=float(x["amount"])) for x in p["rows"]])
            row = dict(tag=p["tag"], fmt=p["fmt"], row=i, cls="seeded" if r["seeded"] else ("correct" if draft_ok else "natural"),
                       kind=r["seeded"])
            for arm, (t, final) in res.items():
                row[f"det_{arm}"] = int(i in t)
                row[f"ok_{arm}"] = int(lt.txn_correct(k, final))
            lrows.append(row)
    with open(os.path.join(scores_dir, "L_rows.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lrows[0]))
        w.writeheader()
        w.writerows(lrows)
    print("collected", len(rows), len(lrows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--model-main", default="claude-cli:claude-sonnet-5-5")
    ap.add_argument("--e1-reports", default=str(paths.RUN_E1_REPORTS), help="E1 report run with REPRO1-3")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--cap", type=float, default=35.0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--collect-only", action="store_true")
    ap.add_argument("--scores", default=None, help="where to write R_verdicts.csv and L_rows.csv (default: --out)")
    a = ap.parse_args()
    out = a.out
    if a.collect_only:
        collect(out, a.scores or out)
        return
    if os.path.exists(out) and os.listdir(out) and not a.resume:
        sys.exit(f"{out} is not empty")
    os.makedirs(os.path.join(out, "R", "runs"), exist_ok=True)
    os.makedirs(os.path.join(out, "L", "responses"), exist_ok=True)
    spent = [0.0]
    if os.path.exists(os.path.join(out, "calls.jsonl")):
        spent[0] = sum(json.loads(line).get("cost", 0) for line in open(os.path.join(out, "calls.jsonl")))
    B = eR.bank()
    jobs = [("R", ("ptr", b, f"PTR{k}", k)) for b in B for k in (1, 2, 3)]
    jobs += [("R", ("role", b, arm, 0)) for b in B for arm in ROLES_R]
    jobs += [("L", (p, arm)) for p in lt.packets() for arm in ROLES_L]
    random.Random("e2e3-order").shuffle(jobs)
    with ThreadPoolExecutor(a.workers) as ex:
        futs = [ex.submit(run_R, j, out, spent, a.cap, a.model_main, a.e1_reports) if t == "R"
                else ex.submit(run_L, j, out, spent, a.cap, a.model_main) for t, j in jobs]
        for i, fu in enumerate(as_completed(futs), 1):
            try:
                fu.result()
            except Exception as e:
                print("FAILED:", repr(e)[:150], flush=True)
            if i % 25 == 0:
                print(f"{i}/{len(jobs)} {time.strftime('%H:%M:%S')}", flush=True)
    collect(out, a.scores or out)


if __name__ == "__main__":
    main()
