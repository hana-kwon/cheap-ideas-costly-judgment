# Cheap Ideas, Costly Judgment: a test bed for organizing AI evaluation

This repository is the research artifact for the proposal "Cheap Ideas, Costly Judgment: Organizing Evaluation in AI-Enabled Science." It is a working test bed in which every error is planted by code and scored against a key, so evaluation structures can be compared on the same items: one AI review, several AI reviews combined by a voting rule, a review with a checklist, independent reproduction followed by comparison, a fixed rule list, own analysis before review, and panels with different role instructions.

It contains two tasks with known answers, the code that generates them, the prompts of every structure, every model transcript and decision from the reference experiments, the preregistered analysis code, and the plans with their time stamps and hashes. All data are synthetic, so everything can be shared and rerun.

The prototype shows three results (proposal, Section 3). Three reviewers built from the same model behave almost as one: the mean correlation of their misses is 0.85 on ledgers and 0.94 on reports, or 1.11 and 1.04 effective independent reviewers out of three. Independent reproduction followed by row-by-row comparison lets 0.26 percent of planted ledger errors through, against 5.2 percent for a single review. In the report task, where reproduction compares only conclusions, it approves every report that reaches the right conclusion by a wrong method, while reviewers approve 61 percent of them.

## Quick start

Requirements: Python 3.9 to 3.11 (tested with 3.9.6 and 3.11) and the packages in `requirements.txt` (no model access is needed for the default run).

```
pip install -r requirements.txt
python run_all.py
```

This takes about one and a half minutes on a laptop CPU and calls no model. It:

1. rebuilds the synthetic report datasets, the report bank, the ledger packets and the seeded drafts from their seeds and checks that they are byte-identical to `data/`;
2. rescores the stored responses in `runs/` (pilot, S1, E1, E2 and E3) and checks the scores against the stored scores;
3. reruns the preregistered analyses and checks every result file against `reference/`;
4. redraws the two proposal figures and recomputes each number cited in the proposal and appendix (`config/proposal_numbers.csv`).

Results go to `outputs/run_<time>/`, including `comparisons.json` (which checks passed), `proposal_numbers_check.csv` (stated and recomputed value of each cited number) and `receipt.json` (SHA-256 of every input and output, package versions, step times). The script refuses to write into a non-empty folder. `--skip-generators` skips step 1.

To also send a small slice of items to a model of your choice and set its answers next to the stored decisions:

```
python run_all.py --live --model claude-cli:claude-haiku-5-5 --n-ledger 2 --n-reports 2
```

## Results of the reference run

The numbers below are in `reference/`, which holds the analysis outputs of the reference experiments; `run_all.py` reproduces each of these files byte for byte from `runs/` and `data/`. Percentages of the ledger task are shares of the 384 planted errors.

| Quantity | Value | File and key |
|---|---|---|
| Miss correlation of three same-model reviewers, ledgers / reports | 0.85 / 0.94 | `reference/e1/e1_analysis.json`, `H2L_...`, `H2R_...` (`rho`) |
| Effective independent reviewers among three, ledgers / reports | 1.11 / 1.04 | same, `n_eff` |
| All three reviewers missed / expected if independent | 3.6 / 0.01 percent | `H2L_...` (`p_all_miss`, `p_indep`) |
| Detected by any of three reviewers / by one reviewer | 96.4 / 94.8 percent | `exploratory_L` |
| Planted errors left after one review / checklist review / reproduction | 5.2 / 3.4 / 0.26 percent | `exploratory_L.means_seeded` |
| Reproduction minus review, packet mean (95 percent interval; Holm p) | 4.5 points (2.5 to 6.8; 0.0006) | `H1L_REV1_minus_REPRO_pass` |
| Planted errors flagged by reproduction; left wrong; correct rows changed | 384 of 384; 1; 0 of 4,415 | `runs/e1_ledger/rows.csv` |
| Reports with a wrong conclusion approved by any structure | 0 of 12 | `exploratory_R` |
| Method-flawed reports approved: review / smaller model / checklist / own analysis first / reproduction / rule list | 61 / 8 / 8 / 42 / 100 / 0 percent | `reference/e2e3/e2e3_analysis.json`, `reference/e1/e1_analysis.json` |
| Correct reports rejected: checklist / smaller model | 2 of 6 / 6 of 6 | `exploratory_R.false_rejection_correct` |
| Own analysis first, change in approval (95 percent interval; Holm p) | 61 to 42 percent (3 to 39 points; 0.38) | `H4_...` |
| Effective reviewers with role instructions, ledgers / reports | 1.21 / 1.15 | `H5L_...`, `H5R_...` |
| Effective reviewers, two same-model reviewers plus the smaller model (ledgers) | 1.55 | `mixed_dependence_REV1_REV2_REVH` |
| S1: pass rates when checking only / signing / owner approves / rows preconfirmed | 4.5 / 5.2 / 5.5 / 4.9 percent | `reference/s1/rescored/analysis.json` |
| Pilot: false discoveries / missed effects / reviewer approvals | 0 of 16 / 0 of 32 / 84 of 84 | `reference/pilot/runs_scored.csv` |
| Model calls in E1, E2 and E3 | 846 | `runs/*/calls.jsonl` |

Figures 1 and 2 of the proposal are `reference/figures/figure_1.png` and `figure_2.png`, with the plotted values in `figure_1_data.csv` and `figure_2_data.csv`. In the reference environment (Python 3.9.6, matplotlib 3.9.4, Calibri installed) the redrawn PNG files are byte-identical. Elsewhere the image bytes can differ with the font and rendering library (under Python 3.11 with the same pinned packages they did), but the plotted values in the data files are identical; without Calibri a fallback font is used.

All 51 numbers listed in `config/proposal_numbers.csv` reproduce as printed in the proposal, summary and appendix. For example, the share of planted ledger errors that all three reviewers missed is 14 of 384, printed as 3.6 percent in the documents and in the Figure 1b label.

## The two tasks

The ledger task gives a model the source documents of a small retail shop for one month (Kenya, Nigeria, India or the United States; 40, 100 or 160 transactions; local informal documents or a standardized table) and an AI-drafted ledger in which one error was planted in 8 percent of rows (account, amount digits, date, or payment channel). Half of the planted errors and an equal number of correct rows carry a FLAGGED mark. A transaction is correct when exactly one final row records its documents and its date, account, channel and amount match the key. The 48 packets hold 4,800 transactions, 384 of them with planted errors.

The report task gives a model an analyst's report on a synthetic dataset of 2,000 firms with a planted effect, together with the data, codebook, final answer and analysis script, and asks whether the conclusion is supported well enough to be released. For each of six datasets there is one correct report and four with a planted flaw: a control measured after treatment, an omitted pre-period outcome, no controls, or a favorable subgroup reported alone. Twelve of the 24 flawed reports reach a wrong conclusion. Reviewers can run Python in a folder that holds only these files; answer keys are kept outside it.

## Repository layout

```
run_all.py                 stored-output reproduction (default) and optional live slice
config/                    pilot design, cited numbers with their formulas, transcript substitutions
data/                      synthetic inputs and the AI drafts (data/README.md, inputs_manifest.json)
runs/                      every stored model response, transcript and decision (runs/README.md)
reference/                 analysis outputs and figures of the reference experiments
preregistration/           English translations of the plans, with hashes (preregistration/README.md)
src/01-05                  generators: report datasets, report bank, ledger packets, AI drafts, seeding
src/06-07                  pilot runner and scorer
src/08-10                  S1 accountability experiment: runner, rescoring, analysis
src/11-13                  E1 evaluation structures: ledger runner, report runner, analysis
src/14-15                  E2 and E3: runner, analysis
src/16-18                  figures, cited-number check, live slice
src/lib/                   shared code: model interface, tasks, prompts, test statistics
src/instrument/            logs every regression fit a model runs (pilot)
tools/scrub_copy.py        the copy step that removed local paths from stored outputs
```

Every script in `src/` starts with a header that names its inputs and outputs and can be run on its own; `run_all.py` shows the order and arguments.

## Rerunning experiments with a model

Each runner takes model strings of the form `provider:name`:

- `claude-cli:claude-sonnet-5-5` uses the Claude Code command-line client with the same flags as the reference runs (a bare model name means this provider);
- `anthropic:<model>` uses the Anthropic Messages API (key in `ANTHROPIC_API_KEY`);
- `openai:<model>` uses any OpenAI-compatible chat endpoint, including open-weight models served locally by vLLM, Ollama, LM Studio or llama.cpp (`OPENAI_BASE_URL`, for example `http://localhost:11434/v1`, and `OPENAI_API_KEY`, any string for a local server);
- `mock:any` returns fixed stand-in answers for pipeline tests.

For the report task, the API providers get four tools that mirror what the command-line reviewers could do: list files, read a file, write a file, and run a Python script, all inside the working folder (`src/lib/models.py`).

Examples (each writes a new run folder; compare it with the stored one by pointing the scoring and analysis steps at it):

```
python src/11_run_e1_ledger.py  --out outputs/e1_ledger_new  --model-main openai:qwen2.5:7b --model-small openai:qwen2.5:3b
python src/12_run_e1_reports.py --out outputs/e1_reports_new --model-main anthropic:<model> --model-small anthropic:<model>
python src/14_run_e2e3.py       --out outputs/e2e3_new       --model-main claude-cli:claude-sonnet-5-5 --e1-reports outputs/e1_reports_new
python src/13_analyze_e1.py outputs/e1_ledger_new outputs/e1_reports_new outputs/e1_new
```

A full E1 run is 336 ledger calls and 168 report sessions; E2 and E3 add 324. Runners stop at a cost cap reported by the client (`--cap`), skip finished items with `--resume`, and never fill in a failed call.

To add a task, provide items, a key, a prompt for each structure and a scoring function that maps a response to detected and correct, following `src/11_run_e1_ledger.py` (text task) or `src/12_run_e1_reports.py` (agent task); the analysis in `src/lib/stats.py` needs only a table of miss indicators per item and structure. To add a structure, add an arm to the runner's `ARMS` (or `REVIEW_ARMS`) table with its prompt.

## Preregistration

S1, E1 and E2/E3 were each fixed before their first model call by recording the time and the SHA-256 of the plan and of the run and analysis code; changes after fixing were appended with time stamps. `preregistration/` has English translations of the three plans, the hashes of the original Korean documents, and a map from the original script names (whose hashes the plans record) to the files here. Analyses were run once with the fixed code; the S1 rescoring with the content-based parser was decided after the S1 results were seen and is labeled that way.

## What this repository does not do

- Model outputs cannot be regenerated bit for bit. The default run reproduces everything downstream of the stored responses; rerunning a structure with a model gives new responses, which can be compared with the stored ones.
- The stored runs used one developer's models through its command-line client. The API and open-weight paths in `src/lib/models.py` were tested against a local stand-in server, not against a real hosted or open-weight model.
- The pilot runner (`src/06_run_pilot.py`) and the drafting step (`src/04_draft_ledgers.py`) were not rerun; their stored outputs are scored.
- The calibration that chose the effect sizes and confounding strength is not reproduced; `src/01_make_report_datasets.py --calibrate` keeps the first calibration grid only.
- Planted errors are generated by code and may be easier or harder than errors models make on their own (proposal, Section 5).

## Citation and license

Please cite the proposal: [Authors] (2026). Cheap Ideas, Costly Judgment: Organizing Evaluation in AI-Enabled Science. Research proposal and test bed.

License: to be chosen by the authors.
