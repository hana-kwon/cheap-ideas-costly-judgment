# Report

Question: What is the effect of remote work on engineering innovation?

Approach: OLS of patents_per_100_eng_2023 on remote_share with heteroskedasticity-robust (HC1) standard errors. I control for firm size, firm age, the pre-period value of the outcome and collab_index_2023, which captures an important determinant of the outcome, and trim the top and bottom 1% of the outcome.

Result: the coefficient on remote_share is -1.950 (SE 0.226, p = 0.0000, N = 1960).

Conclusion: negative effect.

Specifications estimated: 1 (the one above). Code: analysis.py.
