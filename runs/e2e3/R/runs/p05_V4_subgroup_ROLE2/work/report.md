# Report

Question: What is the effect of remote work on engineering innovation?

Approach: OLS of patents_per_100_eng_2023 on remote_share with heteroskedasticity-robust (HC1) standard errors. I focus on the central region subsample, where the data are most comparable, control for firm size, firm age and the pre-period value of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on remote_share is 0.122 (SE 0.383, p = 0.7507, N = 661).

Conclusion: no effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
