# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~3 min on a laptop CPU (stored mode)
# DESCRIPTION  : Reproduces every table, figure and cited number of the proposal from the stored model outputs,
#                without calling any model:
#                  1. rebuilds the synthetic report datasets, report bank, ledger packets and seeded drafts from
#                     their seeds and checks that they are byte-identical to data/;
#                  2. rescores the stored responses of the pilot, S1, E1, E2 and E3 and checks the scores against
#                     the stored scores;
#                  3. reruns the preregistered analyses and checks the results against reference/;
#                  4. redraws the two proposal figures and recomputes the cited numbers.
#                With --live it also sends a small slice of items to a model of your choice (src/18).
#                Writes outputs/<run>/receipt.json with SHA-256 hashes of inputs and outputs, package versions
#                and step times. Refuses to write into a non-empty output folder.
# INPUT FILES  : data/, runs/, reference/, config/
# OUTPUT FILES : outputs/<run>/... , outputs/<run>/receipt.json, outputs/<run>/comparisons.json
# USAGE        : python run_all.py [--out outputs/<name>] [--skip-generators]
#                python run_all.py --live --model claude-cli:claude-haiku-5-5 [--n-ledger 2 --n-reports 2]
# ============================================================
import argparse
import filecmp
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
PY = sys.executable


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree_hashes(d):
    d = Path(d)
    return {str(p.relative_to(ROOT)): sha(p) for p in sorted(d.rglob("*")) if p.is_file() and p.name != ".DS_Store"}


def tree_digest(d):
    """One SHA-256 over the sorted (path, file hash) list of a folder."""
    h = hashlib.sha256()
    for k, v in tree_hashes(d).items():
        h.update(f"{k}\t{v}\n".encode())
    return h.hexdigest()


def same_tree(a, b, ignore=(".DS_Store",)):
    """Byte comparison of two folders. Returns the list of differing or one-sided relative paths."""
    a, b = Path(a), Path(b)
    fa = {str(p.relative_to(a)) for p in a.rglob("*") if p.is_file() and p.name not in ignore}
    fb = {str(p.relative_to(b)) for p in b.rglob("*") if p.is_file() and p.name not in ignore}
    diff = sorted(fa ^ fb)
    diff += sorted(f for f in fa & fb if not filecmp.cmp(a / f, b / f, shallow=False))
    return diff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-generators", action="store_true", help="skip step 1 (saves about a minute)")
    ap.add_argument("--live", action="store_true", help="also run a small live slice with --model")
    ap.add_argument("--model", default="claude-cli:claude-haiku-5-5")
    ap.add_argument("--n-ledger", type=int, default=2)
    ap.add_argument("--n-reports", type=int, default=2)
    a = ap.parse_args()
    out = Path(a.out) if a.out else ROOT / "outputs" / time.strftime("run_%Y%m%d_%H%M%S")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty; choose a new folder")
    out.mkdir(parents=True, exist_ok=True)
    (out / "logs").mkdir()
    runs = ROOT / "runs"
    d = out
    steps = []
    if not a.skip_generators:
        steps += [
            ("01_report_datasets", ["01_make_report_datasets.py", "--out", d / "data/reports"]),
            ("02_report_bank", ["02_make_report_bank.py", "--datasets", d / "data/reports/datasets", "--truth",
                                d / "data/reports/truth", "--out", d / "data/reports/bank"]),
            ("03_ledger_packets", ["03_make_ledger_packets.py", "--out", d / "data/ledgers/packets"]),
            ("05_seeded_drafts", ["05_seed_ledger_drafts.py", "--out", d / "data/ledgers/seeded"]),
        ]
    steps += [
        ("07_score_pilot", ["07_score_pilot.py", "--run", runs / "pilot", "--out", d / "pilot"]),
        ("08_score_s1_locked_parser", ["08_run_s1.py", "--out", runs / "s1", "--score-only", "--scores", d / "s1_locked"]),
        ("09_rescore_s1_content_parser", ["09_rescore_s1.py", "--run", runs / "s1", "--out", d / "s1_content"]),
        ("10_analyze_s1_locked", ["10_analyze_s1.py", d / "s1_locked", d / "s1_locked"]),
        ("10_analyze_s1_content", ["10_analyze_s1.py", d / "s1_content", d / "s1_content"]),
        ("11_score_e1_ledger", ["11_run_e1_ledger.py", "--out", runs / "e1_ledger", "--score-only", "--scores", d / "e1_ledger"]),
        ("12_collect_e1_reports", ["12_run_e1_reports.py", "--out", runs / "e1_reports", "--collect-only", "--scores",
                                   d / "e1_reports"]),
        ("13_analyze_e1", ["13_analyze_e1.py", d / "e1_ledger", d / "e1_reports", d / "e1"]),
        ("14_collect_e2e3", ["14_run_e2e3.py", "--out", runs / "e2e3", "--collect-only", "--scores", d / "e2e3"]),
        ("15_analyze_e2e3", ["15_analyze_e2e3.py", d / "e1_ledger", d / "e1_reports", d / "e2e3", d / "e2e3"]),
        ("16_figures", ["16_make_figures.py", d / "e1/e1_analysis.json", d / "e2e3/e2e3_analysis.json", d / "figures"]),
        ("17_check_numbers", ["17_check_numbers.py", d, runs]),
    ]
    if a.live:
        steps.append(("18_live_slice", ["18_live_slice.py", "--out", d / "live", "--model", a.model,
                                        "--n-ledger", str(a.n_ledger), "--n-reports", str(a.n_reports)]))
    times, failed = {}, []
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
    t_all = time.time()
    for name, args in steps:
        t0 = time.time()
        cmd = [PY, str(SRC / args[0])] + [str(x) for x in args[1:]]
        with open(out / "logs" / f"{name}.log", "w") as log:
            r = subprocess.run(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, env=env)
        times[name] = round(time.time() - t0, 1)
        status = "ok" if r.returncode == 0 else f"FAILED (exit {r.returncode})"
        print(f"{name:32s} {times[name]:7.1f} s  {status}", flush=True)
        if r.returncode != 0:
            failed.append(name)

    # ★ CORE LOGIC: every regenerated or recomputed file is compared byte for byte with the stored version.
    checks = {}
    if not a.skip_generators:
        checks["report datasets and truth"] = same_tree(d / "data/reports/datasets", ROOT / "data/reports/datasets") + \
            same_tree(d / "data/reports/truth", ROOT / "data/reports/truth")
        checks["report bank"] = same_tree(d / "data/reports/bank", ROOT / "data/reports/bank")
        checks["ledger packets"] = same_tree(d / "data/ledgers/packets", ROOT / "data/ledgers/packets")
        checks["seeded drafts"] = [f for f in same_tree(d / "data/ledgers/seeded", ROOT / "data/ledgers/seeded")
                                   if f != "seed_logs.json"]
    pairs = [
        ("pilot scores", d / "pilot/runs_scored.csv", ROOT / "reference/pilot/runs_scored.csv"),
        ("pilot summary", d / "pilot/cell_summary.csv", ROOT / "reference/pilot/cell_summary.csv"),
        ("S1 scores, parser fixed in plan", d / "s1_locked/packet_scores.csv", runs / "s1/packet_scores.csv"),
        ("S1 transaction scores, parser fixed in plan", d / "s1_locked/error_scores.csv", runs / "s1/error_scores.csv"),
        ("S1 analysis, parser fixed in plan", d / "s1_locked/analysis.json", ROOT / "reference/s1/analysis_locked_parser.json"),
        ("S1 scores, content parser", d / "s1_content/packet_scores.csv", ROOT / "reference/s1/rescored/packet_scores.csv"),
        ("S1 analysis, content parser", d / "s1_content/analysis.json", ROOT / "reference/s1/rescored/analysis.json"),
        ("E1 ledger scores", d / "e1_ledger/rows.csv", runs / "e1_ledger/rows.csv"),
        ("E1 report verdicts", d / "e1_reports/verdicts.csv", runs / "e1_reports/verdicts.csv"),
        ("E1 analysis", d / "e1/e1_analysis.json", ROOT / "reference/e1/e1_analysis.json"),
        ("E2/E3 ledger scores", d / "e2e3/L_rows.csv", runs / "e2e3/L_rows.csv"),
        ("E2/E3 report verdicts", d / "e2e3/R_verdicts.csv", runs / "e2e3/R_verdicts.csv"),
        ("E2/E3 analysis", d / "e2e3/e2e3_analysis.json", ROOT / "reference/e2e3/e2e3_analysis.json"),
        ("Figure 1 data", d / "figures/figure_1_data.csv", ROOT / "reference/figures/figure_1_data.csv"),
        ("Figure 2 data", d / "figures/figure_2_data.csv", ROOT / "reference/figures/figure_2_data.csv"),
    ]
    for label, x, y in pairs:
        checks[label] = [] if (x.exists() and filecmp.cmp(x, y, shallow=False)) else [str(x.relative_to(out))]
    # Images depend on installed fonts and library versions, so they are reported but do not fail the run.
    image_same = {f: (d / "figures" / f).exists() and filecmp.cmp(d / "figures" / f, ROOT / "reference/figures" / f, shallow=False)
                  for f in ("figure_1.png", "figure_2.png")}
    numbers = []
    nc = d / "proposal_numbers_check.csv"
    if nc.exists():
        import csv
        numbers = list(csv.DictReader(open(nc)))
    n_match = sum(int(r["match"]) for r in numbers)
    n_rounding = sum(1 for r in numbers if not int(r["match"]) and r["note"].startswith("ROUNDING"))
    comparisons = dict(byte_identical={k: not v for k, v in checks.items()}, differences=checks,
                       figure_images_identical=image_same,
                       proposal_numbers=dict(matched=n_match, explained_rounding_differences=n_rounding, total=len(numbers)),
                       failed_steps=failed)
    (out / "comparisons.json").write_text(json.dumps(comparisons, indent=1) + "\n")

    pk = {}
    for name in ("numpy", "pandas", "statsmodels", "matplotlib"):
        try:
            pk[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            pk[name] = None
    receipt = dict(
        run=out.name, started=time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(t_all)),
        total_seconds=round(time.time() - t_all, 1), step_seconds=times,
        environment=dict(python=platform.python_version(), platform=platform.platform(), packages=pk),
        model_calls="none" if not a.live else f"live slice only ({a.model})",
        inputs=dict(files={**tree_hashes(ROOT / "config"), **tree_hashes(ROOT / "data")},
                    stored_runs_tree_sha256={p.name: tree_digest(p) for p in sorted(runs.iterdir()) if p.is_dir()},
                    reference=tree_hashes(ROOT / "reference"),
                    code={**tree_hashes(SRC), "run_all.py": sha(ROOT / "run_all.py")}),
        outputs={str(p.relative_to(out)): sha(p) for p in sorted(out.rglob("*"))
                 if p.is_file() and p.parent.name != "logs" and p.name != "receipt.json"},
        comparisons=comparisons,
        not_done=["no model was called" if not a.live else "only the live slice called a model",
                  "the stored model outputs in runs/ were not regenerated"],
    )
    (out / "receipt.json").write_text(json.dumps(receipt, indent=1, default=str) + "\n")
    ok = not failed and all(not v for v in checks.values()) and n_match + n_rounding == len(numbers) and numbers
    print(f"\nbyte-identical checks: {sum(not v for v in checks.values())} of {len(checks)}; "
          f"figure images identical: {sum(image_same.values())} of 2; proposal numbers matched: {n_match} of {len(numbers)}"
          f" (plus {n_rounding} printed value that differs only by rounding; see proposal_numbers_check.csv)")
    print(f"total {receipt['total_seconds']} s; receipt: {out / 'receipt.json'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
