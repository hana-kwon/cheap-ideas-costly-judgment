# ============================================================
# START DATE   : 2026-10-29
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 min
# DESCRIPTION  : Pre-specified analysis of E2 and E3 (preregistration/e2e3_prereg_en.md). H4: own analysis then
#                review versus review (report task, flawed reports with the right conclusion). H5: role panel
#                versus same-instruction panel, mean pairwise correlation of misses (both tasks), tested by
#                swapping the two panels' triples within items. Holm adjustment across the three tests.
# INPUT FILES  : <e1 ledger scores>/rows.csv, <e1 report scores>/verdicts.csv, <e2e3 scores>/{L_rows.csv,
#                R_verdicts.csv}
# OUTPUT FILES : <out>/e2e3_analysis.json
# USAGE        : python src/15_analyze_e2e3.py <dir with rows.csv> <dir with verdicts.csv> <dir with L_rows.csv
#                and R_verdicts.csv> <out dir>
# ============================================================
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.stats import holm, panel_swap_test, signflip  # noqa: E402


def main(e1L, e1R, e23, out):
    # task L
    l1 = pd.read_csv(f"{e1L}/rows.csv")
    l2 = pd.read_csv(f"{e23}/L_rows.csv")
    L = l1.merge(l2[["tag", "fmt", "row"] + [c for c in l2 if c.startswith(("det_ROLE", "ok_ROLE"))]], on=["tag", "fmt", "row"])
    S = L[L.cls == "seeded"]
    C = L[L.cls == "correct"]
    miss = lambda d, arms: 1 - d[[f"det_{a}" for a in arms]].values
    roles, same = ["ROLE1", "ROLE2", "ROLE3"], ["REV1", "REV2", "REV3"]
    # task R
    r1 = pd.read_csv(f"{e1R}/verdicts.csv")
    r2 = pd.read_csv(f"{e23}/R_verdicts.csv")
    R = r1.merge(r2[["dataset", "variant"] + [c for c in r2 if c.startswith("dec_")]], on=["dataset", "variant"])
    for a in same + roles + ["PTR1", "PTR2", "PTR3", "REPRO1", "REPRO2", "REPRO3"]:
        R[f"app_{a}"] = (R[f"dec_{a}"] == "approve").astype(int)
    R["app_REV"] = R[[f"app_{a}" for a in same]].mean(axis=1)
    R["app_PTR"] = R[["app_PTR1", "app_PTR2", "app_PTR3"]].mean(axis=1)
    F = R[R.flawed == 1]
    FR = F[F.conclusion_wrong == 0]
    conf = {
        "H4_REV_minus_PTR_false_approval_flawed_right_concl": signflip(FR.app_REV - FR.app_PTR, "H4"),
        "H5L_role_vs_same_rho_miss": panel_swap_test(miss(S, roles), miss(S, same), "H5L"),
        "H5R_role_vs_same_rho_approve_flawed": panel_swap_test(F[[f"app_{a}" for a in roles]].values,
                                                               F[[f"app_{a}" for a in same]].values, "H5R"),
    }
    adj = holm(conf)
    for k in conf:
        conf[k]["p_holm"] = adj[k]
    corr = R[R.flawed == 0]
    expl = {
        "R_false_approval_flawed": {a: round(F[f"app_{a}"].mean(), 4) for a in ["REV", "PTR"] + roles},
        "R_false_approval_flawed_right_concl": {a: round(FR[f"app_{a}"].mean(), 4) for a in ["REV", "PTR"] + roles},
        "R_false_approval_wrong_concl": {a: round(F[F.conclusion_wrong == 1][f"app_{a}"].mean(), 4) for a in ["REV", "PTR"] + roles},
        "R_false_rejection_correct": {a: round(1 - corr[f"app_{a}"].mean(), 4) for a in ["REV", "PTR"] + roles},
        "R_by_flaw_PTR_vs_REV": F.groupby("flaw")[["app_REV", "app_PTR"]].mean().round(3).to_dict(),
        "R_panel_any_majority_all_role": {k: round((F[[f"app_{a}" for a in roles]].sum(axis=1) >= n).mean(), 4)
                                          for k, n in (("any", 1), ("majority", 2), ("all", 3))},
        "L_pass_role": {a: round(1 - S[f"ok_{a}"].mean(), 4) for a in roles},
        "L_detect_role": {a: round(S[f"det_{a}"].mean(), 4) for a in roles},
        "L_false_alarm_role": {a: round(C[f"det_{a}"].mean(), 5) for a in roles},
        "L_panel_detect_any_role_vs_same": {"role": round((S[[f"det_{a}" for a in roles]].sum(axis=1) >= 1).mean(), 4),
                                            "same": round((S[[f"det_{a}" for a in same]].sum(axis=1) >= 1).mean(), 4)},
        "missing_R": {a: int((R[f"dec_{a}"].isna() | R[f"dec_{a}"].isin(["missing", ""])).sum()) for a in ["PTR1", "PTR2", "PTR3"] + roles},
    }
    res = dict(confirmatory=conf, exploratory=expl)
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(f"{out}/e2e3_analysis.json", "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:5])
