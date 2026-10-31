import pandas as pd, numpy as np, statsmodels.formula.api as smf
import os
d=pd.read_csv(os.path.join(os.getcwd(),'data.csv'))
print(d.describe().T); print(d.isna().sum().sum())
pre="log_employees_2020+firm_age_2020+productivity_2020+C(region)+listed+C(sector)+export_share_2020+foreign_owned+family_owned+rd_intensity_2020+union_share_2020+credit_score_2020"
specs={"naive":"productivity_2023~training_hours",
"pre_controls":"productivity_2023~training_hours+"+pre,
"pre_controls_no_lagprod":"productivity_2023~training_hours+"+pre.replace("+productivity_2020",""),
"pre+mgmt(post-treatment)":"productivity_2023~training_hours+mgmt_rating_2023+"+pre,
"log_y pre":"np.log(productivity_2023)~training_hours+"+pre,
"quad pre":"productivity_2023~training_hours+I(training_hours**2)+"+pre,
"mgmt only":"productivity_2023~training_hours+mgmt_rating_2023"}
for k,f in specs.items():
    m=smf.ols(f,d).fit(cov_type='HC1')
    print(k,m.params['training_hours'],m.bse['training_hours'],m.pvalues['training_hours'],m.nobs)
m=smf.ols("training_hours~mgmt_rating_2023+"+pre,d).fit(); print(m.params['mgmt_rating_2023'],m.pvalues['mgmt_rating_2023'])
m=smf.ols("mgmt_rating_2023~training_hours+"+pre,d).fit(); print(m.params['training_hours'],m.pvalues['training_hours'])
m=smf.ols("training_hours~"+pre,d).fit(); print(m.summary().tables[1])
