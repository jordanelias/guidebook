# ICD-11 measured against the four lenses

**Source, retrieved 2026-09-01 and verified, not remembered.**
`https://icdcdn.who.int/static/releasefiles/2026-01/SimpleTabulation-ICD-11-MMS-en.zip`
· 4,214,980 bytes · sha256 `f1356588f40953a83e3af2b662deab47c5e269f944d1ea4ed0cfeb2007c7cd39`
· `Version:2026 Jan 17 - 05:30 UTC` · **37,118 entities**: 28 chapters, 1,360 blocks,
35,664 categories. **No authentication.** Every code and title below is read from that file.

The ICD-API itself (`id.who.int/icd/release/11/2026-01/mms/search`) returns **401** without a
registered bearer token — measured. The release file is the route that needs no credentials, and
it makes an import reproducible offline.

## The owner's example, confirmed

> *"e.g. ICD-11 gives us 'Vision Impairment'"*

| | |
|---|---|
| `BlockL1-9D9` | **Vision impairment** (block, chapter 09) |
| `9D90` | Vision impairment including blindness |
| `9D90.1` / `9D90.2` / `9D90.3` | Mild / Moderate / Severe vision impairment |
| `BlockL1-AB5` | **Disorders with hearing impairment** (block, chapter 10) |
| `AB50` / `AB51` | Congenital / Acquired hearing impairment |
| `BlockL1-8A2` | **Disorders with neurocognitive impairment as a major feature** (chapter 08) |

## THE FINDING: chapter V is a ready-made top-down functioning vocabulary

**Chapter V, "Supplementary section for functioning assessment"**, is the ICF-derived functioning
section *inside* ICD-11 — the Foundation link made concrete in one downloadable file. It holds
three instruments:

| block | non-residual categories |
|---|---|
| WHODAS 2.0 36-item version (`VD*`) | 38 |
| Brief Model Disability Survey (`VE*`) | 8 |
| **Generic functioning domains (`VV*`, `VW*`)** | **44** |

**44 is the number to look at.** Beside this project's 23 identities, 17 access needs and 17
coined axes, it is the same order of magnitude — which is the granularity ruling
(*"roughly correlate to what we have from identity and needs"*) satisfied by a WHO-authored
vocabulary rather than one coined here.

And it reads like this project's own vocabulary, because both are ICF restated:

```
VV10  Seeing and related functions          VV11  Hearing and vestibular functions
VV12  Sensation of pain                     VV00  Energy and drive functions
VV02  Attention functions                   VV91  Handling stress and other psychological demands
VW13  Walking                               VW15  Moving around using equipment
VW11  Transferring oneself                  VW16  Using transportation
VW00  Communicating with - receiving - spoken messages
VW22  Toileting                             VW25  Looking after one's health
VW61  Human rights
```

Compare the project's access needs: `A-NOSIGHT` `A-NOSOUND` `A-REACH` `A-LOWLOAD` `A-EFFORT`
`A-TIME` `A-CALM` `A-STIMULUS` `A-PLAIN` `A-NOSPEECH` `A-PRECISION` `A-SELFCARE` `A-STABLE`
`A-TACTILE` `A-TRIGGER` `A-SIZE` `A-AT`. The overlap is not coincidence — the coined `AX-*` axes
and the `A-*` needs are both hand-made restatements of ICF domains that WHO already publishes.

## What this corrects in my own analysis

I put the medical lens to the owner as **body system (ICD-11 chapters) OR course/shape
("complex")**, and said "complex" is not in ICD-11 at any level. The second half stands; the
dichotomy does not. **ICD-11 carries an impairment tier and a functioning section**, and the
owner's example lands on the first. A reader selecting "Vision impairment" is choosing neither a
chapter nor a course — they are choosing an impairment-level entity that ICD-11 already publishes
at the granularity this project needs.

*"Complex"* is still absent from ICD-11 and from the Foundation. If it is wanted it has to be
authored here, and it is a **separate axis** from anything ICD-11 supplies — not a substitute for
the medical lens, and not a rival to it.

## What is now available without inventing anything

1. **The medical lens** — impairment-tier blocks and categories (`9D90`, `AB50`, `AB51`,
   `BlockL1-8A2` …), each with its Foundation URI, linearisation URI, chapter and browser link,
   straight from the release file.
2. **The ICF lens** — the 44 Generic functioning domains, as a WHO-authored alternative to the 17
   coined `AX-*` axes and the 61 loose ICF codes with no table behind them.
3. **The crossing between them** — *within one file*, because chapter V and the impairment blocks
   share the Foundation. The crossing this project has been hand-authoring in
   `population_axis_map` and `access_need_axis_map` is, for these two lenses, already published.
4. **Reproducibility** — one URL, one sha256, no credentials, no per-request network dependency.

## What is NOT settled, and stays the owner's

- **Which tier the medical lens sits at.** `9D90 Vision impairment including blindness` (category)
  or `BlockL1-9D9 Vision impairment` (block)? Blocks bear no code — the file says so explicitly:
  *"the groupings do not have a code"* — so a block-level vocabulary must key on `BlockId`, not
  `Code`. That is a real schema consequence, not a preference.
- **Whether the ICF lens becomes the 44 WHO domains** and the 17 coined axes are retired, or the
  44 seed a curated subset. Retiring the axes reaches `item_taxonomy_links.icf_code` (158 rows),
  `population_axis_map` (53) and `access_need_axis_map` (21).
- **Whether "complex" gets its own axis** alongside the four lenses.
- **Whether `access_need_icf`'s 15 hand-picked ICF codes** are superseded by the 44, or kept as a
  finer layer beneath them.

## Prior caveat, still standing

Della Mea et al. 2023 maps ICF **Body Structures** (`s` chapter) to ICD-11 Anatomic Detail. This
repo holds **26 b, 25 d, 10 e, zero s**. That paper covers none of our current ICF codes. Chapter V
is a different and directly usable route; the paper is the precedent for the architecture, not a
crossing table for our set.
