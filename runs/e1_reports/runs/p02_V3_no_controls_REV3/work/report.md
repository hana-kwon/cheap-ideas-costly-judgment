# Report

Question: What is the effect of remote work on engineering innovation?

Approach: OLS of patents_per_100_eng_2023 on remote_share with heteroskedasticity-robust (HC1) standard errors. I report the simple regression of the outcome on the treatment, which is transparent and easy to interpret, after trimming the top and bottom 1% of the outcome.

Result: the coefficient on remote_share is 2.066 (SE 0.231, p = 0.0000, N = 1960).

Conclusion: positive effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
