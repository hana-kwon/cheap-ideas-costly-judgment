# ============================================================
# START DATE   : 2026-10-31
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~1 min
# DESCRIPTION  : Copies an original run folder into runs/ and applies the documented path substitutions
#                (config/transcript_substitutions.json) to the copies. Used once when the repository was
#                assembled; it is not part of run_all.py. The source folder is only read.
# INPUT FILES  : <src> (an original run folder), config/transcript_substitutions.json
# OUTPUT FILES : <dst> (must not exist), <dst>/../substitution_log_<name>.json
# USAGE        : python tools/scrub_copy.py <src> <dst> [--exclude-name data.csv] [--exclude-dir failed_cap_261029]
# ============================================================
import argparse
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_rules():
    cfg = json.load(open(ROOT / "config" / "transcript_substitutions.json"))
    home = str(Path.home())
    user = os.path.basename(home)
    return [(a.replace("$HOME", home).replace("$USER", user), b) for a, b in cfg["rules"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--exclude-name", action="append", default=[])
    ap.add_argument("--exclude-dir", action="append", default=[])
    a = ap.parse_args()
    src, dst = Path(a.src), Path(a.dst)
    if dst.exists():
        raise SystemExit(f"{dst} exists; refusing to overwrite")
    rules = load_rules()
    counts = {b: 0 for _, b in rules}
    files = changed = skipped = binary = 0
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = sorted(d for d in dirnames if d not in a.exclude_dir and d != "__pycache__")
        rel = Path(dirpath).relative_to(src)
        (dst / rel).mkdir(parents=True, exist_ok=True)
        for fn in sorted(filenames):
            if fn in a.exclude_name or fn == ".DS_Store":
                skipped += 1
                continue
            raw = (Path(dirpath) / fn).read_bytes()
            files += 1
            try:
                txt = raw.decode("utf-8")
            except UnicodeDecodeError:
                (dst / rel / fn).write_bytes(raw)
                binary += 1
                continue
            new = txt
            # ★ IMPORTANT: rules run in order, longest path first, so the run roots keep a readable name.
            for old, rep in rules:
                counts[rep] += new.count(old)
                new = new.replace(old, rep)
            changed += new != txt
            (dst / rel / fn).write_bytes(new.encode("utf-8"))
    log = dict(source_name=src.name, files_copied=files, files_changed=changed, files_excluded=skipped,
               non_utf8_files=binary, replacements_by_rule=counts,
               excluded_names=a.exclude_name, excluded_dirs=a.exclude_dir)
    (dst.parent / f"substitution_log_{dst.name}.json").write_text(json.dumps(log, indent=1) + "\n")
    print(json.dumps(log))


if __name__ == "__main__":
    main()
