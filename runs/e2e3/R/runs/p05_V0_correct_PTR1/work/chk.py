import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
for d,n in [(df,'all')]:
    f=smf.ols("patents_per_100_eng_2023~remote_share+log_engineers_2020+firm_age_2020+patents_per_100_eng_2020",d).fit(cov_type="HC1")
    print(n,f.params['remote_share'],f.bse['remote_share'],f.pvalues['remote_share'])
