import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
f="export_growth_2023 ~ supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
for c in ['region','product_group','listed']:
    for k,g in df.groupby(c):
        r=smf.ols(f,g).fit(cov_type="HC1");print(c,k,len(g),r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
