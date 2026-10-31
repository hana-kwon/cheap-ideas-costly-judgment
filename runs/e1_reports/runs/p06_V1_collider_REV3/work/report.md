# Report

Question: What is the effect of supplier diversification on export growth?

Approach: OLS of export_growth_2023 on supplier_diversity with heteroskedasticity-robust (HC1) standard errors. I control for firm size, firm age, the pre-period value of the outcome and buyer_rating_2023, which captures an important determinant of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on supplier_diversity is -2.219 (SE 0.219, p = 0.0000, N = 1960).

Conclusion: negative effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
