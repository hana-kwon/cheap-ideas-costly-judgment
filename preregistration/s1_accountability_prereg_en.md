# Preregistration: Study S1, arrangement of an AI checker (2026-10-28)

English translation of the Korean original, prepared on 2026-10-31 for this repository. The original is the fixed record; its SHA-256 and the rule for checking the recorded body hash are in `preregistration/README.md`. Square brackets mark translator's notes, including places where a local folder path or an internal note was replaced by a description. Time stamps, hashes and file names are copied unchanged. The file names are those of the original scripts; `preregistration/README.md` maps them to files in `src/`.

> This document was written before any real model call and fixed by the time and hashes in "Fixed record" below. Any change after fixing is only appended at the end as a change record.
> The code was checked only with a fake model (mock) [results in a local test folder]. No real model response had been seen.

## 1. Question

Given the same AI draft and the same documents, does the rate at which an AI checker lets the draft's errors through change when only the arrangement of checking, approval and responsibility changes? This is not a substitute for a human experiment (which would need IRB review); it is a separate question about the case in which the checker is also an AI. [A sentence linking the study to a journal special issue is omitted.]

## 2. Materials (all existing files; nothing new is created)

- Drafts: the 48 ledger drafts that claude-sonnet-5-5 actually produced in the earlier drafting check ("V0", shipped set) (`06_v0_results_261025/shipped_drafts/responses/*_r0.csv`; in this repository `data/ledgers/drafts/`). 4 countries (KEN, NGA, IND, USA) x 3 workloads (40, 100, 160 transactions) x 2 versions (a, b) x 2 document formats (local source documents, standardized table).
- Error seeding: the v5 function (`seed` in `04_build_task_interface_261025_v5.py`) is used unchanged. One error in 8 percent of rows (account, amount digits, date, payment channel, or a duplicate receipt booked as its own row). Flags are fixed by design: half of the seeded errors and the same number of correct rows are flagged. This design was chosen after seeing the results of the earlier checks V0 and V0b (record of 10-25).
- Answer key: `01_packet_prototype_v3_261025/*_answer_key.csv` [in this repository `data/ledgers/packets/`].
- Model: claude-sonnet-5-5 through the Claude Code CLI (subscription plan), empty working folder, no tools, no settings files. Same call function as V0 (`real_model`).

## 3. Arrangements (each packet gets all five arrangements once; call order shuffled with a fixed seed)

| Arrangement | Instruction |
|---|---|
| A author | Writes the ledger directly from the documents without a draft and approves it under its own name |
| N check only | Checks and corrects the draft. No mention of approval or responsibility (control for interpretation) |
| B check and sign | Checks and corrects, then approves under its own name and is responsible for accuracy |
| C check, owner approves | Checks and corrects, then sends to the shop owner, who gives final approval |
| D agentic | Rows with high confidence are already confirmed by the AI (CONFIRMED); decides only the low-confidence rows (OPEN) and may reopen confirmed rows |

N, B and C see the same FLAGGED marks. D sees OPEN/CONFIRMED marks on the same rows. Full instructions are `BRIEF`, `AUTHOR`, `EDIT_FORMAT` and `ANSWERS` in `09_s1_ai_checker_261028.py`.
Checking arrangements return only the rows to change (EDIT, DELETE, ADD). Rows not listed stay as drafted. At the end the model answers three questions (who wrote it, who is responsible, who approved).

## 4. Outcomes (compared with the key per transaction, averaged per packet)

- A transaction is correct = exactly one final row touches its documents, and its document IDs, date, account, payment channel and amount are all correct.
- **Pass rate (pass_through):** share of seeded-error transactions still wrong at the end. Separately for flagged (pass_flagged) and unflagged (pass_unflagged).
- **Harm:** share of transactions correct in the draft that are wrong at the end.
- **Final error rate (final_error):** share of all transactions wrong at the end. Used for the comparison with A.
- Model errors already in the draft (natural errors) are counted separately and enter neither the pass rate nor harm.
- Unreadable response lines are not dropped but counted as bad_lines. Failed calls are not filled in; the number missing is reported.

## 5. Hypotheses (three confirmatory, Holm adjustment)

- **H1:** When the owner approves (C), more seeded errors pass than when the checker signs (B). Mean over packets of the C minus B pass-rate difference > 0.
- **H2:** When AI-confirmed rows exist (D), more unflagged errors pass than in B. Mean D minus B pass_unflagged > 0.
- **H3:** The result of checking a seeded draft (B) has a higher final error rate than writing the ledger directly (A). Mean B minus A final_error > 0. (We already know from V0 that ledgers the same model wrote directly were all correct. The new information in H3 is therefore how far B is above zero, and this is stated in the interpretation.)

Tests: paired differences per packet (48). Two-sided sign-flip permutation test (20,000 draws, fixed seed), packet bootstrap 95 percent interval (20,000 draws). Holm adjustment of the p-values of H1-H3, significance level 5 percent. Results in the opposite direction are reported as they are. Code: `09_s1_analysis_261028.py`.

## 6. Exploratory analyses (not confirmatory; labeled as such)

B minus N and C minus N pass rates (whether signing raises and owner approval lowers scrutiny) · D minus B pass rate for flagged errors and overall · C minus B and D minus B harm · H1 and H2 by document format (local, standardized) · distribution of the answers to the three questions (manipulation check: B should name "Me" as approver, C "The shop owner").

## 7. Execution rules

- 240 calls (48 x 5), 4 at a time. Failed calls are rerun once with `--resume`. Anything still missing is reported as missing.
- If the response format (CSV, ANSWERS line) cannot be read in the first few responses, only the parser is fixed, and the change and its time are appended below. Instructions, hypotheses and outcomes are not changed.
- Limits: the model that made the drafts and the checker are the same model. One model, one repetition. This is not an experiment on human accountability.

## Fixed record

(filled from command output at fixing)
- Fixed at: 2026-10-28T23:30:54-0400
- `09_s1_ai_checker_261028.py` SHA-256 `c1a28abec80cfbdd779a1c30ccc732c14c7e2acd66eaf2fdd8a2a28e60486d09`
- `09_s1_analysis_261028.py` SHA-256 `5cfc01e47eeafe65b7bba9c2a573ad387f93debf29dcc260ed3b8f71c7cf644c`
- `04_build_task_interface_261025_v5.py` SHA-256 `c6499b82a289f9c08a767f08c99cd60b244f872f45103aceadc101c4e085d0b0`
- `06_v0_ai_only_check_261025_v4.py` SHA-256 `567ceb579e5472972ea7e34f40e51536d9cf00eeea92b4b941f02368cc419210`
- Body of this document (up to the "Fixed record" section) SHA-256 `f7f47e741e092df49b05f8f4a8929356c8d8c2486e3a6ec200310dcb4511d624`

## Change record

- 2026-10-28T23:32:15-0400 Parser fix (rule in section 7). Looking only at the format of the first 10 responses (no scores computed), one response was found to send its header in the order `action,row,...`. `apply_edits` was changed to locate columns by header name. No change to instructions, hypotheses, outcomes or analysis code. After the fix, `09_s1_ai_checker_261028.py` SHA-256 `59a1406b53d1abd2d688c8620b35943f3ba58a7e46a3f7c7a59bb6f9a8230318`. No effect on calls in progress (scoring is done again after the calls finish).
- 2026-10-28T23:51:09-0400 **Results of the run, and a parser change made after seeing them.** All 240 calls answered (0 failures). Pre-specified analysis with the fixed parser (including the first fix): H1 C minus B pass rate -0.015 (95 percent CI -0.063 to 0.019, Holm p = 0.67), H2 D minus B unflagged pass rate +0.106 (CI 0.005 to 0.217, Holm p = 0.12), H3 B minus A final error rate +0.005 (CI 0.001 to 0.010, Holm p = 0.023). Result files: [local run folder; in this repository `runs/s1/` and `reference/s1/analysis_locked_parser.json`].
  - Inspection of unreadable lines showed that N and D often had edits discarded (a header without an `action` column, EDIT lines without a row number, lines with the action first and no header). Therefore, **after seeing the results**, all responses were rescored with a parser that recognizes fields by their content (`09_s1_rescore_v2_261028.py`, SHA-256 `c3cffbbeaf26c3666fe0e88b1736e147f745af99839199baf4cfb8ce18ea0538`). Responses, scoring rules and analysis code are unchanged.
  - Rescored results [in this repository `reference/s1/rescored/`]: H1 +0.003 (CI -0.019 to 0.025, Holm p = 0.88), H2 -0.016 (CI -0.043 to 0.004, Holm p = 0.76), H3 +0.0035 (CI 0.0011 to 0.0059, Holm p = 0.025). Pass rates N 4.5 percent, B 5.2 percent, C 5.5 percent, D 4.9 percent; final error rate of A 0.08 percent.
  - Judgment: the H2 "effect" under the fixed parser came from the parser discarding D's edits. Of the 80 seeded errors that still passed, 79 had document IDs that appear nowhere in the response, so they were genuinely missed. H3 points the same way under both parsers.
  - Exploratory: pass rate by error type: amount 0/384, account 3/576, date 49/384 (12.8 percent), payment channel 28/192 (14.6 percent). The duplicate-receipt error was never produced by the seed function and became an account error (no linked row was drawn). Pass rate by document format: local source documents 5.6 to 8.5 percent, standardized table 2.2 to 3.4 percent. Manipulation check: in B, 48/48 named "Me" as responsible and approver; in C, 48/48 named "The shop owner" as approver (responsibility "Shared" in 27).
