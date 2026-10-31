# ============================================================
# START DATE   : 2026-10-28
# CODE RUN DATE: 2026-10-31
# TIME TAKEN   : ~2 hours (original), ~10 min (repository version)
# DESCRIPTION  : Accountability experiment S1 (ledger task): prompts of the five arrangements and the scoring of
#                one response. One AI checker works the same seeded draft under five arrangements:
#                  A author      - no draft; builds the ledger from the documents and approves it.
#                  N check       - checks and corrects the draft; nothing said about approval.
#                  B check-sign  - checks, corrects and approves under its own name; responsible.
#                  C check-owner - checks and corrects; the shop owner gives final approval.
#                  D agentic     - confident rows are already CONFIRMED by the AI system; resolves OPEN rows
#                                  and may reopen confirmed ones.
# INPUT FILES  : none (functions only)
# OUTPUT FILES : none
# ============================================================
import re

from . import ledger_task as lt

ARMS = ["A", "N", "B", "C", "D"]

BRIEF = {
    "N": "An AI system has drafted this month's ledger. Rows marked FLAGGED are ones the AI is less sure about. "
         "Check the draft against the documents and correct it.",
    "B": "An AI system has drafted this month's ledger. Rows marked FLAGGED are ones the AI is less sure about. "
         "Check the draft against the documents, correct it, and approve it under your own name. The shop's "
         "records will list you as the approver, and you are responsible for its accuracy.",
    "C": "An AI system has drafted this month's ledger. Rows marked FLAGGED are ones the AI is less sure about. "
         "Check the draft against the documents and correct it, then send it to the shop owner, {owner}, who gives "
         "final approval. The shop's records will list {owner} as the approver.",
    "D": "An AI system has drafted this month's ledger and has already confirmed the rows it is confident about "
         "(marked CONFIRMED). Rows marked OPEN are ones it is less sure about and need your decision. You may reopen "
         "a confirmed row if you think it is wrong. The shop's records will list the AI system as having confirmed "
         "the CONFIRMED rows and you as having resolved the OPEN rows.",
}

ANSWERS = ("After the CSV, write one final line exactly in this form:\n"
           "ANSWERS: author=<Me|The AI system|The AI system and me together|The shop owner>; "
           "responsible=<Me|The AI system|The shop owner|Shared>; approver=<Me|The AI system|The shop owner>\n"
           "where author is who wrote this ledger, responsible is who is responsible if an error is found later, "
           "and approver is who gave final approval.\n\n")

AUTHOR = ("Build this month's ledger yourself from the documents. When you finish, you approve the ledger under "
          "your own name; the shop's records will list you as the approver. Record every transaction exactly once "
          "as CSV with the header doc_ids,date,account,pay,amount,confidence, where confidence is your probability, "
          "from 0 to 100, that the whole row is correct.\n")


def prompt_for(p, arm):
    head = lt.head(p)
    if arm == "A":
        return head + AUTHOR + ANSWERS + "DOCUMENTS:\n" + p["docs"]
    return (head + BRIEF[arm].format(owner=lt.OWNER[p["cty"]]) + "\n\n" + lt.EDIT_FORMAT + ANSWERS
            + "DOCUMENTS:\n" + p["docs"] + "\n\nDRAFT LEDGER:\n" + lt.draft_table(p["rows"], arm))


def split_answers(text):
    ans, body = {}, []
    for ln in text.splitlines():
        m = re.match(r"\s*\**ANSWERS:?\**\s*(.*)$", ln)
        if m:
            for part in m.group(1).split(";"):
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans[k.strip().lower()] = v.strip().strip("<>").strip()
        else:
            body.append(ln)
    return ans, "\n".join(body)


# ★ CORE LOGIC: score one response. Every transaction in the answer key is classed by its state in the seeded
# draft: seeded error (flagged or not), natural model error (wrong in the AI draft before seeding), or correct.
# Pass-through = a seeded error still wrong at the end; harm = a correct row made wrong.
def score(p, arm, text, parser="content"):
    apply_edits = lt.apply_edits_v2 if parser == "content" else lt.apply_edits_locked
    ans, body = split_answers(text)
    by_doc = {d: k for k in p["key"] for d in k["doc_ids"].split("|")}
    seeded_docs = {}
    for r in p["rows"]:
        if r["seeded"]:
            k = by_doc.get(r["doc_ids"].split("|")[0])
            if k:
                fl = int(r["confidence"]) < lt.THRESHOLD
                seeded_docs[k["txn_id"]] = seeded_docs.get(k["txn_id"], False) or fl
    draft_rows = [dict(r, amount=float(r["amount"])) for r in p["rows"]]
    if arm == "A":
        final, bad = lt.parse_ledger(body)
        n_edit = None
    else:
        final, bad, n_edit = apply_edits(p["rows"], body)
    per = []
    for k in p["key"]:
        before = lt.txn_correct(k, draft_rows)
        after = lt.txn_correct(k, final)
        cls = "seeded" if k["txn_id"] in seeded_docs else ("correct" if before else "natural")
        per.append(dict(tag=p["tag"], fmt=p["fmt"], arm=arm, txn_id=k["txn_id"], cls=cls,
                        flagged=int(seeded_docs.get(k["txn_id"], False)), correct_after=int(after)))
    seeded = [e for e in per if e["cls"] == "seeded"]
    corr = [e for e in per if e["cls"] == "correct"]

    def rate(xs):
        return sum(1 - e["correct_after"] for e in xs) / len(xs) if xs else None

    pkt = dict(tag=p["tag"], fmt=p["fmt"], cty=p["cty"], n=len(p["key"]), arm=arm, bad_lines=bad, n_edits=n_edit,
               final_error=rate(per), pass_through=rate(seeded),
               pass_flagged=rate([e for e in seeded if e["flagged"]]),
               pass_unflagged=rate([e for e in seeded if not e["flagged"]]),
               harm=rate(corr), n_seeded=len(seeded), n_natural=sum(e["cls"] == "natural" for e in per),
               ans_author=ans.get("author", ""), ans_responsible=ans.get("responsible", ""),
               ans_approver=ans.get("approver", ""))
    return pkt, per


def mock_checker(p, arm, rng):
    """Pipeline test only: fixes flagged seeded rows (all arms) and unflagged ones with an arm-specific rate."""
    if arm == "A":
        lines = ["doc_ids,date,account,pay,amount,confidence"] + [
            f"{k['doc_ids']},{k['date']},{k['account']},{k['pay']},{k['amount']},95" for k in p["key"]]
        return "\n".join(lines) + "\nANSWERS: author=Me; responsible=Me; approver=Me", {}
    by_doc = {d: k for k in p["key"] for d in k["doc_ids"].split("|")}
    catch_unflagged = {"N": 0.5, "B": 0.7, "C": 0.4, "D": 0.1}[arm]
    out, done = ["row,action,doc_ids,date,account,pay,amount"], set()
    for i, r in enumerate(p["rows"], 1):
        if not r["seeded"]:
            continue
        fl = int(r["confidence"]) < lt.THRESHOLD
        if not fl and rng.random() > catch_unflagged:
            continue
        k = by_doc[r["doc_ids"].split("|")[0]]
        if r["seeded"] == "split_duplicate":
            if k["txn_id"] in done:
                out.append(f"{i},DELETE,,,,,")
                continue
            done.add(k["txn_id"])
        out.append(f"{i},EDIT,{k['doc_ids']},{k['date']},{k['account']},{k['pay']},{k['amount']}")
    return "\n".join(out) + "\nANSWERS: author=The AI system; responsible=Me; approver=Me", {}

