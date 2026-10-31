import pandas as pd, statsmodels.formula.api as smf, numpy as np
pd.set_option('display.width',250)
d=pd.read_csv('data.csv')
print(d.corr(numeric_only=True).round(2).to_string())
print(smf.ols("buyer_rating_2023~supplier_diversity+export_growth_2023",d).fit().summary().tables[1])
print(smf.ols("buyer_rating_2023~supplier_diversity+export_growth_2023+log_sales_2020+years_exporting_2020+export_growth_2020",d).fit().summary().tables[1])
