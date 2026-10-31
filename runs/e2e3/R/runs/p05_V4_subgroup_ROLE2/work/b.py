import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c="log_engineers_2020+firm_age_2020+patents_per_100_eng_2020+listed+C(segment)+vc_backed+founder_ceo+cloud_spend_2020+hq_in_hub_city+share_phd_2020+gross_margin_2020"
m=smf.ols("patents_per_100_eng_2023 ~ remote_share*C(region)+"+c,df).fit(cov_type="HC1")
print(m.summary().tables[1])
print(m.wald_test("remote_share:C(region)[T.north]=0, remote_share:C(region)[T.south]=0",scalar=True))
for s in ["hardware","software"]:
    d=df[df.segment==s]
    r=smf.ols("patents_per_100_eng_2023 ~ remote_share+"+c.replace("+C(segment)",""),d).fit(cov_type="HC1")
    print(s,r.params['remote_share'],r.pvalues['remote_share'])
