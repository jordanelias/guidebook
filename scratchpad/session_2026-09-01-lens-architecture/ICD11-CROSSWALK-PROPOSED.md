# Identity lens → ICD-11, a PROPOSED crosswalk

**Every code and title below is read from the WHO 2026-01 MMS release file**
(sha256 `f1356588f40953a83e3af2b662deab47c5e269f944d1ea4ed0cfeb2007c7cd39`, 37,118 entities).
All 23 candidate codes resolved; none was written from memory.

**THE PAIRINGS ARE PROPOSALS, THE CODES ARE FACTS.** The distinction is the whole point. WHO
authored the entities; *which entity belongs beside which identity* is a judgement nobody has made
yet, and R15 of the research contract says a staged description is a HYPOTHESIS that must be
re-described from the source on resolution. Nothing here is written to the database.

## The tier the owner pointed at

Two owner examples, both verified, and they land on the same tier:

- *"ICD-11 gives us 'Vision Impairment'"* → `BlockL1-9D9` **Vision impairment**, ch 09
- *"Paralytic symptoms, etc"* → `BlockL3-MB5` **Paralytic symptoms**, ch 21, whose children are
  `MB50` Tetraplegia · `MB51`/`MB52` Diplegia upper/lower · `MB53` Hemiplegia ·
  `MB54`/`MB55` Monoplegia upper/lower · `MB56` **Paraplegia** ·
  `MB57` Functional level of injury of spinal cord

That is the **manifestation tier**, and it is *cause-agnostic*: paraplegia from a spinal cord
injury, from MS, or from spina bifida all land on `MB56`. Which is exactly what a design guidebook
needs — the environment meets the manifestation, never the aetiology.

## The crosswalk

| identity | display name | proposed ICD-11 | verified title |
|---|---|---|---|
| `BLIND` | blind and low-vision people | `BlockL1-9D9` · `9D90` | Vision impairment · Vision impairment including blindness |
| `DEAF` | Deaf and hard-of-hearing people | `BlockL1-AB5` · `AB50` · `AB51` | Disorders with hearing impairment · Congenital · Acquired |
| `DEAFBLIND` | DeafBlind people | `BlockL1-9D9` + `BlockL1-AB5` | both of the above — the one identity needing two |
| `SCI` | people with spinal cord injuries | `MB56` · `MB50` · `MB57` | Paraplegia · Tetraplegia · Functional level of injury of spinal cord |
| `LMB` | people with limb differences | `MB54` · `MB55` | Monoplegia of upper / lower extremity |
| `MOB` | disabled people with mobility needs | `MB44` · `BlockL3-MB5` | Abnormalities of gait or mobility · Paralytic symptoms |
| `MOVE` | people with movement disorders | `MB46` · `MB47` · `MB45` | Abnormal involuntary movements · Abnormality of tonus or reflex · Lack of coordination |
| `VES` | people with vestibular disorders | `MB48` | Dizziness or giddiness |
| `EPI` | people with epilepsy | `BlockL1-8A6` | Epilepsy or seizures |
| `BRAIN` | people with acquired brain injury | `BlockL1-8A2` · `MB21` | Disorders with neurocognitive impairment as a major feature · Symptoms involving cognition |
| `DEM` | people living with dementia | `BlockL1-8A2` · `MB21` | as above |
| `PAIN` | people with chronic pain | `MG30` · `MB40` | Chronic pain · Sensation disturbance |
| `COM` | people with complex conditions | `MG22` · `MG30` | Fatigue · Chronic pain |
| `MS` | people with MS | `MB56` · `MG22` | Paraplegia · Fatigue |
| `MH` | people with mental health conditions | `MB24` · `MB22` | Symptoms involving mood or affect · involving motivation or energy |
| `AUT` | autistic people | `6A02` | Autism spectrum disorder |
| `ADHD` | ADHDers | `6A05` | Attention deficit hyperactivity disorder |
| `ID` | people with intellectual disabilities | `6A00` | Disorders of intellectual development |
| `NDV` | neurodivergent people | `6A02` · `6A05` · `6A03` | Autism spectrum disorder · ADHD · Developmental learning disorder |

## THE FINDING, and it is a doctrinal one

**Four identities are the test, and ICD-11 does have codes for three of them — but only by
pathologising the identity.**

| identity | ICD-11 entity that exists | the problem |
|---|---|---|
| `BAR` — fat people; people in larger bodies | `5B81` **Obesity**, ch 05 | The exact framing fat liberation rejects. Coding `BAR` as *Obesity* renames the constituency as a disease. |
| `LPA` — little people; people with dwarfism | `5B11` **Short stature, not elsewhere classified**, ch 05 | Dwarfism communities largely reject a pathology frame; the ICD entry is "not elsewhere classified" — a residual. |
| `TALL` — tall people | `5B12` **Constitutional tall stature**, ch 05 | Tall people are not a clinical population at all. This is anthropometry filed as disease. |
| `ALL` — applies to all populations | none | Correctly none: it is a scope marker, not a population. |

I first recorded these as *having no ICD-11 home*. That was wrong and the correction matters,
because it flips the argument: the problem is not a **gap** in ICD-11, it is that **ICD-11's
answer is available and contested**. Three identities this project serves can be coded medically
only by adopting a frame those communities reject.

**That is the argument for the lens architecture, made by the data.** `D-0182` already rules that a
link may be absent from a lens. Here is why that clause earns its keep: `BAR`, `LPA` and `TALL`
should be able to carry `identity_code` and `needs_code` and leave `medical_code` NULL — not
because nothing exists, but because **choosing not to state it is the correct editorial act** for a
project whose fixed doctrine is a thinking tool centred on disabled people, under CRPD.

A schema that required a medical code would force `BAR` → `Obesity` into the record. The
at-least-one CHECK is what stops that, and it stops it structurally rather than by anyone
remembering.

## What is still owed before any of this is written

1. **The owner rules the tier.** Blocks bear no code — the release file says so in its own readme:
   *"the groupings do not have a code"*. A block-level vocabulary must key on `BlockId`
   (`BlockL1-9D9`), a category-level one on `Code` (`9D90`). Mixing them means the primary key is
   `COALESCE(Code, BlockId)`, which is workable but must be a decision, not a default.
2. **The pairings above need owner review**, one at a time. Several are weak and are flagged rather
   than smoothed: `EPI` → *Epilepsy or seizures* is a diagnosis, not a manifestation, and breaks the
   tier discipline the other rows keep. `MS` → *Paraplegia* is true of some people with MS and false
   of most. `COM` → *Fatigue* + *Chronic pain* under-describes "complex conditions" badly.
3. **`MG2A "Ageing associated decline in intrinsic capacity"`** exists in ch 21 and no identity
   claims it; whether ageing is in scope is doctrine, not schema.
4. Nothing here goes near `base_taxonomy_medical` until 1 and 2 are ruled.
