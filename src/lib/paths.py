# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~5 min
# DESCRIPTION  : Repository locations, computed from this file. Every script takes explicit paths on the
#                command line and falls back to these defaults, so nothing depends on a home folder.
# INPUT FILES  : none
# OUTPUT FILES : none
# ============================================================
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
CONFIG = ROOT / "config"
DATA = ROOT / "data"
RUNS = ROOT / "runs"
REFERENCE = ROOT / "reference"
OUTPUTS = ROOT / "outputs"

# Report task inputs
REPORT_DATASETS = DATA / "reports" / "datasets"
REPORT_TRUTH = DATA / "reports" / "truth"
REPORT_BANK = DATA / "reports" / "bank"
REPORT_MANIFEST = DATA / "reports" / "manifest.json"

# Ledger task inputs
LEDGER_PACKETS = DATA / "ledgers" / "packets"
LEDGER_DRAFTS = DATA / "ledgers" / "drafts"
LEDGER_SEEDED = DATA / "ledgers" / "seeded"

# Stored model outputs of the reference experiments
RUN_PILOT = RUNS / "pilot"
RUN_S1 = RUNS / "s1"
RUN_E1_LEDGER = RUNS / "e1_ledger"
RUN_E1_REPORTS = RUNS / "e1_reports"
RUN_E2E3 = RUNS / "e2e3"

INSTRUMENT = SRC / "instrument"
