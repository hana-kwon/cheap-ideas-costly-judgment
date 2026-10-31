# Report

Question: What is the effect of remote work on engineering innovation?

Approach: OLS of patents_per_100_eng_2023 on remote_share with heteroskedasticity-robust (HC1) standard errors. I control for firm size and firm age and trim the top and bottom 1% of the outcome.

Result: the coefficient on remote_share is 0.730 (SE 0.222, p = 0.0010, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
