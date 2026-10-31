# Preregistration records

Each experiment was planned in a document written in Korean before its first model call. The plan was fixed by recording the time and the SHA-256 hashes of the plan body and of the run and analysis code; later changes were only appended as time-stamped change records. The files in this folder are English translations made on 2026-10-31 for this repository. They are translations, not the fixed records. Time stamps, hashes and file names are copied unchanged, and translator's notes are in square brackets (mostly where a local folder path, a person, or an internal note was replaced by a description).

| Experiment | Translation | Fixed at (EDT) | SHA-256 of the Korean original file (as of 2026-10-31) | Recorded body hash |
|---|---|---|---|---|
| S1 accountability | `s1_accountability_prereg_en.md` | 2026-10-28 23:30:54 | `566bd457cc2c0532c982508ee538b07fd15d13eb248f71a12a521e696039fca5` | `f7f47e741e092df49b05f8f4a8929356c8d8c2486e3a6ec200310dcb4511d624` |
| E1 structures | `e1_structures_prereg_en.md` | 2026-10-29 00:38:16 | `d1c41cd2e1ae123064ea80b58f7e617f323d2ee0932b6e820efad445f4530c67` | `bce1d8ca256660573155fe5a4f529222d0490970536a07a3f5aa7faacff69e8a` |
| E2 and E3 | `e2e3_prereg_en.md` | 2026-10-29 19:19:48 | `9fa4ceec111271e2e536bf05e74f9a8019af1c1318406d6ca267ef795d6cfa16` | `e55bc18adabb02e11c086f1d1d05f25f6a7aed42852de92bebd31c7daaef68c5` |
| Pilot (appendix A7) | not translated | 2026-10-25 12:09:53 | `41889b3dc1e9afbe9d1e23f64859d55ae7a9bdc18581352db45ab8336d83edce` | (whole-file hash recorded at 12:10:28) |

The whole-file hashes of S1, E1 and E2/E3 differ from their body hashes because the change records were appended after fixing. The recorded body hash is the SHA-256 of the bytes of the original file that precede the heading line `## 고정 기록` ("Fixed record"). On 2026-10-31 all three recorded body hashes were recomputed from the original files and matched, and every code hash listed in the three fixed records matched the original scripts. The Korean originals are not in this repository because they also contain internal notes; with them, anyone can repeat both checks.

## Original scripts and their files in this repository

The fixed records hash the original scripts. The repository versions keep the logic and the prompts of those scripts; they differ in file locations (arguments instead of fixed folders), in how modules are imported (shared code moved to `src/lib/`), in the model setting (a model string instead of a fixed name), and in comments. The test that they are equivalent is that `python run_all.py` reproduces every stored score and every analysis file byte for byte (see the main README).

| Original script (hash in a fixed record) | Repository file |
|---|---|
| `01_make_datasets.py` | `src/lib/report_data.py`, `src/01_make_report_datasets.py` |
| `04_make_report_bank_261029.py` | `src/02_make_report_bank.py` |
| `01_synthetic_bookkeeping_packet_261025_v3.py` | `src/lib/ledger_packets.py`, `src/03_make_ledger_packets.py` |
| `06_v0_ai_only_check_261025_v4.py` (drafting prompt, ledger parser) | `src/lib/ledger_task.py`, `src/04_draft_ledgers.py` |
| `04_build_task_interface_261025_v5.py` (`seed`) | `src/lib/ledger_task.py`, `src/05_seed_ledger_drafts.py` |
| `02_run_orgs.py` | `src/lib/report_prompts.py`, `src/lib/models.py`, `src/06_run_pilot.py` |
| `03_score.py` | `src/07_score_pilot.py` |
| `09_s1_ai_checker_261028.py` | `src/lib/s1_accountability.py`, `src/lib/ledger_task.py`, `src/08_run_s1.py` |
| `09_s1_rescore_v2_261028.py` | `src/lib/ledger_task.py` (`read_line`, `apply_edits_v2`), `src/09_rescore_s1.py` |
| `09_s1_analysis_261028.py` | `src/10_analyze_s1.py` |
| `05_e1_taskL_ledger_261029.py` | `src/11_run_e1_ledger.py` |
| `06_e1_taskR_reports_261029.py` | `src/12_run_e1_reports.py` |
| `07_e1_analysis_261029.py` | `src/lib/stats.py`, `src/13_analyze_e1.py` |
| `08_e2e3_261029.py` | `src/14_run_e2e3.py` |
| `09_e2e3_analysis_261029.py` | `src/lib/stats.py`, `src/15_analyze_e2e3.py` |
