# Preregistration 07: E2 (own analysis, then review) and E3 (panel with different roles) (2026-10-29)

English translation of the Korean original, prepared on 2026-10-31 for this repository. The original is the fixed record; its SHA-256 and the rule for checking the recorded body hash are in `preregistration/README.md`. Square brackets mark translator's notes, including places where a local folder path, a person, or an internal note was replaced by a description. Time stamps, hashes and file names are copied unchanged. The file names are those of the original scripts; `preregistration/README.md` maps them to files in `src/`.

> Written before any real call and fixed by the time and hashes below. Approval: [the author's approval of 2026-10-29; internal reference omitted]. Cap: $60 together with E1 (E1 used $24.11, so $35 for this run).
> What was seen before fixing: all E1 results [internal results record]. The analysis code was tested with fake random decisions. The directions of the hypotheses were therefore set after seeing E1.

## 1. Questions

- **E2:** With the same model and the same information, does **reviewing someone else's report directly** differ from **reviewing it after first analyzing the data independently** (produce-then-review, PTR) in how well method errors are caught? In E1, reproduction + conclusion comparison passed 100 percent of the reports whose conclusion is right but whose method is wrong, and direct review passed 58 to 67 percent. PTR widens the unit of comparison from the conclusion to the whole analysis.
- **E3:** Do three same-model reviewers given only different roles in their instructions overlap less in their judgments (does the effective number of independent reviewers rise) than three reviewers with the same instruction (E1, rho 0.85 and 0.94)?

## 2. Materials and structures

- Model claude-sonnet-5-5 only (CLI 2.0.43, subscription plan). Task R report bank of 30 (`bank.csv` hash in the fixed record of preregistration 05), task L drafts of 48 (same as E1).
- **PTR1-3 (task R):** E1's independent reanalyses REPRO1-3 (analyses of the same data made without seeing the report: code, report, conclusion) are given as `own_*` files, and the model reviews the analyst's report. Instruction and tools are the same as E1 review, plus only the sentence "compare with your own earlier analysis" (`08_e2e3_261029.py` PTR_TASK). 30 reports x 3 = 90 calls.
- **ROLE1-3 (both tasks):** E1 review instruction + one sentence of role. Task R: methodologist (controls, timing of measurement, sample) / replicator (rerun the code, alternative specifications) / skeptic (assume there is a problem). Task L: row first (compare every field of each row with its document) / error hunt (assume several errors) / documents first (check the ledger in document order). Task R 30 x 3 = 90 calls, task L 48 x 3 = 144 calls.
- The comparison is E1's REV1-3 (same model, same base instruction). That the times differ (E1 ran on 10-29 00:38-01:06 and 18:4x) is stated as a limit.

## 3. Confirmatory hypotheses (Holm over 3, 5 percent)

- **H4 (E2):** Among the 12 reports whose conclusion is right but whose method is wrong, the per-report approval rate REV (mean of E1 REV1-3) minus PTR (mean of PTR1-3) > 0. Two-sided sign flip (report as unit).
- **H5L (E3, ledgers):** Among the 384 seeded errors, the mean pairwise correlation of ROLE1-3 misses < that of REV1-3. Permutation test that swaps the two panels' three judgments as a block for each item (5,000 times), two-sided.
- **H5R (E3, reports):** Among the 24 flawed reports, the correlation of ROLE1-3 approvals < that of REV1-3. Same test.

## 4. Exploratory (labeled as such)

False approval of PTR and of each ROLE (24 flawed / 12 wrong conclusion / 12 right conclusion) · false rejection of correct reports (cost) · PTR versus REV by flaw type · role panel by rule (any / majority / all) · ledger pass rate, detection and false alarms by role · "any one" detection of the role panel versus the same-instruction panel.

## 5. Execution rules

- 3 at a time, cap $35. Calls blocked by the subscription limit ("Spending cap reached") are recorded as failures (`failed_cap`), not as decisions, and rerun once with `--resume` after the limit resets. Only cases where the model did not write a verdict file count as "missing" (not approval).
- Code: `08_e2e3_261029.py` (run and scoring), `09_e2e3_analysis_261029.py` (analysis). Task L parsing uses the same content-based parser as E1.
- Limits: the 3 role instructions are used for the first time here and other role combinations are not tested. Comparison with people uses published results only (NeurIPS consistency experiment; Skitka 2000) [internal reference omitted].

## Fixed record

- Fixed at: 2026-10-29T19:19:48-0400
- `08_e2e3_261029.py` SHA-256 `e2413fae6ac4cdbbe1849820283f0374e6403d06475bd07d9308d667302e97a2`
- `09_e2e3_analysis_261029.py` SHA-256 `c29563205e8682f0afed6c5f4286481f131340ea58aa834353cf06ec5e33ebd3`
- `07_e1_analysis_261029.py` SHA-256 `99179950838a232da6bdf44a6bc45335835e25bbe56f3fec5a07342e89912063`
- `05_e1_taskL_ledger_261029.py` SHA-256 `affbaaa3388bb0c51f6f125fbecc3f825192ab417e99d65422358b4b7d3d353b`
- `06_e1_taskR_reports_261029.py` SHA-256 `57aca93faa8cb13e90b92873c6514f2d0385e5577101afa959480a8834a91a69`
- `02_run_orgs.py` SHA-256 `e1d6eff17879e39f364832e4be025b734ee206ac9dd6a105dc7f05ae532f235c`
- Body of this document SHA-256 `e55bc18adabb02e11c086f1d1d05f25f6a7aed42852de92bebd31c7daaef68c5`

## Change record

- 2026-10-29T19:48:06-0400 Around 19:43 the subscription limit ("Spending cap reached resets 10:10pm") made later calls fail (200/324 processed by then, $10.33). Per section 5 they stay recorded as failures, not decisions, and from 22:13 only the missing calls are rerun with `--resume`. If the limit is hit again during the rerun, the run continues the same way up to 3 more times at 30-minute intervals (a limit failure is not a model judgment). The analysis is run with the fixed `09_e2e3_analysis_261029.py` after all calls finish. Results have not been seen yet.
- 2026-10-29T21:10:41-0400 Rerun finished (0 verdicts missing); fixed analysis run. Results and interpretation in [the internal results record; the numbers are in `reference/e2e3/e2e3_analysis.json`].
