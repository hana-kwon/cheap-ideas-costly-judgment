# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~30 s
# DESCRIPTION  : Report bank with planted flaws. For each of the six datasets, five analyst reports are built
#                deterministically from the specification table: one correct (pre-treatment confounders, full
#                sample, level outcome, 1 percent trim) and four flawed (control measured after treatment,
#                omitted pre-period outcome, no controls, favorable subgroup only). Each report folder holds
#                report.md, final_answer.json and analysis.py, which reproduces the reported number.
#                Gate: every analysis.py is executed and must reproduce its specification-table estimate.
# INPUT FILES  : <datasets>/<id>/{data.csv, codebook.md}, <truth>/<id>_truth.json, <truth>/<id>_specspace.csv
# OUTPUT FILES : <out>/<dataset>_<variant>/{data.csv, codebook.md, report.md, final_answer.json, analysis.py},
#                <out>/bank.csv (variant, flaw, conclusions)
# USAGE        : python src/02_make_report_bank.py --datasets <dir> --truth <dir> --out <empty dir>
# ============================================================
import argparse
import json
import os
import shutil
import subprocess
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import paths  # noqa: E402
from lib.report_data import STORIES  # noqa: E402

DATASETS = ["p01", "p02", "p03", "p04", "p05", "p06"]


def conclusion(coef, p):
    if p < 0.05:
        return "positive effect" if coef > 0 else "negative effect"
    return "no effect"


# ★ CORE LOGIC: the four flaws. Each is a choice a careful reviewer should object to; whether it also changes
# the conclusion is recorded separately (conclusion_wrong), because a flawed method can land on the right
# answer by luck.
def pick_variants(sp, truth_concl):
    row = lambda c, s: sp[(sp.controls == c) & (sp["sample"] == s) & (sp.form == "level") & (sp.outliers == "trim1")].iloc[0]
    out = {"V0_correct": ("confounders", "all", None), "V1_collider": ("conf_plus_m", "all", "collider"),
           "V2_omit_prior": ("size_age", "all", "omitted_prior"), "V3_no_controls": ("none", "all", "no_controls")}
    # Favorable subgroup: the subsample (correct controls) whose conclusion departs most from the truth. For a
    # true effect that is the least significant subgroup; for a null, the most significant positive one.
    subs = sp[(sp.controls == "confounders") & (sp["sample"] != "all") & (sp.form == "level") & (sp.outliers == "trim1")]
    if truth_concl == "positive effect":
        s = subs.sort_values("p", ascending=False).iloc[0]
    else:
        pos = subs[subs.coef > 0]
        s = (pos if len(pos) else subs).sort_values("p").iloc[0]
    out["V4_subgroup"] = ("confounders", s["sample"], "subgroup_only")
    return {k: (c, smp, flaw, row(c, smp)) for k, (c, smp, flaw) in out.items()}


RATIONALE = {
    None: "I control for firm size, firm age and the pre-period value of the outcome, all measured before treatment, and trim the top and bottom 1% of the outcome.",
    "collider": "I control for firm size, firm age, the pre-period value of the outcome and {m}, which captures an important determinant of the outcome, and trim the top and bottom 1% of the outcome.",
    "omitted_prior": "I control for firm size and firm age and trim the top and bottom 1% of the outcome.",
    "no_controls": "I report the simple regression of the outcome on the treatment, which is transparent and easy to interpret, after trimming the top and bottom 1% of the outcome.",
    "subgroup_only": "I focus on the {label} subsample, where the data are most comparable, control for firm size, firm age and the pre-period value of the outcome, and trim the top and bottom 1% of the outcome.",
}


def code_for(story, controls, sample):
    s = STORIES[story]
    cols = {"none": [], "size_age": [s["z_size"][0], s["z_age"][0]],
            "confounders": [s["z_size"][0], s["z_age"][0], s["z_prior"][0]],
            "conf_plus_m": [s["z_size"][0], s["z_age"][0], s["z_prior"][0], s["m"][0]]}[controls]
    if sample == "all":
        filt = ""
    elif sample.startswith("region_"):
        filt = f"df = df[df['{s['region']}'] == '{sample[7:]}']\n"
    elif sample.startswith("listed_"):
        filt = f"df = df[df['{s['public']}'] == {sample[7:]}]\n"
    else:
        filt = f"df = df[df['{s['sector']}'] == '{sample[7:]}']\n"
    return f"""import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data.csv")
{filt}y = df["{s['y'][0]}"]
lo, hi = y.quantile([0.01, 0.99])
df = df[(y >= lo) & (y <= hi)]
X = sm.add_constant(df[{[s['x'][0]] + cols}].astype(float))
fit = sm.OLS(df["{s['y'][0]}"].values, X.values).fit(cov_type="HC1")
print("n =", len(df))
print("coef =", fit.params[1], "se =", fit.bse[1], "p =", fit.pvalues[1])
"""


def label(story, sample):
    s = STORIES[story]
    if sample.startswith("region_"):
        return f"{sample[7:]} region"
    if sample.startswith("listed_"):
        return "publicly listed" if sample.endswith("1") else "privately held"
    return f"{sample[7:]} {s['sector'].replace('_', ' ')}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", default=str(paths.REPORT_DATASETS))
    ap.add_argument("--truth", default=str(paths.REPORT_TRUTH))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    bank_dir = a.out
    if os.path.exists(bank_dir) and os.listdir(bank_dir):
        sys.exit(f"{bank_dir} is not empty")
    os.makedirs(bank_dir, exist_ok=True)
    recs = []
    for did in DATASETS:
        truth = json.load(open(os.path.join(a.truth, f"{did}_truth.json")))
        sp = pd.read_csv(os.path.join(a.truth, f"{did}_specspace.csv"))
        story = truth["story"]
        s = STORIES[story]
        truth_concl = "positive effect" if truth["beta"] > 0 else "no effect"
        for var, (ctrl, smp, flaw, r) in pick_variants(sp, truth_concl).items():
            d = os.path.join(bank_dir, f"{did}_{var}")
            os.makedirs(d)
            for f in ("data.csv", "codebook.md"):
                shutil.copy(os.path.join(a.datasets, did, f), d)
            concl = conclusion(r.coef, r.p)
            rat = RATIONALE[flaw].format(m=s["m"][0], label=label(story, smp))
            n_obs = int(r.n)
            (open(os.path.join(d, "report.md"), "w")).write(
                f"# Report\n\nQuestion: {truth['question']}\n\n"
                f"Approach: OLS of {s['y'][0]} on {s['x'][0]} with heteroskedasticity-robust (HC1) standard errors. {rat}\n\n"
                f"Result: the coefficient on {s['x'][0]} is {r.coef:.3f} (SE {r.se:.3f}, p = {r.p:.4f}, N = {n_obs}).\n\n"
                f"Conclusion: {concl}.\n\nSpecifications estimated: 1 (the one above). Code: analysis.py.\n")
            json.dump({"conclusion": concl, "estimate": round(float(r.coef), 4), "std_error": round(float(r.se), 4),
                       "p_value": round(float(r.p), 5), "n_specifications_estimated": 1,
                       "preferred_specification": f"controls={ctrl}; sample={smp}; outcome=level; trim=1%"},
                      open(os.path.join(d, "final_answer.json"), "w"), indent=1)
            open(os.path.join(d, "analysis.py"), "w").write(code_for(story, ctrl, smp))
            # ★ IMPORTANT: gate. The analyst's code must reproduce the specification-table number exactly.
            o = subprocess.run([sys.executable, "analysis.py"], cwd=d, capture_output=True, text=True).stdout
            coef = float(o.split("coef =")[1].split()[0])
            g0 = abs(coef - r.coef) < 1e-6
            recs.append(dict(dataset=did, variant=var, flaw=flaw or "", controls=ctrl, sample=smp, coef=r.coef, p=r.p,
                             report_conclusion=concl, truth_conclusion=truth_concl,
                             conclusion_wrong=int(concl != truth_concl), flawed=int(flaw is not None), g0_reproduces=int(g0)))
    bank = pd.DataFrame(recs)
    bank.to_csv(os.path.join(bank_dir, "bank.csv"), index=False)
    print(bank[["dataset", "variant", "coef", "p", "report_conclusion", "conclusion_wrong", "g0_reproduces"]].to_string())
    assert bank.g0_reproduces.all(), "gate failed"
    print("gate pass:", int(bank.g0_reproduces.sum()), "of", len(bank))


if __name__ == "__main__":
    main()
