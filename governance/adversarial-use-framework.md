# Adversarial-Use Framework
**Status:** CANONICAL — A10 Session 1
**Phase:** Stage A Phase 10 — Adversarial-use review framework
**Created:** 2026-04-30 02:11 UTC
**Doctrinal basis:** `workplan/workplan-co0007-v3.md` §A10 (three canonical vectors) · CS9 (cross-stage adversarial-use review) · A4 voice-style §§8.1–8.3 (tier-located authority, mitigation against minimum-compliance weaponization) · A5 §3.4 (synthesis attribution requirement, mitigation against Co-1 instrumentalization) · A6 §2 (evidence-state machine, mitigation against tier laundering) · A7 §3.4 (population variability, mitigation against deficit-list surveillance) · project-standards L20 (no code-only synthesis)

---

## 0. What this document covers and what it does not

A guidebook of accessible-design best practices is information. Information can be misused. This document catalogues identifiable misuse patterns, names the mitigations the project's existing methodology already provides, and specifies a pre-release review gate plus a periodic review cadence. It is not a guarantee that misuse can be prevented — that is not within the project's reach. It is a commitment that misuse vectors are surfaced explicitly, that mitigations are designed in deliberately, and that each release is reviewed against the catalogue before publication.

The document does not attempt to anticipate every possible misuse. It catalogues vectors that have been identified at A10 plus those that fall out cleanly from other phases' work. The catalogue is open — new vectors discovered in Stage B/C, or surfaced in post-launch use, are appended via the standing change-log mechanism (§5.4). The document also does not address misuse of the project's data infrastructure (e.g., scraping the BPC corpus to train models hostile to disabled people); that is a separate concern handled by the data-licensing portion of A11 (legal/regulatory framework).

---

## 1. Canonical adversarial-use vectors (named at workplan-co0007-v3 §A10)

Three vectors were named at workplan-v3 as the project's minimum adversarial-use disclosure. Each is described below in terms of the misuse mechanism, the harm pattern, and the existing project mechanisms that mitigate it.

### 1.1 Minimum-compliance weaponization (V-01)

**Mechanism.** The guidebook publishes specifications above the regulatory floor (Tier 1–5 evidence-based ranges; best-practice synthesis). An adversarial reader cites the guidebook to argue that a Universal Mode (code-floor) compliant design is *adequate because the guidebook acknowledges Universal Mode exists* — using the guidebook's own structure to justify floor-only design. A variant: citing the conditional language of Tier 1 ("range with median default") to argue that the lower bound of the range is acceptable as a default rather than the median.

**Harm.** Disabled people receive code-floor environments where evidence supports better design. The guidebook's existence is used as cover.

**Mitigation in the guidebook's structure.**
- Project-standards Core Doctrine: "Codes are Tier 6 — the compliance floor, not the aspiration." Every code-only specification is explicitly the floor.
- Project-standards L20: a best_practice_synthesis derived solely from code consensus is in error. The guidebook does not offer code values as best practice.
- Voice-style §8.1: Universal Mode specifications cite the code; Tier 1 specifications cite the evidence; Tier 2 specifications locate authority in OT assessment plus the individual. A reader cannot extract a code-floor range while reading the evidence-citing prose.
- Three-tier design hierarchy: Universal Mode is *universal design / code compliance*, never *best practice*. The hierarchy makes the distinction between floor and aspiration unmistakable.

**Mitigation residue.** The mitigations are structural, not absolute. A reader determined to cite Universal Mode as adequate can do so. The mitigation makes that citation visibly inconsistent with the guidebook's own language.

### 1.2 Exclusionary ROI (V-02)

**Mechanism.** The guidebook's Part 11 (Economics of Accessible Construction) catalogues cost data, ROI evidence, and economic arguments for accessibility provisions. An adversarial reader inverts the direction: citing the cost data to argue that a specific provision exceeds an acceptable ROI threshold for the projected disabled population at a site. A variant: using prevalence figures (e.g., "wheelchair users are 1.5% of the population") to argue that population-specific provisions are not warranted at "low-prevalence" sites.

**Harm.** Accessibility provisions are reduced or eliminated based on population-prevalence calculations that disregard the cumulative effect across building lifecycle, the impact of non-provision (people who cannot use the site at all are excluded from prevalence figures by selection effect), and the dignity-rights basis of accessibility (which is not contingent on prevalence).

**Mitigation in the guidebook's structure.**
- Mission-and-epistemics §Mission: accessibility is grounded in CRPD Art. 9 (accessibility) and Art. 5 (equality and non-discrimination), not in cost-benefit analysis. Economic data informs feasibility, not entitlement.
- DAR (Design for Adaptable Readiness) principle: spaces designed for current accessibility plus future adaptability. Cost arguments that defer accessibility to "when needed" are inconsistent with DAR.
- Part 11 framing: economics is presented as *enabling-budget evidence* (these costs are real and manageable), not as *threshold-justifying evidence* (these costs warrant exclusion when above a threshold).
- Population-variability acknowledgment (A7 §3.4): every specification acknowledges that prevalence-at-this-site is the wrong denominator. The right denominator is people-affected-over-the-building's-lifecycle.

**Mitigation residue.** Cost data can always be selectively cited. Part 11 prose declines to offer the threshold-justifying framing; the framing-checker (when run on Part 11) flags any draft that does.

### 1.3 Surveillance via inferred functional needs (V-03)

**Mechanism.** The functional-axes taxonomy (per A7 expanded scope: ambulatory capacity, vision, hearing, cognition, sensory processing) is a navigation aid for design. An adversarial third party — an employer, insurer, landlord, or government — could use the same taxonomy to infer disability status from observable behaviour or environmental needs, and discriminate accordingly. A variant: requiring a person to declare a population code (MOB, VIS, etc.) to access an accommodation, creating a registry.

**Harm.** The guidebook's classifications, designed to inform building design, become a vocabulary for unwanted disability classification of individuals. Accommodation requests become disability disclosures. Surveillance enables discrimination.

**Mitigation in the guidebook's structure.**
- A7 §3.4 (population variability acknowledgment): the guidebook explicitly states that population codes are organising principles, not definitions of people. "A person is not defined by their disabilities."
- A7 §3.3 (one-slug-one-population): the codes apply to specifications, not to people. The taxonomy is for design synthesis, not for personal classification.
- Voice-style §1.3 (specification-tier framing): specifications are about environments, not about people. A reader applying the codes to individuals is using them outside their intended scope.
- The guidebook does not produce a person-assessment instrument. There is no "fill in your population code" form. Tier 2 person-specific design is OT-assessed in confidence, not by population-code inventory.

**Mitigation residue.** The functional-axes taxonomy is publishable knowledge. Anyone can use it for surveillance regardless of the guidebook's intent. The mitigation is that the guidebook does not provide the instrumentation for surveillance — no assessment forms, no person-classification protocols, no datasets of individuals tagged by population code.

---

## 2. Additional vectors identified at A10

Six additional vectors fall out cleanly from prior phase work. They are catalogued at A10 because they share the V-01–V-03 structure (named misuse pattern + identifiable mitigation in existing methodology) and warrant the same review treatment.

### 2.1 Selective citation (V-04)

**Mechanism.** The guidebook's evidence-state machine (A6) records convergence assessment for each cell — convergent, divergent, single-axis, pending. An adversarial reader cites only the evidence supporting their preferred value, ignoring the divergence assessment. A variant: citing a Tier 1 study that supports a value while suppressing the Tier 1 study that contradicts it.

**Mitigation.** A6 §3.2: convergence is recorded explicitly. A divergent assessment names the synthesis_approach. Selective citation is detectable by checking the cited source list against the cell's convergence record.

### 2.2 Co-1 instrumentalization (V-05)

**Mechanism.** Citing a Co-1 source (lived-experience research, DPO position) as endorsement of a design when the source's actual position diverges from the citation. A variant: paraphrasing a Co-1 source in a way that flattens or inverts its argument.

**Mitigation.** A5 §3.4: synthesis_attribution_required field on EvidenceSource. Substantial synthesis from a Co-1 source must declare the synthesis. A5 §6.1: every Co-1 citation carries six required schema fields including verification_status. The verification report (A5 §6.3) records whether the cited claim is faithful to the source.

### 2.3 Evidence-tier laundering (V-06)

**Mechanism.** Claiming Tier 4–5 (international standards / national framework) status for what is properly Tier 6 (statutory code), or claiming Tier 3 (systematic review) for a non-systematic narrative review. The intent: dodge code-floor accountability by relabeling the source.

**Mitigation.** A6 §1: tier and evidence_type are mechanically validated against the source. EvidenceSource.tier is bounded 1–6; EvidenceSource.evidence_type uses the canonical enum. A6 validators check tier-type consistency. Project-standards L20: a Tier 6 source cannot underpin a best_practice_synthesis.

### 2.4 Anti-DAR deferral (V-07)

**Mechanism.** Citing DAR (Design for Adaptable Readiness, Part 10) to defer accessibility: "the building is DAR-ready, we'll add accessibility when needed." This inverts DAR's intent — DAR is current-accessibility *plus* future-adaptability, not future-accessibility *instead of* current-accessibility.

**Mitigation.** Part 10 framing (when written): DAR is additive, not substitutive. The mitigation is in the prose itself; the framing-checker is the validator.

### 2.5 Adversarial litigation citation (V-08)

**Mechanism.** A defendant in a disability-discrimination case cites the guidebook's Tier 2 (person-specific, OT-resolved) language to argue that a contested provision is "discretionary" and the plaintiff's preferences are not entitled. A variant: citing pending/provisional cells to argue the evidence is too thin to compel provision.

**Mitigation.** A11 (legal/regulatory framework, separate phase) addresses this directly. A10's contribution: a front-matter disclaimer on every release explicitly states that the guidebook is design guidance, not legal authority, and that pending/provisional cells reflect synthesis status, not entitlement status.

### 2.6 Population-proxy denial (V-09)

**Mechanism.** The guidebook proxies IntD (intellectual disability) coverage through DEM (dementia, for wayfinding/cognitive simplicity) and NDV (neurodivergence, for sensory environment / Easy Read). An adversarial reader argues that IntD does not need separate advocacy because the guidebook covers it through proxy. The harm: IntD-specific advocacy is undercut by appeal to the guidebook's coverage map.

**Mitigation.** A7 §1.1: the IntD proxy decision is documented, including the rationale (sparse evidence base, substantial functional overlap with DEM/NDV). The proxy is a coverage-strategy admission, not a denial that IntD is distinct. The framing language explicitly states that THIN-BASE disclosure attaches to all IntD-relevant specifications.

---

## 3. Mitigation map

Every catalogue entry maps to one or more mitigations already present in the project's methodology. The map is visible in the catalogue file (`data/adversarial_use/catalog.yaml`) and is checked by the validator (§4) at release.

| Vector | Primary mitigations |
|---|---|
| V-01 minimum-compliance weaponization | project-standards L20, voice-style §8.1, three-tier design hierarchy, evidence-state machine |
| V-02 exclusionary ROI | mission CRPD basis, DAR principle, Part 11 framing, population variability |
| V-03 surveillance via inferred functional needs | A7 §3.4 (codes are organising principles), no person-assessment instrument |
| V-04 selective citation | A6 §3.2 convergence assessment recorded |
| V-05 Co-1 instrumentalization | A5 §3.4 synthesis_attribution_required, A5 §6.3 verification report |
| V-06 evidence-tier laundering | A6 §1 tier-type validation, project-standards L20 |
| V-07 anti-DAR deferral | Part 10 prose framing, framing-checker |
| V-08 adversarial litigation citation | A11 framework + front-matter disclaimer |
| V-09 population-proxy denial | A7 §1.1 IntD proxy rationale, THIN-BASE disclosure |

The map's purpose is to make the existing mitigations legible and to ensure that any change to the methodology that weakens a mitigation surfaces at the next adversarial-use review (a methodology change that removes the convergence assessment record, for example, would weaken V-04's mitigation and trigger reconsideration of V-04 at the next release gate).

---

## 4. Pre-public-release review gate

### 4.1 What the gate does

Before any guidebook version transitions to `ACTIVE` (per A9 GuidebookVersionStatus), a release-gate review is conducted. For each catalogue entry, a reviewer records: (a) whether the version's prose, structure, and data introduce new exposure to that vector; (b) whether the vector's named mitigations remain operative in the version; (c) whether new mitigations were added or existing ones were weakened. The output is a YAML record per (version × vector) pair, stored under `data/adversarial_use/review_log/{version_tag}.yaml`.

### 4.2 What the gate does not do

The gate does not prove the absence of misuse. It does not prevent misuse. It does not produce a misuse-impossibility certification. It is a structured pre-release review against a known catalogue; misuse vectors not yet in the catalogue are not detected.

### 4.3 Reviewer composition pre-launch

Pre-launch (per A5 §1, current state) the reviewer is the solo author. The review is documented as `reviewer: solo_author_pre_launch` in the review_log entry. Post-launch, the review may engage external reviewers; that change to reviewer composition is itself a post-launch decision, not specified in this document.

### 4.4 Validator behaviour at the gate

The validator (`scripts/audit_adversarial_use.py`) enforces three checks at release gate:

| Check | Severity | Description |
|---|---|---|
| Catalogue well-formed | ERROR | Every entry in `data/adversarial_use/catalog.yaml` has all required fields and resolves to schema |
| Review coverage complete | ERROR | The version being released has a `review_log/{version_tag}.yaml` entry for every catalogue vector |
| Review entries well-formed | ERROR | Each review entry has reviewer, date, status (one of `cleared`, `cleared_with_notes`, `escalate`), and notes (required when status ≠ `cleared`) |

A release that fails any of these is blocked at CI. A release whose review_log records `escalate` for any vector requires explicit author override (a `release_override.yaml` record acknowledging the unresolved escalation), which surfaces in the release notes.

---

## 5. Periodic review cadence (CS9)

### 5.1 Per-release review

Each release runs the §4 pre-release gate. The output is committed alongside the version in `data/adversarial_use/review_log/`.

### 5.2 Stage C review (when reached)

During Stage C, a periodic adversarial-use review runs at a cadence to be set when Stage C begins. The roadmap currently specifies "periodic review during Stage C" without a fixed interval; that interval is set at the Stage C kickoff, with the catalogue and accumulated review_log as input.

### 5.3 Catalogue extensions

When a new vector is identified — by an author, by a reviewer, by external feedback, by Stage C use observation — it is appended to the catalogue with a new vector_id (V-NN). The vector's first review_log entry must cover all currently-active and in-prep guidebook versions retroactively, to confirm whether the version is exposed to the newly-identified vector. Retroactive entries are tagged with `retroactive: true`.

### 5.4 Standing change log

Changes to the catalogue (new vectors, retired vectors, mitigation reassignments) are recorded in `governance/adversarial-use-framework.md` §6 (Status). The doctrine-recheck phase (A13) audits the change log against the validator behaviour to confirm the framework remains operative.

---

## 6. Validator specification (`scripts/audit_adversarial_use.py`)

### 6.1 Scope

The script enforces the §4.4 checks and produces a release-gate report. It is run in CI alongside other validators. It does not perform automated misuse detection — most vectors are not mechanically detectable, and pretending otherwise would create a false-confidence failure mode.

### 6.2 Inputs

| Path | Purpose |
|---|---|
| `data/adversarial_use/catalog.yaml` | Vector catalogue (single file, schema MisuseVectorCatalog) |
| `data/adversarial_use/review_log/{version_tag}.yaml` | Per-version review log (one file per guidebook version) |
| `data/temporal/guidebook_versions/*.yaml` | Active and prep version records (from A9) — used to determine which versions need review_log coverage |

### 6.3 Outputs

A report printed to stdout. Exit codes: 0 = pass, 1 = errors, 2 = config error.

### 6.4 CLI

| Flag | Behaviour |
|---|---|
| `--catalog-only` | Validate only the catalogue file format; skip review-coverage checks |
| `--version VERSION_TAG` | Validate review coverage only for the named version (default: every ACTIVE or IN_PREP version) |
| `--report` | Print summary; exit 0 always |

---

## 7. Status

| Field | Value |
|---|---|
| Created | 2026-04-30 02:11 UTC |
| Phase | Stage A Phase 10 (Adversarial-use review framework) — Session 1 |
| Status | CANONICAL |
| Catalogue version | 1 (V-01 through V-09) |
| Forward dependencies | `audit_adversarial_use.py` (this session); A11 (front-matter disclaimer wording for V-08); A13 (doctrine-recheck) |
| Schema dependencies | `schemas/adversarial_use.py` (new); `schemas/enums.py` (extended) |

### 7.1 Change log

| Date | Change |
|---|---|
| 2026-04-30 02:11 | Initial canonical version. V-01 through V-09 catalogued. |

---

**End of A10 governance document.**
