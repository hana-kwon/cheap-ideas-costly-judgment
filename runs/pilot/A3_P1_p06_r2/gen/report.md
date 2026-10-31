# Effect of supplier diversification on export growth

**Conclusion: no detectable effect.** This does not support the PI's hypothesis.

**Preferred estimate** (OLS, HC1 robust SEs, n=2000): a 1 SD increase in supplier_diversity changes export_growth_2023 by **0.051 index points, SE 0.247, p=0.836**. The 95% CI is about [-0.43, 0.54].

The preferred model controls for all pre-period covariates: log sales, years exporting, 2020 export growth, region, listed, product group, inventory days, foreign ownership, imported-input share, port distance, ISO certification and debt ratio.

## Specifications estimated (5)
All have the outcome export_growth_2023 and robust SEs.
1. Naive bivariate: 1.78 (SE 0.255), p<0.001. This is confounded, mainly by firm size and experience. Controls shrink it to about zero.
2. **Pre-period controls (preferred):** 0.051 (SE 0.247), p=0.836.
3. Same as 2, plus buyer_rating_2023: -2.41 (SE 0.228), p<1e-25. I rejected this one. The rating is measured in 2023, after the treatment, so it is probably an outcome of diversity or is jointly determined with export growth. Conditioning on it biases the estimate (diversity and rating correlate at 0.49).
4. Minimal controls (log sales, years exporting, 2020 growth): 0.057 (SE 0.246), p=0.817.
5. Specification 2 plus a squared diversity term, to test nonlinearity: the linear coefficient is 0.056 (SE 0.246), p=0.819. I did not examine the squared term separately.

## Caveats
- This is a cross-section. The identification relies on observed pre-period covariates, so unobserved confounding is still possible.
- The positive raw correlation (0.16) disappears once pre-period firm characteristics are controlled for.
- The result is not a proof of zero. The confidence interval excludes effects larger than about 0.5 points per SD, which is small next to an outcome SD of about 11.
