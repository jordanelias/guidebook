# Equivalents record — KO/KR (session_2026-11-06-base-vocabulary-review)

**Verdict.** I covered the three owner classes in Korean with attested forms from tiers 1, 2 and 4. Tier 3 (signage manuals) and tier 5 (disabled people's organisations) gave nothing I could retrieve. I attempted 20 of the 560 register-v2 concepts, chosen for the owner classes and for forms a second reading of the held texts turned up. Every quote checks against the bytes fetched (search log, "Verification"). Nothing was written to the DB, committed or pushed.

**Concepts attempted** (`cut -f1 equivalents.tsv | tail -n +2 | sort -u`): R2-050, R2-208 (parking and its markings), R2-333 (the umbrella qualifier), R2-163 to R2-166 and R2-168 to R2-171, R2-174, R2-175 (vertical transport), and R2-005, R2-074, R2-083, R2-093, R2-094, R2-176, R2-314 (variants met on the way). **Not attempted:** the other 540, including most of the first pass's FOUND rows (slope, handrails, landings, contrast). R2-051 (a second bay class) and R2-053 (access aisle) had no Korean form in these texts.

**Counts** (re-run; do not trust): by usage type, `cut -f6 equivalents.tsv | tail -n +2 | sort | uniq -c` gives code term 43, colloquial 9, qualifier 9, regional variant 5, outdated 3, product name 2, seed 3. By tier, `cut -f8 … | uniq -c` gives tier 1: 28, tier 2: 25, tier 3: 0, tier 4: 18, tier 5: 0, seed: 3. Distinct forms: `awk -F'\t' 'NR>1{print $3}' equivalents.tsv | sort -u | wc -l` gives 61. Rows with a conflation note: `awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l` gives 15.

**The owner classes in Korean**
- *Parking.* The code term is 장애인전용주차구역 (Act art 17; R1 제4호; the transport annex). Variants:
  - 장애인전용 주차구역 and 장애인 전용주차구역 (spacing only).
  - The parking law's 장애인 전용주차구획 (구획 where the other laws say 구역).
  - Colloquial: 장애인주차구역, 장애인 주차구역, and 장애인자동차전용주차구역 (Incheon).
  - The permit is now 장애인전용주차구역 주차표지. Its old name, 장애인자동차표지, was replaced by the Act's 부칙, but a district menu still uses it.
  - In every source, the bay is named by user group and reservation (장애인, 전용), never by an umbrella adjective.
- *Umbrella qualifier.* There is no one adjective. The statute's umbrella is a noun class: 편의시설 (accessibility law) or 이동편의시설 (transport law), keyed to a user class (장애인등, 교통약자). For a route or room, the code writes clauses: 장애인등의 통행이 가능한 / 이용이 가능한. The prefixes 장애인용, 장애인전용 and 휠체어사용자용 are narrower. 접근가능한 occurs once, meaning only "reachable". The certification is 장애물 없는 생활환경 (BF, "Barrier Free"). Seoul's ordinance defines 유니버설디자인 for all citizens, which is wider. The city uses 무장애 for tourism. 배리어프리 occurred in none of the 17 texts read, so it is an unattested seed.
- *Vertical transport.* 승강기 is the lift-safety law's class word, covering 엘리베이터, 에스컬레이터 (including 무빙워크) and 휠체어리프트. In the accessibility law, the elevator is 장애인용 승강기. 엘리베이터 is defined over a vertical or inclined path. 휠체어리프트 covers both 수직형 (the platform lift) and 경사형 (the stair lift). Use subtypes include 승객용, 장애인용 and 주택용 엘리베이터.

**Conflations, recorded and not settled** (all 15 are in column 12). The strongest: 장애인용 승강기 is an elevator in the accessibility rule (R1 제9호), but the 장애인용 경사형 휠체어리프트 in the lift-safety rule (art 68). Also:
- 승강기 is the class in one law and the car lift in another.
- One transport annex says 승강기 for stations and 엘리베이터 for ships.
- 승강장 is a lift landing, a wheelchair-lift landing and a station platform.
- 승강설비 covers both vertical transport and bus boarding devices.
- 휠체어 리프트 also names a bus lift.
- 구역 and 구획 name one bay.
- 점자블록 says "braille" for tactile paving.
- 무빙워크 is filed under 에스컬레이터.

**Not obtained:** the MOLIT mobility-facility manual page (TLS failed twice; Wayback not tried); any DPO page (searches returned news only, which is excluded); the BF evaluation-item 고시; the art 3 bay-size table in 주차장법 시행규칙; road-sign annexes (not attempted).

**Self-attack**
1. Tier 5 is empty, so the community's own forms and the forms it rejects are missing. News suggests 리프트 is a contested word in the subway-access campaign, but I could not attest it.
2. Some spacing variants come from pdftotext. 통과 유효폭 in the transport annex could be a glyph-gap artefact rather than printed spacing. Check against the HWP or a rendered page.
3. Article, item and 목 locators are hand-set. Two were wrong on the first build (제29호 for 제27호; 제5호 for 제6호) and were corrected. Others may still be off.
4. Tier-4 sources are uneven. The mediahub tourism piece is a citizen reporter's article on a city site. The Incheon page dates from 2016 and cites superseded clause numbers.
5. Sense judgments are mine. Examples: 편의시설 as the umbrella, 운반구 as the cab, 경사판 under Ramp. Each has a scope note, but none was cross-checked by a second reader.
