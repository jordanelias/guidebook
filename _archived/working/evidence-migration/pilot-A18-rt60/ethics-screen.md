# Ethics screen — A-18 (RT60) · A10 nine-vector + Kawa + CRPD

*Ethical grounding is a gate, not a footnote (plan Part V·5). The nine A10 vectors are not mechanically
detectable — this is a reasoned screen. `governance/adversarial-use-framework.md`, project-standards L539.*

> **Corrected** after the adversarial verifier: the first draft called the code/evidence gap "an instance of
> V-01." It is a **susceptibility**, not a demonstrated instance — and ANSI's own Footnote e already
> specifies 0.3 s for hearing-impaired children, so the code does not actually floor them at 0.6 s. Softened
> below.

## A10 nine-vector screen

| vector | exposure for A-18? | reasoning (corrected) |
|---|---|---|
| **V-01 · minimum-compliance weaponization** | **SUSCEPTIBILITY (not an instance)** | *If* a designer applied the code's **general** RT60 minimum (0.6 s, typical-hearing, unoccupied) to a hearing-impaired space while ignoring **ANSI's own Footnote-e 0.3 s provision for HI children**, that would be minimum-compliance misuse. But the code's own population provision guards against it, and no actor is demonstrated — so this is an attack surface the render must foreclose (code shown as ◐ floor, population target ● kept visible), not a live defect. |
| **V-09 · population-proxy denial** | **MODERATE** | Using the Universal value (0.55 s, typical-hearing) to deny the Population value (0.3 s, HI children) because "most occupants hear typically." The population-specific target must survive the presence of a universal one. |
| **V-06 · evidence-tier laundering** | **LOW (well-guarded)** | Risk of presenting code *convergence* as the evidence basis. The DB already guards this: the code values are tagged `echo_of` and never counted as independent evidence. The render must preserve that separation. |
| **V-04 · selective citation** | **LOW–MOD** | Moving the number by citing only the typical-hearing or only the HI-children studies. Mitigated by keeping all four population rows visible. |
| **V-07 · anti-DAR deferral** | **LOW–MOD** | Because acoustic treatment is retrofittable, "we'll fix acoustics later" is an available excuse; the DAR layer must be provisioned now, not used to defer. |
| **V-05 · Co-1 instrumentalization** | **latent** | Co-1 is currently absent; when added it must be a verified pass, never a checkbox endorsing a pre-set number. |
| V-02 · V-03 · V-08 | not evident | RT60 is a physical target with no per-person data capture. |

**Screen result:** the only material exposures are **V-09** and a **V-01 susceptibility** — both defects of
*presentation*, not of the value, and both foreclosed by the plan's walled-off code-floor + anti-laundering
lens + population rows kept distinct. No `ethics-gap` blocks the value.

## Kawa cultural-transfer flag (L405)

- **The RT60 value is physics-based → transfers universally.** Reverberation time is an acoustic-physics
  parameter; the 0.3 s / 0.55 s targets carry across cultures without adaptation. No `kawa-universalized`
  violation in stating them globally.
- **But the spatial-use model does not.** If a provision implies *how* a low-reverberation space is used
  (private retreat vs shared calm), that social/spatial model is culturally specific and needs Person-Mode
  co-design — not universalization. A-18 as written is a pure physical target, so this is a note, not a flag.

## CRPD frame (L383)

CRPD Art. 9 obligates accessible acoustic environments but mandates **obligations, not specifications** — it
does not set 0.3 s. The guidebook fills that gap and must not present 0.3 s as a legal mandate (S2): it is an
evidence-derived best-practice target, with the legal floor (codes) shown separately.
