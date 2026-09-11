# ICD-11 verification is possible after all — and MB5 checks out

**I was wrong, and the correction matters more than the finding.** Hours earlier I reported that
*"not one ICD-11 code can be verified from this container"* and called the block absolute. It was
not. The owner supplied `https://icd.who.int/browse/`, and reading that page's own markup led to
WHO's CDN release files, which are **unauthenticated**. What I had actually established was that the
*OAuth2 API* and the *JavaScript browser* were closed to me — and I generalised from two closed doors
to a closed building. `governance/research-contract.yaml` R10 says a publisher block is not a
terminal answer; I applied that rule to citations all session and failed to apply it here.

## The route, and the artefact

    https://icdcdn.who.int/static/releasefiles/2024-01/SimpleTabulation-ICD-11-MMS-en.zip

3,421,544 bytes · `sha256 b92212138c67738a…` · persisted via `retrieval_log.fetch()` under
`retrieval-log/session_2026-09-11-medical-lens-icd11/`. Found by fetching the browse root and
grepping its markup for `who.int` hosts — the page advertises its own release files.

`_extension_for` correctly wrote it as `.zip` rather than `.json`, which is the 2026-09-02
content-sniffing fix doing the job it was built for.

Contents: `readme.txt` (a column dictionary), `SimpleTabulation-ICD-11-MMS-en.txt` (10,863,111
bytes, tab-separated), and an `.xlsx` of the same. **36,044 entities.**

## MB5, verified from those bytes

The owner's example is exactly as described. Chapter **21 — "Symptoms, signs or clinical findings,
not elsewhere classified"**. The grouping names itself:

| | |
|---|---|
| `BlockL3-MB5` | **Paralytic symptoms** ← the block; bears no code |
| `MB50` | Tetraplegia (+ `.0` flaccid, `.1` spastic, `.Z` unspecified) |
| `MB51` / `MB52` | Diplegia of upper / lower extremities |
| `MB53` | Hemiplegia (+ alternating, flaccid, spastic) |
| `MB54` / `MB55` | Monoplegia of upper / lower extremity |
| `MB56` | Paraplegia |
| `MB57` | Functional level of injury of spinal cord (cervical, thoracic, lumbar, sacrum) |
| `MB5Y` / `MB5Z` | Other specified / unspecified **paralytic symptoms** |

32 categories in total. Its ancestry is `BlockL1-MB4` (clinical findings of the nervous system) →
`BlockL2-MB4` (symptoms or signs involving the nervous system) → `BlockL3-MB5` (paralytic symptoms).

## "High level" is now a measured quantity, not a judgement

`ClassKind` partitions the 36,044 entities: **28 chapters · 1,353 blocks · 34,663 categories.** The
readme states that *"Blocks are high level groupings that do not bear a code"* — so the owner's "high
level" resolves to **blocks**, and the ratio settles the grain argument outright: anchoring on
categories would be a 34,663-row nomenclature, anchoring on blocks is a browsable lens.

**Consequence for the schema, and it is already accommodated.** A block's identifier is a `BlockId`
(`BlockL3-MB5`), not a code. `base_taxonomy_medical.icd11_anchors` is TEXT and `add-medical`'s
payload check greps the artefact for the literal string, so a BlockId verifies exactly as a code does.
Nothing needs changing — but the column's comment calls them codes, and that wording should widen.

## The chapter choice is the real finding

**Chapter 21 is the right chapter for this project, and now demonstrably so.** Symptom-and-sign
entities describe *functional presentation* — tetraplegia, paraplegia, hemiplegia, functional level of
cord injury. That is the same subject matter as our axes, which are demand constructs. A disease
chapter is one inferential step further out: "multiple sclerosis" does not state a functional demand,
whereas "paraplegia" nearly is one.

This is why the adjudication's 29 disease *entities* were the wrong shape, and it is a stronger
reason than grain alone. **`MB57` Functional level of injury of spinal cord** is the clearest case:
it is what `SCI` means functionally, expressed in WHO's own vocabulary.

It also sharpens the over-reach caveat rather than dissolving it. `MB56` Paraplegia impairs b730, and
b730 is declared by AX-AMB, AX-REA and AX-WHM — but BAR, LPA and TALL sit on those axes for
anthropometric reasons. The join still proposes and judgment still prunes; Chapter 21 just makes the
candidate list far better than a disease chapter would.

## What is now unblocked, and what is not

**Unblocked:** every anchor can be verified offline against a persisted artefact. `icd11_verified_at`
can be stamped for real. No WHO credentials are needed for the linearization.

**Still open:** the WHO ICD API remains 401 and would be needed for *entity-level* detail beyond this
flat file (definitions, parents/children as data, post-coordination). The flat file carries Code,
BlockId, Title, ClassKind, depth, chapter, BrowserLink and grouping membership — which is everything
a correspondence map at block grain requires, and nothing more.

**Licensing is narrowed but not settled.** The owner ruled "use ICD-11", which answers DG-NON item 7
as to source. The file's `readme.txt` is a column dictionary and states no licence, so what governs
reuse of WHO's *titles* in a CC BY-SA 4.0 work is still unread. The point-don't-copy design keeps the
exposure to bare identifiers plus, at most, a title used for identification — the same way the project
already stores `standard_number` values like `DIN 18041:2016`.
