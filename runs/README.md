# Stored model outputs

Every model call behind the proposal and appendix, as recorded during the runs. `run_all.py` rescores these files without calling any model. All calls used Claude Code CLI 2.0.43 with claude-sonnet-5-5 as the main model and claude-haiku-5-5 as the smaller model. Text calls ran in an empty folder with no tools and no settings files; report-task sessions ran in a folder holding only the files listed below. The CLI also makes small auxiliary calls on other models (for example to name a session); `calls.jsonl` and the transcripts record tokens per model, and the answers came from the model named in each record.

| Folder | Experiment | Contents |
|---|---|---|
| `pilot/` | Pilot (appendix A7) | `ledger.jsonl` (48 organizations: analyst answer, reviewer verdicts, approval outcome); per organization the analyst folder `gen/` and reviewer folders `ver_r1_k/` with every file the models wrote, `_fits.jsonl` (every regression fit, logged by `src/instrument/sitecustomize.py`), and full transcripts `*_transcript.jsonl` |
| `s1/` | S1 accountability (ledgers) | `responses/` (240: 48 packets x arrangements A, N, B, C, D), `calls.jsonl` (240, with prompt SHA-256 and token use), `seeded/` (the 48 seeded drafts), `packet_scores.csv` and `error_scores.csv` (scored with the parser fixed in the plan) |
| `e1_ledger/` | E1, ledger task | `responses/` (336: REV1-3, REVH, TGT and REPRO for 48 packets, plus 48 RESOLVE answers of the reproduction structure), `calls.jsonl` (336), `rows.csv` (one row per packet row and structure: detected, correct at the end) |
| `e1_reports/` | E1, report task | `runs/<dataset>_<report>_<structure>/` (168 sessions: 150 reviews and 18 independent reanalyses `*_data_REPRO1-3`) with `transcript.jsonl`, `work/` (every file the model read or wrote, except the data file), `done.json`; `calls.jsonl` (178 lines); `verdicts.csv` |
| `e2e3/` | E2 and E3 | `R/runs/` (180 report sessions: PTR1-3 and ROLE1-3), `L/responses/` (144 ledger reviews: ROLE1-3), `calls.jsonl` (332 lines), `R_verdicts.csv`, `L_rows.csv` |

## Calls blocked by a usage limit

A subscription usage limit blocked some calls. They returned no judgment, are not model decisions, and were rerun once after the limit reset; none was missing after the reruns (see the change records in `preregistration/`).

- E1 ledger task: 9 calls failed before writing a response; they left no file and no `calls.jsonl` line. The responses present are the reruns.
- E1 report task: 10 sessions ended without a verdict. Their lines remain in `calls.jsonl` with outcome "missing" (hence 178 lines for 168 sessions); their folders were set aside during the run and are not included. The folders present are the reruns.
- E2 and E3: 8 sessions were recorded as `failed_cap` in `calls.jsonl` (hence 332 lines for 324 calls); the reruns replaced their folders.

## What was left out, and changes made when copying

- Test runs made before each experiment (code checks with fake responses and a few trial calls) are not included; they were excluded from all analyses by the plans.
- The copies of `data.csv` inside the pilot folders (132 files) were removed; each was checked to be byte-identical to `data/reports/datasets/<id>/data.csv`. In E1, E2 and E3 the runner itself deleted the data file after each session.
- Local paths were replaced in every copied text file by the literal substitutions in `config/transcript_substitutions.json` (applied by `tools/scrub_copy.py`; counts per folder in `substitution_log_*.json`): the run folder on the original machine became `<run_root>`, its home folder `<home>`, and its user name `<user>`. No other text was changed. Some transcripts contain made-up paths such as `/Users/<name>/Desktop/...` that a model wrote while reasoning; these are model text and were left as they are.
