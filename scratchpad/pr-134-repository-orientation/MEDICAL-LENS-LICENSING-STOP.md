> # ⚠ SUPERSEDED 2026-09-11 — BOTH ITS PREMISES FELL, IN OPPOSITE DIRECTIONS
>
> **Read this file as a record of what was true for about four hours, not as instruction.** It is
> kept rather than deleted because the project supersedes wrong records in place; the ledger entries
> in `references/project-standards.md` dated 2026-09-11 are what binds.
>
> **1. The licensing block is lifted.** The owner ruled *"Yes, use ICD-11"*, answering DG-NON item 7
> as to source. This file's central claim — that writing content awaits a licensing ruling — is spent.
>
> **2. The 29 candidate rows are withdrawn, and not because of licensing.** Measured against WHO's own
> release file: ICD-11 offers 108 depth-1 blocks even restricted to the eight chapters touching our
> axes, 6.4× the axis vocabulary, and the admitted corpus names exactly ONE diagnosis needing a route.
> The lens is **demand-populated** — a row when a source or reader route names a diagnosis, never a
> pre-populated mirror. So the thing this file was holding back is not merely unblocked; it is
> cancelled.
>
> **3. And the verification claim in here is wrong too.** This file states ICD-11 codes cannot be
> verified from the container. They can: WHO's CDN release files are unauthenticated, and
> `SimpleTabulation-ICD-11-MMS-en.zip` is persisted under `retrieval-log/`. I had generalised from a
> 401 API and a JavaScript browser to a closed building, which is exactly what R10 forbids.
>
> **What survives:** the reasoning that identifiers are facts while prose is ours (rule 5), and that
> a determination keyed on a diagnosis alone asserts the medical model as the frame. Both are now
> enforced in `add-medical` and migration 074.
>
> **One thing that CANNOT be corrected:** migration 074's header still says the content half is
> licensing-blocked. Migrations are immutable once committed (`CLAUDE.md` rule 3 — fix forward, never
> edit), so that text stands and this entry is its supersession.

# STOP — the medical vocabulary's content half is blocked on a licensing ruling

Derived 2026-09-11. The structural half (migration 074, the two crossing maps, `db.py add-medical`,
the integrity check) is **code and schema and is not blocked**. What is blocked is writing 29 rows of
ICD-11-derived `display_name` / `description` text.

## Three findings, and they compound

**1. Licensing is explicitly non-delegable, and D-0188 did not enumerate it.**
`governance/decision-protocol.md:81` lists *"Licensing model (per A11 §4)"* as DG-NON item **7**, and
`CLAUDE.md` §8 names licensing among the owner-reserved concerns. D-0188 delegated adjudication of
**the items presented to the owner**; the medical vocabulary's *content* was one of them, its
*licensing* was raised by nobody — not by the adjudication, and not by me when I briefed it. The
delegation cannot be stretched to cover a question it never saw. That is the same discipline the
delegation itself was recorded under: it reaches the enumerated items and no further.

**2. The guidebook is CC BY-SA 4.0, which is a share-alike licence.**
`governance/legal-regulatory.md:130`, with the consequence spelled out at `:133-137` — *"derivatives
must be released under CC BY-SA 4.0"*. ICD-11 is WHO copyright under WHO's own terms. My
understanding is that ICD-11 content carries a no-derivatives IGO licence, which would be
**incompatible with share-alike**: ND-licensed text cannot be folded into a work that must remain
relicensable under SA.

**[UNVERIFIED] — and deliberately so.** Licence terms change, this is outside what should be asserted
from memory, and the project's whole posture is that a bibliographic or legal fact written from memory
is the defect (`CLAUDE.md` §5(c)). **What resolves it:** read WHO's current ICD API Terms of Use and
the ICD-11 licence notice directly. Do not resolve it from a model's recollection, including this
file's.

**3. The API is unreachable from this container, so every anchor would be from memory.**
Measured: no ICD/WHO credentials in the environment; `https://id.who.int/icd/release/11/mms` → **401**;
`https://icdaccessmanagement.who.int/connect/token` → **400**. The adjudication's Ruling 1.4 requires
`icd11_verified_at` to be set **only** from a persisted payload under `retrieval-log/`. With no
credentials, every one of the 29 anchors lands NULL — which is the honest outcome the rule designs
for, and also the reason not to pretend the vocabulary is verified.

## The design that probably dissolves all three, and is the project's own rule

**Store the bare code as an anchor; write `display_name` and `description` in the project's own words.**

- A bare alphanumeric code (`6A02`) is a fact, not creative expression. The prose stays ours.
- It is **rule 5 verbatim** — *point, do not copy*. The licensing constraint and the project's
  architecture rule happen to point the same way, which is the strongest kind of agreement available.
- It serves the CRPD posture better than clinical phrasing would: the identity lens already holds the
  community's preferred names (`populations.display_name`), and D-0170's `identity_first` relationship
  exists precisely so the community's name renders rather than the diagnosis.
- The anchor stays verifiable by anyone holding credentials, and `icd11_verified_at` records whether
  verification has actually happened rather than whether someone believed it had.

**This is a recommendation, not a ruling.** It is owner-gated under DG-NON item 7.

## What must not happen while this is open

- No ICD-11 title or description text written into `base_taxonomy_medical`.
- No `icd11_verified_at` set without a persisted payload naming the code.
- No claim in a commit, PR body or record that the vocabulary is ICD-11-verified.

CONDITION: Any session filling `base_taxonomy_medical`, or citing the adjudication's Ruling 1.1 row table.
ACTION: Build the structure; leave the content pending the owner's licensing ruling. The 29 candidate
rows in the adjudication are *expected* anchors and are explicitly not verified — treat them as a
retrieval queue, never as data.
DATE: 2026-09-11.
