# Present both — the ruling, and the two defects reading a ratio exposed

**Session id:** `session_2026-09-17-notation-present-both`
**Branch:** `claude/research-preparation-joue00` · **PR** #144
**Owner ruling:** 2026-09-17, recorded in `references/project-standards.md`

> **"Present both--don't choose between ratio or percentage."**

> **CLOSED.** Migration 087, notation arithmetic in the engine, two data corrections, one gap
> closed by the ruling. 29 pilot assertions passing; `test_db_integrity` 71/71;
> `validate_evidence_state` 7/7; battery PASS with no blocking failures. Schema 86 → 87.

## What the ruling settles, and what it re-frames

The `DEC` gap asked whether the engine may convert a ratio into a percentage. The ruling makes the
question malformed: **the engine does not pick a notation at all.** It composes across them and
carries both.

Recorded in the ledger with three limits the ruling implies rather than states: conversion is for
**comparison, not replacement**; a derived notation is **marked derived**; and a derived notation
that does not terminate — `1:12` is 8.333…% — is **marked inexact**, because rounding a figure into
the position of a stated one is the 2026-08-19 shape one column along. And a notation is not a unit:
millimetres and degrees stay refused (ACTION 4).

## The result

```
param 3×MOB   provisional   max 5 %   ·   max 1:20
              both stated by a source · both exact · neither chosen
```

Before the ruling the same cell composed its interval from **2 of 7** governing claims. All seven
now compose, on one exact scale held in `Fraction`, and the answer changes for a reason worth
stating: **the gentlest ceiling in this corpus is written as a ratio.** An engine that could not
read ratios was selecting the gentlest *percentage* and calling it most-accommodating.

## Two defects that reading a ratio exposed

Neither was caused by this change. Both were unreachable while the engine was half-blind.

**1. A determination with a minimum above its maximum.** `REF-00987` (ADA) carried **no comparator**
while its own verified claim_text reads *"not steeper than 1:12"*. `parse_bound` reads a bare number
as a **point**, so the row contributed a floor as well as a ceiling and the selection returned
`min 8.33% .. max 5%` — an interval describing nothing. It had never surfaced because the row is
written as a ratio and the engine had never read it.

- The engine now **refuses** an incoherent interval and names the likely cause.
- The comparator is recorded via `amend-extraction`, the verb that exists for exactly this. That is
  **recording what the source already says**, not changing a judgment: every other governing row for
  this parameter carries `<=`.

**2. `close-gap` accepts statuses the database rejects.** The CLI tests `LIKE 'CLOSED%'`; the strict
vocabulary lives as a **Python tuple inside `test_db_integrity`**. `CLOSED-RULED` was accepted by the
writer and failed B06 afterwards. The right status existed all along — `CLOSED-DECIDED`, added for a
gap closed by *deciding* it, which is precisely what a ruling does. **The vocabulary's only home is a
test file, so the CLI cannot derive it** — rule 8's shape, and not fixed here: the fix is to move the
vocabulary to the schema or to `dbcore`, which is a migration and a decision about where it lives.

## One limitation of the write path, hit and worked around

`emit_batch_sql` emits **every insert before every update**, so a retire-then-replace on a uniquely
indexed row cannot travel in one migration: the new determination is inserted while the old is still
live and `idx_spec_row_identity` refuses it. The transaction rolled back cleanly and nothing partial
reached the blob. Split into two migrations, which is the pattern batch 09 already used. Not fixed:
reordering globally would break the opposite case, where a row must exist before it is updated.

## A silent failure closed after the adversarial pass named it

The attestation's counterclaim pointed out that `NOTATION_FAMILIES` invites extension by analogy,
and that adding `degrees` would be **wrong** — a gradient in degrees is the *arctangent* of the
ratio, not a rescaling. Worse, adding it to the tuple without writing the arithmetic made
`to_canonical` fall through and read `5` degrees **as 5%**, silently, only in the composed value.

`to_canonical` and `from_canonical` now **refuse** a family member with no conversion behind it, and
a test pins it. Membership is a mathematical claim; forgetting to back it is now an error rather
than a wrong answer. What the guard does *not* prove is that a conversion someone did write is
correct — a wrong-but-present one would pass everything here.

## What did not change

The proxy branch, its marker and its supporting set are untouched. The value moved from *"5%, and
five claims unread"* to *"5% = 1:20, all seven read"* — a better-founded number, not a different
claim. **The determination still rests on codes and is warranted by findings**, and the engine still
does not read the dose-response curves' tested ranges. That remains owed.
