import pandas as pd, statsmodels.api as sm
df=pd.read_csv("data.csv")
pre=['log_sales_2020','years_exporting_2020','export_growth_2020','inventory_days_2020','foreign_owned','share_imported_inputs_2020','port_distance_km','certified_iso','debt_ratio_2020','listed']
def f(c,d=df):
    X=sm.add_constant(d[['supplier_diversity']+c].astype(float));r=sm.OLS(d.export_growth_2023,X).fit(cov_type="HC1");print(c[-2:],r.params['supplier_diversity'],r.bse['supplier_diversity'])
f([]);f(pre);f(pre+['buyer_rating_2023']);f(['buyer_rating_2023'])
print(df[['supplier_diversity','buyer_rating_2023','export_growth_2023']].corr())
print(sm.OLS(df.buyer_rating_2023,sm.add_constant(df[['supplier_diversity']])).fit().params)
