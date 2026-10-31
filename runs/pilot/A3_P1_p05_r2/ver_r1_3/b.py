import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
c="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+C(region)+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
for f in ["patents_per_100_eng_2023~remote_share","patents_per_100_eng_2023~remote_share+"+c,"patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020"]:
    r=smf.ols(f,d).fit(cov_type='HC1');print(r.params['remote_share'],r.bse['remote_share'],r.pvalues['remote_share'])
print(smf.ols("remote_share~"+c,d).fit().summary())
print(smf.ols("patents_per_100_eng_2023~remote_share+"+c,d).fit(cov_type='HC1').summary())
print(d.corr(numeric_only=True).round(2))
