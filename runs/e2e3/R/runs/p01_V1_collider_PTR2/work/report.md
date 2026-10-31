# Report

Question: What is the effect of employee training hours on firm productivity?

Approach: OLS of productivity_2023 on training_hours with heteroskedasticity-robust (HC1) standard errors. I control for firm size, firm age, the pre-period value of the outcome and mgmt_rating_2023, which captures an important determinant of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on training_hours is -2.142 (SE 0.221, p = 0.0000, N = 1960).

Conclusion: negative effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
