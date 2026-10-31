# Effect of supplier diversification on export growth

**Conclusion: positive effect (small).** Preferred estimate: a 1 SD increase in supplier diversity raises 2023 export growth by about 0.69 index points (SE 0.240, p = 0.0038, HC1 robust). The outcome has mean about 100.5.

## Approach
Cross-section of 2000 firms, with no missing data. I used OLS with robust (HC1) standard errors. The identification assumption is selection on observables, using the pre-period (2020) firm characteristics as controls. `buyer_rating_2023` is measured after the treatment (2021-22). It is likely a mediator or collider, because it correlates 0.54 with diversity and 0.56 with the outcome. I therefore excluded it from the preferred model. Adding it flips the sign, which is what you would expect from conditioning on a post-treatment variable.

## Specifications estimated (6)
Coefficients are on supplier_diversity.

1. Raw bivariate OLS: 2.553 (SE 0.246, p = 3e-25). Confounded; not preferred, because the larger, more established firms that have more suppliers also grow faster.
2. Core controls (log sales, years exporting, past export growth): 0.691 (SE 0.240, p = 0.004).
3. **Preferred.** All pre-period controls (core, region, listed, product group, inventory days, foreign owned, imported input share, port distance, ISO certification, debt ratio): 0.693 (SE 0.240, p = 0.0038).
4. Specification 3 plus post-treatment buyer_rating_2023: -2.121 (SE 0.233, p = 8e-20). Not preferred, because it conditions on a post-treatment variable and is biased.
5. Specification 3 with a diversity x product-group interaction: main effect 0.819 (SE 0.342, p = 0.017) for durables. The interaction is -0.246 (SE 0.444, p = 0.58), so there is no evidence of heterogeneity.
6. Specification 3 with a quadratic term: linear term 0.694 (p = 0.004), squared term 0.015 (p = 0.93). There is no evidence of nonlinearity.

## Caveats
The estimate is robust to the choice of pre-period controls (0.69 in specifications 2 and 3). It still relies on there being no unobserved confounding. The effect is modest in size.
