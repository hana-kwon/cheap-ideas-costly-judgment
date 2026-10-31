import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
c="supplier_diversity+log_sales_2020+years_exporting_2020+export_growth_2020"
for v in ['listed','product_group','region','foreign_owned','certified_iso']:
    for g,d in df.groupby(v):
        m=smf.ols("export_growth_2023~"+c,d).fit(cov_type="HC1");print(v,g,len(d),round(m.params['supplier_diversity'],3),round(m.bse['supplier_diversity'],3))
print(df[['supplier_diversity','export_growth_2020','export_growth_2023','buyer_rating_2023']].corr())
m=smf.ols("export_growth_2023~supplier_diversity*C(region)+log_sales_2020+years_exporting_2020+export_growth_2020",df).fit(cov_type="HC1");print(m.summary().tables[1])
