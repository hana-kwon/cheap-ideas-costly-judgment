# Report

Question: What is the effect of supplier diversification on export growth?

Approach: OLS of export_growth_2023 on supplier_diversity with heteroskedasticity-robust (HC1) standard errors. I report the simple regression of the outcome on the treatment, which is transparent and easy to interpret, after trimming the top and bottom 1% of the outcome.

Result: the coefficient on supplier_diversity is 1.543 (SE 0.234, p = 0.0000, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
