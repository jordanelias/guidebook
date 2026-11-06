# Search log: terminology pass NL/NL (session_2026-11-06-base-vocabulary-review)

Every query and retrieval as run. "Prior" was written before the result. Shape note per R14. Empties kept.

## Instrument derivation (database and registry, read-only)
- D1 `select * from research_code_leads where jurisdiction like '%NL%'`. Prior: one or two Bbl leads. Result: 1 row (lead 98, NEN 9120:2025, REFERENCE-ONLY, "paywalled NEN standard"). No lead names the Bbl itself. Shape: well-formed.
- D2 `select ref_id, pub_title, standard_number, jurisdiction from evidence_sources where jurisdiction in ('NL','BE') or ref_id in ('REF-00995','REF-00996')`. Prior: the Verzamelbesluit and the IPLO page. Result: REF-01020 (Stb. 2024, 368, amending the Bbl), REF-01021 (IPLO "Hellingbaan: regels bij nieuwbouw"), REF-01022 (Ieder(in) consultation reply); REF-00995 and REF-00996 are BE (out of scope, not used). Shape: well-formed.
- D3 `grep -n NL references/standards-registry.md`. Prior: NEN 9120 entries. Result: four NL entries, all NEN 9120 / NEN 1814 / NEN-EN 17210; two say NEN 9120 is "freely available" / "Free to download", contradicting lead 98's "paywalled". No Bbl entry. Shape: well-formed.
- D4 held aliases `select alias, alias_type, jurisdiction, notes from term_aliases where lower(language)='nl'`: 140 distinct; all TRANSLATION/SYNONYM etc., most noted "model-generated 2026-07-25". Treated as seeds only.

## Retrievals
- R1 `fetch https://wetten.overheid.nl/BWBR0041297/2026-01-01`. Prior: HTML of the consolidated Bbl. Result: curl exit 92 (HTTP/2 PROTOCOL_ERROR), 0 bytes, artefact e3b0c44298fc1c14.txt. Manual probes: `--http1.1` gives exit 52 (empty reply); the bare host root also fails; proxy status shows no relay failures. Shape: correct URL; the block is the host's or the path's, not the query's.
- R2 `curl -I https://repository.officiele-overheidspublicaties.nl/bwb/BWBR0041297/`. Prior: the BWB open-data repository serves the same texts as XML. Result: 301 to `manifest.xml`.
- R3 fetch the manifest (artefact c5253a2292d875ee.xml). Prior: an expression in force now. Result: 11 expressions; latest `2026-09-24_0`, einddatum 9999-12-31, so in force on 2026-11-06.
- R4 fetch `.../2026-09-24_0/xml/BWBR0041297_2026-09-24_0.xml` (timeout 240). Prior: about 6 MB XML. Result: 200, 6523883 bytes, artefact 52ef1dbbf8d109ba.xml. Converted with `tools/x2t.py` (BWB XML to located text; first version joined a lid's paragraphs out of order, fixed to document order and re-run before any quote was taken).
- R5 fetch BWB manifest of Bouwbesluit 2012, BWBR0030461 (artefact aaff58a5871b960b.xml). Prior: last expression ends 2023-12-31. Result: 44 expressions, last `2023-09-07_0` ending 2023-12-31. Not in force.
- R6 fetch `.../BWBR0030461/2023-09-07_0/xml/BWBR0030461_2023-09-07_0.xml`. Prior: 200. Result: 200, 5004029 bytes, artefact 56c4f96582c47206.xml; read only for carve comparison.
- R7 fetch `https://www.nen.nl/nen-9120-2025-nl-335193` (URL from standards-registry.md). Prior: a product page with a free-download button. Result: 404 (artefact e1ff5a4301551d4c.html). The registry URL is dead.
- W1 WebSearch `NEN 9120:2025 toegankelijkheid gratis downloaden` (standard). Prior: a NEN Connect link. Result: 15 links incl. connect.nen.nl/standard/detail/3705063 and the ministry page volkshuisvestingnederland.nl/.../toegankelijk-bouwen. The search engine's summary is not a source.
- R8 fetch `https://connect.nen.nl/standard/detail/3705063`. Prior: a registration wall. Result: 404 page with text "This standard is only available when consulted from the Netherlands" and a DRM (Locklizard) viewer notice (artefact fd242f46e9c38fcb.html). NOT-OBTAINABLE from this environment; no account was created.
- R9 fetch the ministry page (artefact 8be21dedbca82962.html). Prior: it states NEN 9120's status. Result: 200; says NEN 9120 is "een vrijwillige norm en aanvulling op de minimumeisen van het Bbl" and free on the NEN site. Text via `tools/h2t.py`.
- Not retrieved: the IPLO page (REF-01021) and Stb. 2024, 368 (REF-01020): both were read by batch 23 and are commentary or amending text; the consolidated Bbl carries their effect.

## Absence checks in the Bbl text (case-insensitive substring counts on text/52ef1dbbf8d109ba.txt; prior written first)
- G1 `drempel` — Prior: absent (the Bbl says hoogteverschil). Result 0. The ministry page does use "drempel".
- G2 `stroef`, `slip`, `glad` — Prior: absent. 0, 0, 0.
- G3 `tactiel`, `noppen`, `ribbel`, `geleidestrook` — Prior: absent (NEN 9120 territory). 0, 0, 0, 0.
- G4 `ringleiding`, `slechthorend`, `auditief`, `akoestisch`, `nagalm` — Prior: absent. All 0. `galm` 2 (art. 4.110 and heading).
- G5 `kleurtemperatuur` — Prior: absent. 0. `kleur` 6, all tunnel doors or building appearance.
- G6 `gang` as a word — Prior: absent; substring hits only in toegang/gangpad. `grep -cw gang` 0.
- G7 `tussenbordes`, `rustbordes` — Prior: absent. 0, 0. `niveauverschil` 5, all inside `lucht-geluidniveauverschil` (acoustics).
- G8 `rolstoel` — Prior: rare. 1 (rolstoelgebruiker, art. 4.181 lid 5). `functiebeperking` 5.
- G9 `wastafel`, `magnetron`, `schakelaar`, `stootbord`, `rooster`, `verkeersdrempel`, `beplanting` — Prior: absent. All 0.
- G10 held NL aliases tested as lower-cased substrings of the Bbl text: 13 of 140 hit; true hits in the register sense are hellingbaan, verkeersroute, vrije doorgang, vrije hoogte, rolstoelgebruiker, geluidsabsorptie, bewegwijzering; `gang` and `rolstoel` are substring artefacts; bouwbesluit, VN-gehandicaptenverdrag, thermisch comfort and oververhitting hit outside the accessibility rules. Parameter-level TRANSLATION aliases (gangbreedte, draaicirkel, bedieningskracht, nagalmtijd, luminantiecontrast, kleurtemperatuur, deurbreedte, hellingspercentage) occur 0 times.
