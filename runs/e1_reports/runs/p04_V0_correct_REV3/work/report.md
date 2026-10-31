# Report

Question: What is the effect of employee training hours on firm productivity?

Approach: OLS of productivity_2023 on training_hours with heteroskedasticity-robust (HC1) standard errors. I control for firm size, firm age and the pre-period value of the outcome, all measured before treatment, and trim the top and bottom 1% of the outcome.

Result: the coefficient on training_hours is 0.904 (SE 0.227, p = 0.0001, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
