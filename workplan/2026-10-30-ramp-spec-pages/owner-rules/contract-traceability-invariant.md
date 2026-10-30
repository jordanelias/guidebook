---
name: contract-traceability-invariant
description: "Hard requirement for the Guidebook — every boundary/handoff/IO at every stage and layer must have a verifiable, traceable contract."
metadata: 
  node_type: memory
  type: project
  originSessionId: d8ad22dd-b407-4f8b-b198-5ff102840966
---

A load-bearing requirement for the Guidebook pipeline: **at every single stage and layer — from the moment a website is visited and something of value is located, through every handoff — there must be a proper handshake/contract.** EVERY handshake / contract / handoff / exchange / input-output MUST be **verifiable** (you can mechanically check the contract held) AND **traceable** (you can follow provenance backward and forward across the boundary).

Boundaries this covers in the current system (non-exhaustive): runtime website request → data lookup → render; migration → DB (`data_migrations` ledger, `content_sha`); DB → Pydantic/JSON schema validation; DB → generated parts/site/vetting-surface; research → evidence collection (citation mining, probes, source/URL verification runs); evidence → judgment (directness, scope, tier, FDR, convergence, evidence_cell_state); judgment → synthesis → collation → rendering; governance DR → attestation JSON; CI gate handoffs.

**Why:** This is the transparency guarantee that makes the output policy-grade and academically defensible (see [[project-end-goal]]). An untraceable or unverifiable handoff is a break in the evidence chain even if both sides are individually correct — it is treated as a defect of the same class as data corruption.

**How to apply:** When auditing or building, enumerate boundaries and for EACH ask: (1) Is there an explicit contract (schema/interface/ledger entry)? (2) Is conformance verifiable by a check, not by trust? (3) Is the exchange traceable end-to-end (provenance preserved, attributable, reproducible)? Any boundary that crosses data without all three is a finding. "Verifiable + traceable at every boundary" is a first-class audit dimension, not a nice-to-have.

**Sharpening — obscured transitions do the most damage.** The highest-risk boundaries are the ones nobody declared as boundaries: implicit couplings, hand-synced duplicate representations (DB ⇄ JSON register kept in sync manually), steps "applied out-of-band" (the ledger-only `data_migrations` rows where SQL was not re-executed), manual handoffs with no record (PI bump that only goes live when the owner pastes into claude.ai), silent field drops in `convert_*` mappings, and identifiers reused with shifted meaning across layers. A declared boundary can be guarded; an obscured one corrupts the chain with no alarm. So the audit must FIND hidden transitions, not just grade the visible ones — actively hunt for undeclared seams and rank them above cosmetically-imperfect declared contracts.
