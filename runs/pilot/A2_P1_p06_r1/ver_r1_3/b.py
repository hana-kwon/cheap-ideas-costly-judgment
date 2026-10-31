import sys, traceback
f=open('out.txt','w')
try:
    import pandas as pd, numpy as np, statsmodels.formula.api as smf
    d=pd.read_csv('data.csv')
    pre="log_sales_2020+years_exporting_2020+export_growth_2020+C(region)+listed+C(product_group)+inventory_days_2020+foreign_owned+share_imported_inputs_2020+port_distance_km+certified_iso+debt_ratio_2020"
    m=smf.ols('export_growth_2023~supplier_diversity+I(supplier_diversity**2)+'+pre,d).fit(cov_type='HC1')
    print(m.summary().tables[1],file=f,flush=True)
    d['q']=pd.qcut(d.supplier_diversity,5,labels=False)
    m=smf.ols('export_growth_2023~C(q)+'+pre,d).fit(cov_type='HC1');print(m.params[:5],m.pvalues[:5],file=f,flush=True)
    for v in ['region','product_group','listed','foreign_owned','certified_iso']:
        m=smf.ols('export_growth_2023~supplier_diversity*C(%s)+'%v+pre,d).fit(cov_type='HC1')
        print(v,m.params.filter(like='supplier_diversity').round(2).to_dict(),m.pvalues.filter(like=':').round(3).to_dict(),file=f,flush=True)
    print(d.supplier_diversity.describe(),file=f,flush=True)
except Exception:
    traceback.print_exc(file=f)
f.close()
