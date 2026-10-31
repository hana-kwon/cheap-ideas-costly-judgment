# ============================================================
# START DATE   : 2026-10-25
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~2 s
# DESCRIPTION  : Writes the 24 synthetic ledger document sets (4 countries x 3 workloads x 2 versions), each in
#                two renderings (local informal text and standardized table) with its answer key, plus a
#                scoring self-test and the recoverability (parity) check. With the two renderings these are
#                the 48 packets of the ledger task.
# INPUT FILES  : none (seeds are the packet tags, e.g. random.Random("KEN_40tx_a"))
# OUTPUT FILES : <out>/{CTY}_{N}tx_{VER}_{local.txt, standard.csv, answer_key.csv},
#                <out>/scoring_selftest.csv, <out>/parity_check.csv
# USAGE        : python src/03_make_ledger_packets.py --out <empty dir>
# ============================================================
import argparse
import csv
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import ledger_packets as pk  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists() and any(out.iterdir()):
        sys.exit(f"{out} is not empty")
    out.mkdir(parents=True, exist_ok=True)
    tests, parity = [], []
    for cty in pk.COUNTRY:
        for n in pk.WORKLOADS:
            for ver in pk.VERSIONS:
                tag = f"{cty}_{n}tx_{ver}"
                docs = pk.make_transactions(cty, n, random.Random(tag))
                key = pk.answer_key(docs)
                local = pk.render_local(cty, docs, random.Random(tag + "-render"))
                with open(out / f"{tag}_standard.csv", "w", newline="") as f:
                    csv.writer(f).writerows(pk.render_standard(docs))
                (out / f"{tag}_local.txt").write_text("\n".join(local) + "\n")
                with open(out / f"{tag}_answer_key.csv", "w", newline="") as f:
                    wr = csv.DictWriter(f, fieldnames=list(key[0]))
                    wr.writeheader()
                    wr.writerows(key)
                pc = pk.parity_check(cty, docs, local)
                parity.append(dict(packet=tag, docs=len(docs), duplicates=sum(k == "duplicate" for _, _, k in docs),
                                   parity_failures=pk.parity_failures(pc), **pc))
                # ★ IMPORTANT: scoring self-test. A perfect ledger must score 1 and each kind of damage must
                # lower the score, in every packet.
                perfect = [dict(doc_ids=k["doc_ids"], date=k["date"], account=k["account"], pay=k["pay"],
                                amount=k["amount"]) for k in key]
                cases = {"perfect": perfect, "one_duplicate_row": perfect + [perfect[0]],
                         "first_two_merged": [dict(perfect[0], doc_ids=perfect[0]["doc_ids"] + "|" + perfect[1]["doc_ids"])] + perfect[2:],
                         "all_dates_wrong": [dict(p, date="1900-01-01") for p in perfect],
                         "amount_plus_049": [dict(p, amount=float(p["amount"]) + 0.49) for p in perfect],
                         "one_malformed_line": perfect}
                for lab, sub in cases.items():
                    tests.append(dict(packet=tag, case=lab, **pk.score(key, sub, malformed=lab == "one_malformed_line")))
    for name, rows in (("scoring_selftest.csv", tests), ("parity_check.csv", parity)):
        with open(out / name, "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(rows[0]))
            wr.writeheader()
            wr.writerows(rows)
    print("packets:", len(parity), "| total parity failures:", sum(p["parity_failures"] for p in parity),
          "| duplicate receipts:", sum(p["duplicates"] for p in parity))


if __name__ == "__main__":
    main()
