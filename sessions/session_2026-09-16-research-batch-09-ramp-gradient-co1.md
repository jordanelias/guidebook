# Batch 09 — the R1 pass owed on ramp gradient (TERM-001, parameter 3) × MOB

**Session id:** `session_2026-09-16-research-batch-09-ramp-gradient-co1`
**Branch:** `claude/pensive-bardeen-d26q0s` · **PR** #140
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry`
**Scope:** R1 only — the Co-1 / T2 / Co-2 pass, outside PubMed.

**CORRECTED 2026-09-17.** This line read *"No determination was re-computed; `specification_id 2`
stands as batch 08 left it."* It was true when written and false within the hour, and the
correction is left visible because the mechanism is the point: admitting evidence for a parameter
that already carries a live determination makes that determination's junction incomplete, and
`test_db_integrity` K02 goes **BLOCKING red** until the cell is re-determined. It is not optional
and it is not a separate piece of work — it is what admitting evidence *means*. So
`specification_id 2` was retired and superseded by **`specification_id 3`**, which accounts for
every extraction on parameter 3. Verify with `PRAGMA`-free SQL against `specifications` rather
than trusting this sentence.

**The determination moved and did not change.** `specification_id 3` is still `pending` with
`refs=0`, because `assess_cell.gather_sources()` gathers `figure_role IN ('claim','derived')` and
both Co-1 rows are `finding`. That is the exact mechanism the owner named on 2026-09-16: a
determination cannot yet be reached from findings plus a threshold. The batch's headline evidence
is in the corpus and reaches no cell.

Every figure below is derived from `data/guidebook.db` after the migration applied (rule 7).
Re-derive before relying on any of it; the commands are in the PR.

## Why this batch exists

Batch 08 closed with *"A Co-1 pass outside PubMed"* named as owed, and with the PubMed Co-1
zero diagnosed as a **venue** fact rather than a query-shape one — 0 hits with the
co-production clause, 63 with the same subject terms and the clause removed (exec 31, the
control). This batch tested that diagnosis and discharged the debt.

**The diagnosis was right.** The same subject, sought in a different venue and a different
language, is not empty.

## The finding: the Co-1 leg succeeded in Japanese and nowhere else

Ten executions across six languages. Every English execution — UK, US, Co-1 and Co-2 alike —
returned no disability-led publication stating or contesting a gradient. The Japanese
execution returned two sources written **by wheelchair users**, one of which is admitted.

- **REF-00989** — 白倉栄一 (Shirakura Eiichi), 車椅子ライフデザイナー and wheelchair user,
  on WelSearch (a site that self-describes as publishing 専門家 **and** 当事者). First-person
  authorship is evidenced **in the retrieved bytes**, not inferred from venue (D-0178):
  *「車椅子ユーザーである私がスロープの勾配の本音をお伝えしていきながら」*.
- Two extractions, both `finding`/`participatory_finding`:
  - *「実際に、一般の乗りなれている車椅子ユーザーであれば、1/12は大丈夫かと思います。1/8となると、助走があればいけると思います。」*
  - *「8分の１より勾配がある場合は、いくらスロープがあっても車椅子を自走で上るのは不可能に近いです。」*

**Why the second row matters beyond this cell.** The owner's 2026-09-16 statement records
that the dose-response evidence has a degenerate solution — both curves monotonic, so "best"
resolves to 0°, which is not a ramp — and that the missing half is a **threshold of
acceptability** no admitted source supplied. This row supplies one for self-propulsion, from
lived experience: above one-in-eight it is not that the ramp is uncomfortable, it is that it
cannot be climbed. It is a **boundary, not a recommended value**, and must not be read as
asserting that one-in-eight is acceptable.

## A second jurisdiction, and a disagreement worth the guidebook's attention

- **REF-00988** — DGUV Information 215-112 Kap. 4.3 (DE, T5): *"Rampenläufe dürfen maximal
  eine Neigung von 6 % aufweisen"*. Against **REF-00987**'s ADA 1:12 (8.33%) already in the
  corpus, two regulatory strata disagree by about a factor of 1.4 on the same parameter.
  Neither anchors at full strength (§6). The document names no basis for its 6%, so none is
  recorded — DIN 18040-1 appears only as further reading, and was not guessed at.

- **Not admitted, and the reason is specific.** The Flemish *Handboek Toegankelijkheid
  Publieke Gebouwen* carries the single most useful thing this pass found — a
  **rise-conditioned** gradient table (≤10cm→10%/1m; 10–25cm→8,3%/3m; 25–50cm→6,25%/8m;
  >50cm→5%/10m) **and the acceptability criterion itself**: *"Bij hellingen vormt de fysieke
  haalbaarheid van de (zelfstandige) rolstoelgebruiker het uitgangspunt"*, because *"hoe
  groter het hoogteverschil, hoe zachter … men gedurende een langere tijd een inspanning moet
  leveren"*. The retrieved bytes carry **no publication date**, `add-source --year` is
  required, and inventing one is the §5(c) failure. Staged as a candidate; a dated carrier is
  owed. That is the whole blocker — nothing about its content is in doubt.

## The defect this pass found, which is larger than the batch

**The verbatim fidelity check — the mechanical answer to the 2026-08-19 fabrication — was
vacuous for every non-Latin script.** `retrieval_log.normalise_quote` reduced text to
`[^0-9a-z]`, i.e. ASCII letters and digits, deleting every character of every non-Latin
writing system. Measured:

- The 45-character sentence 「8分の１より勾配がある場合は…不可能に近いです。」 normalised to `8`.
- So did the **invented** sentence 「この文章はコーパスに存在しません8」 — *"this sentence does not
  exist in the corpus"* — and it therefore **verified against the artefact**.

So for a source in Japanese, Chinese, Korean, Arabic, Hindi or Bengali — six of the nineteen
languages `skills/multilingual-research_SKILL.md` obliges — `--claim-text` and `--quote` could
be fabricated outright and the floor passed. Two further consequences, both measured:

- **R11 was mechanically impossible for CJK.** A concept phrase with no ASCII digits (自走,
  勾配) normalised to the empty string and was refused as *"no letters or digits to match"*.
  Harvesting a source's own words — the one thing R11 asks — could not be done in the
  source's own script.
- **No CJK numeral could pass the digit check.** `db.py` extracts digits with `\d`, which is
  Unicode-aware and matches full-width `１`; the normaliser deleted it. The two halves of one
  check disagreed, so `8分の１` could never support a claimed value.

**Fixed** in `retrieval_log.normalise_quote`: NFKC first (so `１`→`1`), accents folded rather
than deleted (`Pérez`→`perez`, not `prez`), and `str.isalnum()` in place of the ASCII class.
Verified: the invented Japanese and Korean sentences now fail; all four real Japanese quotes
still pass; **all 18 quotes already committed in the corpus still verify, zero regressions**.

## A second gap, raised by the owner mid-session and shipped

**The repository could not read the format its evidence arrives in.** `retrieval_log.py`'s own
comment says PDF *"is the format Co-1 and disability-led evidence overwhelmingly arrives in"*,
and a fresh container has no `pypdf`, no `pdfminer`, no `pdftotext`. The first non-English
source of this pass was a PDF. `pypdf` and `cffi` are now declared in
`governance/check-registry.yaml`'s `batteries:` — the one home of the dependency list — with
the reason recorded there. `cffi` is load-bearing, not cosmetic: the container's Debian
`cryptography` 41.0.7 ships without `_cffi_backend`, so `import pypdf` raises a Rust
`PanicException` that `except ImportError` does not catch.

## What the gates say

```
research_batch_dod.py --session <id>        COMPLIANT   (was NON-COMPLIANT on R9a; see below)
citation_mining_completeness.py --session   EXAMINED: 1 · Outstanding 0 · VERDICT: CLEAN
run_checks.py --selftest                    PASS (before and after)
```

**R9a WAS NON-COMPLIANT AND IS NOW FIXED, ON AN OWNER RULING OF 2026-09-17.** This section
first recorded a waiver: R9a fails when a batch admits no DOI-bearing source, and **a Co-1 /
DPO / grey / regulatory pass admits none by construction**, so the definition-of-done gate
reported NON-COMPLIANT for exactly the evidence class R1 exists to reach. The owner ruled to
fix rather than waive, and the fix is that R9a **could** have performed the check all along:

- The identifier stash holds URLs as well as DOIs — derive the split with
  `SELECT COUNT(*) FROM source_locators WHERE COALESCE(url,'') <> ''` — and both of this
  batch's admissions carry one. R9a compared DOIs only. Widening it is R9b's own 2026-08-23
  widening applied to R9a, on the same reasoning: identity is not DOI-conditional.
- **A URL counts as a held identity only when it resolves to exactly one ref_id.** Measured
  before the change: the BSI catalogue page for BS 8300 is held against **seven** ref_ids,
  the ISO, DIN and ADA standards pages against five each. Those are landing pages — one
  address serving a standards family — and sharing one is correct. A naive URL join would
  have fired on every one and advised "cross-file the held id", which for two genuinely
  different standards destroys an identity rather than repairing one.
- The zero-branch conflated **"admitted nothing"** with **"admitted sources carrying no
  comparable identifier"**, and told a batch with two well-located sources that it was
  "missing its locators". They are now separate messages, and the second is still a failure:
  a source with no resolvable identifier at all cannot be cross-filed or re-retrieved.

Fault-injected on a scratch copy, all three behaviours in one run: **fires** on a singleton
URL collision, **silent** on a three-way landing page, **silent** on a RETIRED tombstone.

## Tooling defects found and NOT worked around

1. **`amend-search` cannot record an admission decided after its search was logged.**
   `log-search` refuses `--results-admitted` without `--admitted-ref-id` (invariant H05);
   `amend-search` takes only `--append-note`. So a late admission is permanently edgeless —
   the very state H05 exists to prevent, reached by the sanctioned route. Avoided here by
   rebuilding the scratch in admission-first order.
2. **A standards PDF cannot be given a page locator after admission.** R3 reads
   `evidence_sources.pages`; `correct-source` derives values from a payload and has no value
   flag; `amend-source` refuses bibliographic fields. `add-source --pages` at admission is the
   only path. Avoided by rebuilding, not by hand SQL.
3. **`--verbatim-exempt` covers `--claim-text` but not the relation `--quote`**, though
   `_require_verbatim`'s own docstring says *"ONE RULE, EVERY QUOTED COLUMN"*. A PDF-only
   source stating its figure against a named reference therefore cannot be extracted at all.
   Not hit here — DGUV states its figure absolutely, so `--relation none` is literally true —
   but it will bite the next standards source that cites another.

## Owed

- **A dated carrier for the Flemish handbook.** It holds the acceptability criterion.
- **Retrieval routes the general index does not reach:** APF France Handicap, CERMI/ONCE, PVA,
  DPI Japan, Foundations (HTTP 403), AOTA CPG (member-gated). Every one is a Co-1/Co-2 target
  that exists and was not reached — R14 diagnosis WRONG INDEX or RETRIEVAL FAILURE, recorded
  per execution, never as absence.
- **Nine of nineteen languages unsearched on this parameter**, and no gate says so.
- **バリアフリー法 itself** (`research_code_leads`): the corpus holds a lived-experience
  assessment of a legal figure it has never read.
- **The `EN`/`en` case split in `search_executions.language`** — pre-existing, and R5's own
  comment records the same class of bug being fixed once already.

---

## Addendum, 2026-09-17 — the contract's own gate now runs in CI

The R9a fix above exposed the larger half of the same finding, and the owner ruled on both.

**The gate CI ran was not the gate the contract names.** `research_dod` runs `--all`, which
asks whether the CORPUS is compliant. That question cannot fail for a single bad batch once
the corpus holds good sources: one batch admitting an unlocated source is invisible beside a
corpus of located ones. The contract is per-BATCH — the session-start hook says in as many
words *"Gate before you claim done: `research_batch_dod.py --session <id>`"* — and nothing ran
it. It was enforced by an operator remembering, which is CLAUDE.md §2's "you are the gate".

**`research_dod_session` is now registered BLOCKING**, scoped to `LATEST-RESEARCH`. Blocking
because DR-2026-07-25 is not hedged — *"RESEARCH IS INVALID IF IT IS NOT COMPLIANT"* — and an
advisory gate annotates that sentence rather than implementing it. It is not red-by-
construction: batch 08, batch 09 and the corpus-wide posture all pass as it lands.

**AND IT WOULD HAVE BEEN A VACUOUS GATE ON EVERY PR.** `@SESSION@` is substituted from the
pointer file; pointer files carry `.md`; the DB stores the bare stem; `--session` is
interpolated into `WHERE session = ?`. Measured before the fix:

```
created_by_session = '<id>'      -> 2 rows
created_by_session = '<id>.md'   -> 0 rows
```

So registering this check as written would have installed a BLOCKING gate that runs on every
PR, examines nothing, and reports the contract satisfied — CLAUDE.md §7's named trap ("wrong
form scopes a gate to nothing and it passes green") and §5(a) together, in the one place the
project declares research invalid without. `research_batch_dod.py` now strips a trailing
`.md` before any query runs, and the runner-expanded command was verified to examine a real
subject (2 admissions, 1 tier-1..3 population match) rather than an empty one.

**The pointer's lag is a feature here.** `LATEST-RESEARCH` moves at CLOSE, so a PR opened
mid-batch is gated on the last CLOSED batch, and the new one is gated once its pointer moves
— which is exactly when a batch claims to be done.

**One stale self-justification corrected in passing.** `research_dod`'s `no_floor` reason
argued it was "genuinely non-vacuous today (R1 fails NON-COMPLIANT on live data)". R1 is
COMPLIANT and has been for some time. The structural claim it was defending still holds; the
evidence offered for it had rotted, which is rule 7a's exact shape. It now carries the command
instead of the figure.

---

## Addendum 2, 2026-09-17 — the encoding gap, closed

Recorded above as owed and now fixed on owner instruction. It was the third and last member
of one family: **the apparatus held bytes it could not read, and said nothing.**

**Both halves were broken.** `fetch()` invoked curl with `-w '%{http_code}'` alone, so the
server's `Content-Type: text/html; charset=…` — the only authoritative statement of how those
bytes decode — was discarded at the one moment it exists. Every reader then assumed UTF-8:
`raw.decode("utf-8", errors="replace")`.

**What that did to real sentences**, measured before the change:

```
shift_jis  勾配は、12分の1を超えないこと   -> normalises to 'za121a'
euc_kr     경사로의 기울기는 8분의 1        -> '81'
gb18030    坡道坡度不应大于1:12            -> 'μyо112'
latin-1    Rampenläufe dürfen …           -> 'rampenlufedrfen…'
```

The first three cannot match anything, so a genuine quote is **refused** — blocking, but safe.
**The Latin-1 case is the dangerous one**: it yields a plausible, pronounceable body that would
match a quote typed with the same mangling, so a wrong reading could verify. These are the
encodings of the languages the multilingual skill obliges: Shift_JIS/EUC-JP, GB18030/Big5,
EUC-KR, Windows-1256, ISO-8859-x.

**The fix.** `fetch()` now records `content_type` on every manifest line. `decode_artefact()`
resolves an encoding in a deliberate order:

1. **BOM**, UTF-32 tested before UTF-16 because `ff fe 00 00` starts with `ff fe`. The mark is
   stripped explicitly — only `utf-8-sig` consumes its own, and testing caught `utf-16-le`
   decoding it as a literal U+FEFF into the text.
2. **Strict UTF-8**, and if it succeeds nothing else is consulted. This is the guard against
   the second trap: servers mis-declare charsets routinely, and honouring a wrong declaration
   over plainly-UTF-8 bytes would manufacture mojibake from a body that was fine. Real text in
   a legacy encoding is almost never accidentally valid UTF-8.
3. **Declared charset** — HTTP header first (the spec's authority), then the document's own XML
   declaration or HTML meta.
4. Otherwise **undecodable**, returned as such.

**No statistical detection, deliberately.** A guessed encoding inside a fidelity check could
produce a body that looks right and is not, which is the failure the module exists to prevent.

**Undecodable bytes are now named, never silently skipped.** A miss used to report `EXAMINED: n`
over artefacts it had not actually read; it now adds `N NOT SEARCHED, bytes undecodable: …`.
"Not found" is a statement about what could be searched, and the reader is told which.

**Verified.** Round-trip through Shift_JIS, EUC-KR, GB18030, ISO-8859-1, and BOM-bearing UTF-8,
UTF-16 and UTF-32. Mis-declaration trap: valid UTF-8 wrongly declared ISO-8859-1 still decodes as
UTF-8. End-to-end against a real Shift_JIS page written into a scratch retrieval log, a Japanese
quote is found and an invented one is not — and the same artefact under the OLD path normalised
to `'zxvza121aɓb'`, where the genuine quote does not match. **All 22 quotes already committed in
the corpus still verify, zero regressions.**
