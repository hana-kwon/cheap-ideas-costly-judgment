# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~10 s
# DESCRIPTION  : Builds the six synthetic report-task datasets (two with a planted effect of 0.08, two with
#                0.05, two with zero effect) from the seeds in data/reports/manifest.json, and computes for
#                each dataset the estimate in all 256 plausible specifications (truth files). Optional
#                --calibrate prints the grid used to choose effect sizes and confounding strength.
# INPUT FILES  : data/reports/manifest.json
# OUTPUT FILES : <out>/datasets/<id>/{data.csv, codebook.md}, <out>/truth/<id>_truth.json,
#                <out>/truth/<id>_specspace.csv
# USAGE        : python src/01_make_report_datasets.py --out outputs/<run>/data/reports
# ============================================================
import argparse
import itertools
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import paths  # noqa: E402
from lib.report_data import N, SECTOR_LEVELS, STORIES, correct_spec, simulate, spec_space  # noqa: E402


def calibrate(out):
    """Grid over beta, confounding and outlier size. Prints the power of the correct specification and the
    share of the specification space with a positive significant estimate."""
    rows = []
    for conf, osh, beta in itertools.product([0.15, 0.25, 0.35], [0.0, 3.0], [0.0, 0.045, 0.075]):
        res = []
        for seed in range(25):
            df = simulate(10_000 + seed, beta, conf, osh)
            sp = spec_space(df, "training")
            c = correct_spec(sp)
            res.append({"correct_sig_pos": (c.p < 0.05) and (c.coef > 0),
                        "share_sig_pos": float(((sp.p < 0.05) & (sp.coef > 0)).mean()),
                        "share_sig_neg": float(((sp.p < 0.05) & (sp.coef < 0)).mean())})
        r = pd.DataFrame(res).mean().to_dict()
        r.update({"conf": conf, "outlier_shift": osh, "beta": beta})
        rows.append(r)
        print(json.dumps(r))
    os.makedirs(out, exist_ok=True)
    pd.DataFrame(rows).to_csv(os.path.join(out, "calibration_grid.csv"), index=False)


def build(manifest_path, out):
    man = json.load(open(manifest_path))
    os.makedirs(os.path.join(out, "truth"), exist_ok=True)
    for d in man["datasets"]:
        df = simulate(d["seed"], d["beta"], man["conf"], man["outlier_shift"], d["story"])
        s = STORIES[d["story"]]
        ddir = os.path.join(out, "datasets", d["id"])
        os.makedirs(ddir, exist_ok=False)  # ★ IMPORTANT: never overwrite an existing dataset
        df.to_csv(os.path.join(ddir, "data.csv"), index=False)
        cols = [(s["x"][0], s["x"][1]), (s["y"][0], s["y"][1]), (s["z_size"][0], s["z_size"][1]),
                (s["z_age"][0], s["z_age"][1]), (s["z_prior"][0], s["z_prior"][1]), (s["m"][0], s["m"][1]),
                (s["region"], "Region (north, central, south)"), (s["public"], "1 if publicly listed"),
                (s["sector"], "Sector: " + " / ".join(SECTOR_LEVELS[d["story"]]))]
        cols += [(c, "Firm characteristic measured in 2020 (pre-period)") for c in s["w"]]
        cb = ["# Codebook", "", f"Unit: one row per firm ({N} {s['unit']}). Cross-section.", "",
              "| column | description |", "|---|---|", "| firm_id | Firm identifier |"]
        cb += [f"| {c} | {t} |" for c, t in cols]
        open(os.path.join(ddir, "codebook.md"), "w").write("\n".join(cb) + "\n")
        sp = spec_space(df, d["story"])
        sp.to_csv(os.path.join(out, "truth", d["id"] + "_specspace.csv"), index=False)
        c = correct_spec(sp)
        truth = {"id": d["id"], "story": d["story"], "type": d["type"], "beta": d["beta"], "seed": d["seed"],
                 "conf": man["conf"], "outlier_shift": man["outlier_shift"],
                 "true_effect_sign": "positive" if d["beta"] > 0 else "none",
                 "correct_spec": {"coef": float(c.coef), "se": float(c.se), "p": float(c.p)},
                 "share_specs_sig_pos": float(((sp.p < 0.05) & (sp.coef > 0)).mean()),
                 "share_specs_sig_neg": float(((sp.p < 0.05) & (sp.coef < 0)).mean()),
                 "question": s["question"], "hypothesis": s["hypothesis"]}
        json.dump(truth, open(os.path.join(out, "truth", d["id"] + "_truth.json"), "w"), indent=1)
        print(json.dumps({k: truth[k] for k in ["id", "type", "beta", "share_specs_sig_pos"]}
                         | {"p_correct": truth["correct_spec"]["p"]}))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--manifest", default=str(paths.REPORT_MANIFEST))
    ap.add_argument("--calibrate", action="store_true")
    a = ap.parse_args()
    if a.calibrate:
        calibrate(a.out)
    else:
        build(a.manifest, a.out)


if __name__ == "__main__":
    main()
