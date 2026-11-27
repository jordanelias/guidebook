# Draft for the owner to adopt or amend: the D1 identification entry (not a delegated resolution)

**What this file is.** This is a draft. The owner may adopt it, amend it or discard it; it records nothing until then. It is **not** part of the delegated block in `delegated-resolutions-2026-11-27-v3.md` (OD-105 refers the authorship question to the owner). No session appends it on its own say-so. `review-identity-need-icf` checks only that the cited heading begins "Owner" and that the entry names each row as TRIPLE-<id>; it does not check that the words are the owner's, so the safeguard is the convention behind it (ledger 8490, "so that no session states its own row"). Appending it departs from the 2026-11-26 ACTION (3), which says to cite "this entry"; record that departure.

**Why it exists.**
- The verb accepts an `--approval-ref` only when the heading begins "Owner" and the entry's text names every row of the batch as `TRIPLE-<id>` (`dbcore.ledger_entry_names`).
- The owner's answer is recorded once, in the ledger. Find it with `git grep -n -F "D1 retire" -- references/project-standards.md`. That entry names no TRIPLE token. Read it from its heading to the next `## ` heading; a dry run of the verb citing it is refused with "does not name TRIPLE-53" (`audit-session-work.md`, AU-02).

**How to use it.**
- Append it only after the owner has typed words that adopt it or name the rows. Put those words in the quotation slot.
- Date the heading with the day of those words.
- Before appending, confirm that the heading occurs once: `grep -c -F "<heading text>" references/project-standards.md` must print 0. A second identical heading makes the verb refuse.
- The text does not restate the owner's 2026-11-26 answer; it cites it by the grep above.

The text, between the rules below:

---

## Owner answer <YYYY-MM-DD> — the rows of D1 (A-SIZE with e120): TRIPLE-53, TRIPLE-57 and TRIPLE-61

Given in <session>, in a typed message. Derive the time from the preserved transcript once committed. Recorded on contact (CLAUDE.md rule 0).

**Owner's words, quoted (typed):**

> "<the owner's words adopting this identification or naming the rows, verbatim>"

**Readings.**
- [ASSUMPTION: the rows the owner's D1 answer applies to are TRIPLE-53 (LPA), TRIPLE-57 (TALL) and TRIPLE-61 (BAR). These are the pending rows of need A-SIZE with ICF e120 that item D1 of the approval list described as "the three pending e120 rows (A-SIZE with LPA, TALL, BAR)" — basis: `select triple_id, identity_code, state from identity_need_icf where need_code = 'A-SIZE' and icf_code = 'e120' and retired_at is null`, re-run on the day of appending; the earlier owner entry is found with `git grep -n -F "D1 retire" -- references/project-standards.md`.]
- The answer itself is not repeated here. Read it where the grep finds it.

CONDITION: any session retiring or counting the A-SIZE e120 rows, or planning GAP-379.
ACTION: (1) Retire TRIPLE-53, TRIPLE-57 and TRIPLE-61 with `db.py review-identity-need-icf --decision reject`, citing this entry's heading as `--approval-ref`, in a data pull request of its own (CLAUDE.md rule 10). Dry-run it on a scratch copy first. (2) GAP-379 gets a dated note and stays open for A-TRIGGER (COM, EPI). (3) Treat the reading above as unratified except where the owner's words state it.
DATE: <YYYY-MM-DD> — owner answer (typed words, quoted above).

---
