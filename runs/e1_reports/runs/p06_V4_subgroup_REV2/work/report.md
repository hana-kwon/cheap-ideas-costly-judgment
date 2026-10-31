# Report

Question: What is the effect of supplier diversification on export growth?

Approach: OLS of export_growth_2023 on supplier_diversity with heteroskedasticity-robust (HC1) standard errors. I focus on the north region subsample, where the data are most comparable, control for firm size, firm age and the pre-period value of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on supplier_diversity is 0.543 (SE 0.382, p = 0.1545, N = 656).

Conclusion: no effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
