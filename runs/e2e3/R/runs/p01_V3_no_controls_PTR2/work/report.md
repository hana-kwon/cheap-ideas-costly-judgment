# Report

Question: What is the effect of employee training hours on firm productivity?

Approach: OLS of productivity_2023 on training_hours with heteroskedasticity-robust (HC1) standard errors. I report the simple regression of the outcome on the treatment, which is transparent and easy to interpret, after trimming the top and bottom 1% of the outcome.

Result: the coefficient on training_hours is 2.165 (SE 0.225, p = 0.0000, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
