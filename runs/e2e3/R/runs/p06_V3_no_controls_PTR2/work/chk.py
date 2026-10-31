import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
for f in ["export_growth_2023~supplier_diversity","export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"]:
    r=smf.ols(f,df).fit(cov_type="HC1");print(r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(df[['supplier_diversity','log_sales_2020','years_exporting_2020','export_growth_2020']].corr())
