# Report

Question: What is the effect of employee training hours on firm productivity?

Approach: OLS of productivity_2023 on training_hours with heteroskedasticity-robust (HC1) standard errors. I focus on the north region subsample, where the data are most comparable, control for firm size, firm age and the pre-period value of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on training_hours is 0.218 (SE 0.408, p = 0.5934, N = 684).

Conclusion: no effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
