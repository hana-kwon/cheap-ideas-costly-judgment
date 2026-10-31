import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("data.csv")
y = df["export_growth_2023"]
lo, hi = y.quantile([0.01, 0.99])
df = df[(y >= lo) & (y <= hi)]
X = sm.add_constant(df[['supplier_diversity', 'log_sales_2020', 'years_exporting_2020']].astype(float))
fit = sm.OLS(df["export_growth_2023"].values, X.values).fit(cov_type="HC1")
print("n =", len(df))
print("coef =", fit.params[1], "se =", fit.bse[1], "p =", fit.pvalues[1])
