import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('<run_root>/runs/pilot_261025/A1_P1_p01_r2/ver_r1_1/data.csv')
print(d.describe().T)
f="productivity_2023 ~ training_hours + log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
r=smf.ols(f,d).fit(cov_type='HC1');print(r.params['training_hours'],r.bse['training_hours'])
print(d.corr(numeric_only=True)['training_hours'])
for x in ['listed','export_share_2020','foreign_owned','family_owned','rd_intensity_2020','union_share_2020','credit_score_2020']:
    print(x, smf.ols(f"training_hours~{x}",d).fit().pvalues[x], smf.ols(f"productivity_2023~{x}+training_hours",d).fit().pvalues[x])
