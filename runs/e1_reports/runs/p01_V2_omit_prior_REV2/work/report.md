# Report

Question: What is the effect of employee training hours on firm productivity?

Approach: OLS of productivity_2023 on training_hours with heteroskedasticity-robust (HC1) standard errors. I control for firm size and firm age and trim the top and bottom 1% of the outcome.

Result: the coefficient on training_hours is 0.627 (SE 0.221, p = 0.0045, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
