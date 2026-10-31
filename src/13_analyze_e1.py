# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 min
# DESCRIPTION  : Pre-specified analysis of experiment E1 (preregistration/e1_structures_prereg_en.md). Ledger
#                task: paired packet-level pass-rate contrasts and the dependence of reviewers' misses. Report
#                task: report-level false-approval contrasts and the dependence of reviewers' approvals. Holm
#                adjustment across the six confirmatory tests, then the exploratory summaries listed in the plan.
# INPUT FILES  : <ledger scores>/rows.csv (src/11), <report scores>/verdicts.csv (src/12)
# OUTPUT FILES : <out>/e1_analysis.json, printed tables
# USAGE        : python src/13_analyze_e1.py <dir with rows.csv> <dir with verdicts.csv> <out dir>
# ============================================================
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.stats import dependence, holm, signflip  # noqa: E402


def task_L(path):
    r = pd.read_csv(path)
    s = r[r.cls == "seeded"].copy()
    c = r[r.cls == "correct"].copy()
    for arm in ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO"]:
        s[f"pass_{arm}"] = 1 - s[f"ok_{arm}"]
        s[f"miss_{arm}"] = 1 - s[f"det_{arm}"]
    pk = s.groupby(["tag", "fmt"]).mean(numeric_only=True).reset_index()
    pk["unit"] = pk.tag + "_" + pk.fmt
    s["unit"] = s.tag + "_" + s.fmt
    res = {
        "H1L_REV1_minus_REPRO_pass": signflip(pk.pass_REV1 - pk.pass_REPRO, "H1L"),
        "H2L_dependence_REV123_miss": dependence(s, ["miss_REV1", "miss_REV2", "miss_REV3"], "unit", "H2L"),
        "H3L_REV1_minus_TGT_pass": signflip(pk.pass_REV1 - pk.pass_TGT, "H3L"),
    }
    expl = {"means_seeded": {a: dict(pass_=round(s[f"pass_{a}"].mean(), 4), detect=round(s[f"det_{a}"].mean(), 4))
                             for a in ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO"]},
            "false_alarm_correct_rows": {a: round(c[f"det_{a}"].mean(), 5) for a in ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO"]},
            "harm_correct_rows": {a: round(1 - c[f"ok_{a}"].mean(), 5) for a in ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO"]},
            "panel_detect_any_majority_all": {
                rule: round(((s[["det_REV1", "det_REV2", "det_REV3"]].sum(axis=1)) >= k).mean(), 4)
                for rule, k in (("any", 1), ("majority", 2), ("all", 3))},
            "mixed_dependence_REV1_REV2_REVH": dependence(s, ["miss_REV1", "miss_REV2", "miss_REVH"], "unit", "mixL"),
            "by_kind_pass": s.groupby("kind")[[f"pass_{a}" for a in ["REV1", "TGT", "REPRO"]]].mean().round(4).to_dict(),
            "by_fmt_pass": s.groupby("fmt")[[f"pass_{a}" for a in ["REV1", "TGT", "REPRO"]]].mean().round(4).to_dict()}
    return res, expl


def task_R(path):
    v = pd.read_csv(path)
    for a in ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO1", "REPRO2", "REPRO3", "CHK"]:
        v[f"app_{a}"] = (v[f"dec_{a}"] == "approve").astype(int)
    v["app_REPRO"] = v[["app_REPRO1", "app_REPRO2", "app_REPRO3"]].mean(axis=1)
    wrong = v[v.conclusion_wrong == 1]
    flawed = v[v.flawed == 1]
    correct = v[v.flawed == 0]
    res = {
        "H1R_REV1_minus_REPRO_false_approval_wrong_concl": signflip(wrong.app_REV1 - wrong.app_REPRO, "H1R"),
        "H2R_dependence_REV123_approve_flawed": dependence(flawed, ["app_REV1", "app_REV2", "app_REV3"], "dataset", "H2R"),
        "H3R_REV1_minus_TGT_false_approval_flawed": signflip(flawed.app_REV1 - flawed.app_TGT, "H3R"),
    }
    arms = ["REV1", "REV2", "REV3", "REVH", "TGT", "REPRO", "CHK"]
    expl = {"false_approval_flawed": {a: round(flawed[f"app_{a}"].mean(), 4) for a in arms},
            "false_approval_wrong_conclusion": {a: round(wrong[f"app_{a}"].mean(), 4) for a in arms},
            "false_approval_flawed_right_conclusion": {a: round(flawed[flawed.conclusion_wrong == 0][f"app_{a}"].mean(), 4) for a in arms},
            "false_rejection_correct": {a: round(1 - correct[f"app_{a}"].mean(), 4) for a in arms},
            "panel_approve_flawed_any_majority_all": {
                rule: round(((flawed[["app_REV1", "app_REV2", "app_REV3"]].sum(axis=1)) >= k).mean(), 4)
                for rule, k in (("any", 1), ("majority", 2), ("all", 3))},
            "by_flaw_false_approval": flawed.groupby("flaw")[[f"app_{a}" for a in arms]].mean().round(3).to_dict(),
            "missing_decisions": {a: int((v[f"dec_{a}"].isna() | (v[f"dec_{a}"] == "missing")).sum()) for a in arms if a != "REPRO"}}
    return res, expl


def main(l_run, r_run, out):
    os.makedirs(out, exist_ok=True)
    resL, explL = task_L(f"{l_run}/rows.csv")
    resR, explR = task_R(f"{r_run}/verdicts.csv")
    conf = {**resL, **resR}
    adj = holm(conf)
    for k in conf:
        conf[k]["p_holm"] = adj[k]
    res = dict(confirmatory=conf, exploratory_L=explL, exploratory_R=explR)
    json.dump(res, open(f"{out}/e1_analysis.json", "w"), indent=1, default=str)
    print(json.dumps(conf, indent=1))
    print(json.dumps({"L": explL["means_seeded"], "R_flawed": explR["false_approval_flawed"],
                      "R_wrong": explR["false_approval_wrong_conclusion"]}, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
