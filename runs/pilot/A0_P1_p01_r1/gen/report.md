# Effect of training hours on productivity

**Conclusion: positive effect (modest).** Preferred estimate: +0.58 thousand USD value added per employee for each additional unit of training_hours. The training_hours variable is standardized, so one unit is about one SD. SE = 0.233 (HC1 robust), p = 0.0128, N = 2000.

**Preferred specification:** OLS of productivity_2023 on training_hours. Controls are all pre-period (2020) covariates: lagged productivity, log employees, age, export share, foreign/family ownership, R&D intensity, union share, credit score, listed, region and sector. Standard errors are HC1.

The naive estimate is more than four times larger (2.49) because training is correlated with firm characteristics that also raise productivity. I treat the controlled estimate as the more credible one. It is still observational, so unmeasured confounding remains possible.

I deliberately excluded mgmt_rating_2023 from the preferred model. It is measured in 2023, after training, and correlates 0.54 with training, so it is plausibly a mediator or collider. Conditioning on it flips the sign (-2.35). That is a bad-control artifact, not evidence of a negative effect.

## All specifications estimated (7 in total)
Estimates are for training_hours, in thousand USD per unit of training_hours.

| # | Specification | Estimate | SE | p |
|---|---|---|---|---|
| 1 | Naive: productivity_2023 ~ training | 2.488 | 0.241 | 4.8e-25 |
| 2 | + productivity_2020 only | 2.069 | 0.243 | 1.7e-17 |
| 3 | **Preferred: + all pre-period controls, region, sector** | **0.579** | **0.233** | **0.0128** |
| 4 | Same as 3 plus mgmt_rating_2023 (bad control, not preferred) | -2.347 | 0.229 | 1.0e-24 |
| 5 | Same as 3 without productivity_2020 | 0.709 | 0.233 | 0.0023 |
| 6 | Log(productivity_2023) outcome, controls as in 3 | 0.0061 (about 0.6% per unit) | 0.0023 | 0.0095 |
| 7 | Controls as in 3, with training x sector interaction | 0.781 (manufacturing); interaction with services -0.383 (p=0.38) | 0.321 | 0.015 |

The interaction in spec 7 gives no evidence that the effect differs by sector.
