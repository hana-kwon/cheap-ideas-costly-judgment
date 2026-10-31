# Preregistration 05: Experiment E1, the same evaluation structures on two tasks (2026-10-29)

English translation of the Korean original, prepared on 2026-10-31 for this repository. The original is the fixed record; its SHA-256 and the rule for checking the recorded body hash are in `preregistration/README.md`. Square brackets mark translator's notes, including places where a local folder path, a person, or an internal note was replaced by a description. Time stamps, hashes and file names are copied unchanged. The file names are those of the original scripts; `preregistration/README.md` maps them to files in `src/`.

> Written before any real call and fixed by the time and hashes in "Fixed record" below. Any change is only appended at the end as a change record.
> Approval: [the author's approval of 2026-10-29 to proceed; internal reference omitted]. [Target outlet note omitted.]
> What was seen before fixing: code tests with fake responses (the ledger task reused S1 responses; the report task used random decisions), and 2 test calls for the report task ([local smoke-test folder], excluded from analysis). The S1 ledger results and the exploratory calculation made after them (independent rewriting + comparison, 384/384) were already known. H1L is therefore a **reconfirmation** of that exploratory result, and the target fields of TGT (field checklist: dates and payment channels) were chosen by looking at the fields most often missed in S1.

## 1. Question

When producing work costs almost nothing, which evaluation structure (one reviewer, three same-model reviewers with an approval rule, a field checklist, independent reproduction followed by comparison) reduces errors that pass, and do same-model reviewers judge independently (the assumption of Sah and Stiglitz)?

## 2. Tasks and materials

- **Task L (ledgers):** the same 48 drafts as S1, the same seeded errors (8 percent of rows, 384 per batch), the same marks (FLAGGED). Scored against the answer key. Code `analysis/01_code/05_e1_taskL_ledger_261029.py`. Responses are read **from the start this time** with the content-based parser written for the S1 rescoring (`09_s1_rescore_v2_261028.py` [in the S1 project folder]).
- **Task R (research reports):** 6 datasets x 5 reports = 30 (`analysis/01_code/04_make_report_bank_261029.py`; gate G0 passed 30/30: each analysis script reproduces the estimate in the specification table). 1 correct + 4 flawed (control measured after treatment, omitted pre-period outcome, no controls, favorable subgroup). Of the 24 flawed reports, 12 also have a wrong conclusion. Code `06_e1_taskR_reports_261029.py`.
- Models: claude-sonnet-5-5 (main), claude-haiku-5-5 (smaller model), Claude Code CLI 2.0.43 (subscription plan). Report-task reviewers get the same instructions and tools as in the pilot (`02_run_orgs.py` VER_TASK; may run Python).

## 3. Evaluation structures (every item goes to every structure)

| Structure | Task L | Task R |
|---|---|---|
| REV1, REV2, REV3 | Sonnet reviews 3 times (unaware of each other): checks and corrects the draft | Sonnet reviews 3 times: approve/reject |
| REVH | One Haiku review | One Haiku review |
| TGT | Sonnet review + "first compare every row's date and payment channel with the documents" | Sonnet review + instruction to check "(1) controls measured after treatment (2) control for the pre-period outcome (3) full sample" |
| REPRO | Sonnet writes the ledger anew without the draft, then only rows that differ from the draft are selected mechanically, then Sonnet compares the two versions (unlabeled as to who wrote which) with the documents and decides | Sonnet analyzes the data anew without the report (3 times); approve the report if its conclusion equals the reanalysis conclusion |
| CHK | (none) | Deterministic checklist (no model): reject if a control is measured after treatment, the pre-period outcome is omitted, or the sample is a subset |

## 4. Outcomes

- Task L: **pass rate** = share of seeded-error rows whose transaction is wrong in that structure's final ledger. Detection rate = the row was edited or deleted (review) or selected as a disagreement (REPRO). False alarm = share of correct rows touched. Harm = share of correct rows wrong at the end.
- Task R: **false approval** = share of flawed reports approved (12 with a wrong conclusion / all 24 flawed). False rejection = share of the 6 correct reports rejected. If there is no verdict file, it is counted as "missing" (not approval) and the number is reported.
- Dependence: mean pairwise correlation rho of the miss indicators of REV1-3 on the same items (L: not detected, R: flawed report approved), effective number of independent reviewers n_eff = 3/(1+2 rho), and the share missed by all three divided by the product under independence.

## 5. Confirmatory hypotheses (6 tests, Holm adjustment, significance level 5 percent)

| | Task L (unit: 48 packets) | Task R |
|---|---|---|
| **H1 reproduction > review** | REV1 pass rate minus REPRO pass rate > 0 (paired difference, two-sided sign flip) | Among the 12 wrong-conclusion reports, REV1 approval minus REPRO approval (mean of 3) > 0 (two-sided sign flip) |
| **H2 same-model reviewers' judgments are not independent** | rho of REV1-3 misses > 0 (one-sided permutation test: item order shuffled separately for each reviewer, 5,000 times) | rho of REV1-3 approvals among the 24 flawed reports > 0 (same permutation test) |
| **H3 field checklist > review** | REV1 pass rate minus TGT pass rate > 0 (two-sided) | Among the 24 flawed reports, REV1 approval minus TGT approval > 0 (two-sided) |

- Results in the opposite direction are reported as they are. Bootstrap intervals (packet or dataset clusters) are descriptive. Analysis code `07_e1_analysis_261029.py` (tested on fake data: with random decisions, H2 permutation p = 0.13).

## 6. Exploratory (labeled as such)

Detection and false approval of the three reviewers by approval rule (any one / majority / all) · rho of Haiku alone and of a mixed panel (REV1, REV2, REVH) (diversity of judgment) · comparison with CHK · false alarms, harm, false rejection (the cost side) · by error type and document format · false approval of the 12 reports whose conclusion is right but whose method is wrong.

## 7. Execution rules and limits

- Calls: task L 48 x (3 REV + REVH + TGT + REPRO) + up to 48 resolution calls = at most 336, 3 at a time. Task R 30 x 5 + 18 reanalyses = 168, 3 at a time. Cap (cost reported by the CLI): task L $25, task R $30, total at most $60. If a cap is reached, stop and report the number missing.
- Failed calls are rerun once with `--resume`. Anything still missing is not filled in.
- Limits: two models (same developer). Task R has only 30 reports and 6 datasets, so its power is low. REPRO in task L has two stages (rewrite + resolution) and so more calls than one reviewer (the cost difference is reported as exploratory). No human evaluators.

## Fixed record

- Fixed at: 2026-10-29T00:38:16-0400
- `04_make_report_bank_261029.py` SHA-256 `bb00caa9cc7efa643ca36872355958befa064526e45581640c4edf795fa8e591`
- `05_e1_taskL_ledger_261029.py` SHA-256 `affbaaa3388bb0c51f6f125fbecc3f825192ab417e99d65422358b4b7d3d353b`
- `06_e1_taskR_reports_261029.py` SHA-256 `57aca93faa8cb13e90b92873c6514f2d0385e5577101afa959480a8834a91a69`
- `07_e1_analysis_261029.py` SHA-256 `99179950838a232da6bdf44a6bc45335835e25bbe56f3fec5a07342e89912063`
- `02_run_orgs.py` SHA-256 `e1d6eff17879e39f364832e4be025b734ee206ac9dd6a105dc7f05ae532f235c`
- `09_s1_ai_checker_261028.py` SHA-256 `59a1406b53d1abd2d688c8620b35943f3ba58a7e46a3f7c7a59bb6f9a8230318`
- `09_s1_rescore_v2_261028.py` SHA-256 `c3cffbbeaf26c3666fe0e88b1736e147f745af99839199baf4cfb8ce18ea0538`
- Report bank `bank.csv` SHA-256 `b4b8f9ce31f1d06e64de68444575e4494c78b2044e51303da9ee9a5febc39c97`
- Body of this document (up to the "Fixed record" section) SHA-256 `bce1d8ca256660573155fe5a4f529222d0490970536a07a3f5aa7faacff69e8a`

## Change record

- 2026-10-29T18:41:49-0400 **Subscription usage limit reached during the run (recorded before seeing results).** Between 01:02 and 01:06 the Claude Code CLI returned "Spending cap reached resets 3:30am", so 9 task-L calls (recorded as failures, no response) and 10 task-R calls (no verdict file, recorded by the code as "missing") were not processed. This was the subscription's usage limit, not the cap we set ($60) (CLI-reported cost up to that point: L $12.44, R $10.39). These 19 calls are infrastructure failures, not model judgments, so they are treated as the "failed calls" of section 7; the 10 task-R run folders were moved to `e1R_261029/failed_cap_261029/` (not deleted) [not included in this repository]. After the limit reset (2026-10-29 18:4x), both tasks are rerun once with `--resume`. The "missing" rule of section 4 applies only when the model did not write a verdict. The analysis is run after the rerun finishes.
- 2026-10-29T18:46:23-0400 Rerun finished (0 calls missing). Results and interpretation of the pre-specified analysis are in [the internal results record; the numbers are in `reference/e1/e1_analysis.json`]. Analysis code and hypotheses were used as fixed.
