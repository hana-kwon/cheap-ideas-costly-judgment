import pandas as pd, numpy as np, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
for c in ['log_sales_2020','years_exporting_2020','export_growth_2020']:
    r=smf.ols("export_growth_2023 ~ supplier_diversity+"+c,df).fit(cov_type="HC1");print(c,r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
    print(' corr with sd',df[c].corr(df.supplier_diversity),' with y',df[c].corr(df.export_growth_2023))
f="export_growth_2023 ~ supplier_diversity+I(supplier_diversity**2)+log_sales_2020+years_exporting_2020+export_growth_2020"
r=smf.ols(f,df).fit(cov_type="HC1");print(r.summary().tables[1])
f="export_growth_2023 ~ supplier_diversity*log_sales_2020+supplier_diversity*export_growth_2020+years_exporting_2020"
r=smf.ols(f,df).fit(cov_type="HC1");print(r.summary().tables[1])
r=smf.quantreg("export_growth_2023 ~ supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020",df).fit();print(r.params['supplier_diversity'],r.pvalues['supplier_diversity'])
print(df.corr(numeric_only=True)['supplier_diversity'])
