# Effect of training hours on productivity

**Data:** 2000 firms, cross-section, no missing values. training_hours is standardized (mean 0). Outcome is 2023 value added per employee (thousand USD). All standard errors are HC1 robust.

**Preferred specification (#4):** OLS of productivity_2023 on training_hours. Controls are all 2020 pre-period covariates (log employees, age, productivity_2020, export share, foreign, family, R&D, union share, credit score, listed) plus region and sector.
- Estimate: **0.579** thousand USD per +1 unit of training_hours (about 1 SD, if training_hours has unit variance; I did not check this)
- SE: 0.233
- p = 0.0128
- Conclusion: positive effect, but modest.

**Why this one:** The naive estimate (2.49) falls by about 77% once pre-period firm characteristics are controlled for. This is strong evidence that selection or confounding drives most of the raw association. Controlling for 2020 productivity and the other 2020 characteristics is appropriate because they are measured before training. The estimate is still only as good as the selection-on-observables assumption, so unobserved confounding could remain. The result is causal only under that assumption.

**mgmt_rating_2023:** I excluded it from the preferred model. It is measured in 2023, after training, so it is a potential mediator or collider. Controlling for it flips the sign to -2.35, which is the kind of bias that conditioning on a post-treatment variable produces. I do not interpret that estimate causally.

## All specifications estimated (7)
| # | Specification | Estimate | SE | p |
|---|---|---|---|---|
| 1 | Naive: productivity_2023 ~ training | 2.488 | 0.241 | 4.8e-25 |
| 2 | + productivity_2020 | 2.069 | 0.243 | 1.7e-17 |
| 3 | + all 2020 pre-controls | 0.606 | 0.235 | 0.0098 |
| 4 | + region, sector (**preferred**) | 0.579 | 0.233 | 0.0128 |
| 5 | #4 + mgmt_rating_2023 (post-treatment; not preferred) | -2.347 | 0.229 | 1.0e-24 |
| 6 | log(productivity) outcome, same controls as #4 | 0.0061 (about 0.6% per unit) | 0.0023 | 0.0095 |
| 7 | #4 + quadratic training term (linear coefficient; the quadratic term was not examined) | 0.580 | 0.233 | 0.0127 |

Specifications 3, 4, 6 and 7 agree on a small positive effect. The large raw association in specs 1 and 2 overstates it, and spec 5 is distorted by conditioning on a post-treatment variable.
