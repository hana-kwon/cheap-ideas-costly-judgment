import pandas as pd, statsmodels.formula.api as smf
df=pd.read_csv("data.csv")
print(df.export_growth_2023.std(), df[['supplier_diversity','log_sales_2020','years_exporting_2020','export_growth_2020']].corr())
r=smf.ols("export_growth_2023~supplier_diversity+I(supplier_diversity**2)+log_sales_2020+years_exporting_2020+I(log_sales_2020**2)",df).fit(cov_type="HC1")
print(r.summary().tables[1])
r=smf.ols("export_growth_2023~supplier_diversity+log_sales_2020+years_exporting_2020",df).fit(cov_type="HC1")
print(r.summary().tables[1])
