# Report

Question: What is the effect of supplier diversification on export growth?

Approach: OLS of export_growth_2023 on supplier_diversity with heteroskedasticity-robust (HC1) standard errors. I control for firm size and firm age and trim the top and bottom 1% of the outcome.

Result: the coefficient on supplier_diversity is 0.106 (SE 0.232, p = 0.6486, N = 1960).

Conclusion: no effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
