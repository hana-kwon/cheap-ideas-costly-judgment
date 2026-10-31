import pandas as pd, statsmodels.formula.api as smf
d=pd.read_csv('data.csv')
for f in ['export_growth_2023~supplier_diversity','export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020','export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020+buyer_rating_2023']:
    r=smf.ols(f,d).fit(cov_type='HC1');print(r.params['supplier_diversity'],r.bse['supplier_diversity'])
print(d[['supplier_diversity','buyer_rating_2023','export_growth_2023']].corr())
