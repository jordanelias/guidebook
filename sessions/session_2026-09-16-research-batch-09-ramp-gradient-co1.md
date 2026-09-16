# Batch 09 — the R1 pass owed on ramp gradient (TERM-001, parameter 3) × MOB

**Session id:** `session_2026-09-16-research-batch-09-ramp-gradient-co1`
**Branch:** `claude/pensive-bardeen-d26q0s` · **PR** #140
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry`
**Scope:** R1 only — the Co-1 / T2 / Co-2 pass, outside PubMed. No determination was
re-computed; `specification_id 2` stands as batch 08 left it.

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
research_batch_dod.py --session <id>        NON-COMPLIANT — 1 rule: R9a
citation_mining_completeness.py --session   EXAMINED: 1 · Outstanding 0 · VERDICT: CLEAN
run_checks.py --selftest                    PASS (before and after)
```

**The R9a failure is structural and is flagged rather than worked around.** R9a is a vacuity
guard: it fails when a batch admits no DOI-bearing source, because a pass would assert
nothing. But **a Co-1 / DPO / grey / regulatory pass admits no DOI-bearing sources by
construction** — none of them have DOIs. So the definition-of-done gate reports
NON-COMPLIANT for exactly the evidence class R1 exists to reach, and the contract declares
research invalid when non-compliant. Every other rule passes. This needs an owner ruling:
either R9a becomes NOTHING-IN-SCOPE-is-acceptable when no admission carries a DOI, or Co-1
batches carry a standing waiver. **Waiver recorded here and in PR #140; nothing was
relabelled to make it green.**

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
