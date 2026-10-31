# Report

Question: What is the effect of supplier diversification on export growth?

Approach: OLS of export_growth_2023 on supplier_diversity with heteroskedasticity-robust (HC1) standard errors. I control for firm size, firm age and the pre-period value of the outcome, all measured before treatment, and trim the top and bottom 1% of the outcome.

Result: the coefficient on supplier_diversity is 0.053 (SE 0.233, p = 0.8191, N = 1960).

Conclusion: no effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
