# Pass record — terminology pass KO/KR, session_2026-11-06-base-vocabulary-review

**Verdict.** The two principal instruments are retrieved from law.go.kr and read in full in Korean, apart from their figures. They are the Enforcement Rule's 별표 1 (detailed structural and material standards) and the Enforcement Decree's 별표 2 (facility types and installation standards by building class), plus the Decree's 별표 1 (target facilities) and the Rule's 별표 2 (signage). The Act, Decree and Rule bodies are read in part. The held source REF-01031 is the current 별표 1: the in-force Rule (2026-07-02) links byte-identical bytes, still stamped <개정 2023. 12. 11.>. Of the 75 register concepts, 45 are FOUND, 16 FOUND-PARTIAL and 14 SEARCHED-ABSENT. The reverse harvest has 106 phrases the register lacks. Every quote verifies in the saved text (whitespace-stripped). Nothing was written to the DB, committed or pushed. SEARCHED-ABSENT means absent from these texts, not from Korean law: the BF certification criteria, KS standards and the transport-mobility act were not read.

## Retrieved and read (detail per instrument: instruments.tsv; every request: search-log.md)
- R1 시행규칙 [별표 1], 22 pp., sha256 b71c64f1…: items 1, 4–22, 27–29 and 비고 read; items 2, 3, 23–26 are 삭제. [SKIPPED: every 아래의 그림 figure (images).]
- D2 시행령 [별표 2] <개정 2024. 9. 19.>, 10 pp.: read in full. The 의무/권장 matrix was read for its structure only, because its extracted columns do not align, and no finding rests on a matrix cell.
- D1 시행령 [별표 1], 4 pp.: read in full. R2 시행규칙 [별표 2], 1 p.: text read. [SKIPPED: the 작도법 drawing.]
- ACT (in force 2025-12-21): arts 1–9 and 14–17 read. DEC (2026-01-02): arts 1–5의2, 7 and 7의2 read. RUL (2026-07-02): arts 1–8 read. The rest is skipped (administration, penalties, 부칙): see instruments.tsv.
- Not read: the 장애물 없는 생활환경 인증 criteria (named in Act art 10의2; not attempted, budget), the Decree's 별표 2의2–2의4 and the Rule's 별표 3, KS standards (no KS number occurs in the seven texts), and 교통약자의 이동편의 증진법 (roads and transport).
- Route: the `법령/<name>` path returns an iframe shell. Its `lsInfoP.do` target is a JS skeleton. The AJAX endpoint `lsInfoR.do` answers a plain GET with the full body, and that body lists `flDownload.do?flSeq=` PDF links for every annex. Wayback was not needed. Four of 13 requests failed once with curl exit 35 (TLS) and succeeded on retry.

## Counts (re-run, do not trust; from the repo root, D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/KO-KR)
- Rebuild and verify: `python3 -I $D/build.py`. It exits 1 on any unverified quote, unknown concept, missing absence note or artefact-hash mismatch. At writing it gave 69 observations, 106 reverse-harvest rows, 10 seeds and 0 failures.
- Coverage: `cut -f3 $D/coverage.tsv | sort | uniq -c` gives 45 FOUND, 16 FOUND-PARTIAL, 14 SEARCHED-ABSENT. The register is derived in build.py: 32 rows from catalogue 2.1, 18 from 2.2, 10 from base_parameters and 15 B651 headings marked RHFAC-does-not-name.
- Distinct observed phrases: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gives 69. Rows by instrument: `awk -F'\t' 'NR>1{split($4,a," ");print a[1]}' $D/observations.tsv | sort | uniq -c` gives R1 63, D2 5, R2 1.
- Independent check: 133 of 137 R1 quotes are `scoped` under `retrieval_log.locate_quote(q, ref_id='REF-01031')`, which searches batch 23's PyMuPDF text (search-log G3).
- Held KO aliases found in the texts: 12 of 156 distinct (search-log G2). None of the parameter-level aliases occurs.

## Where Korean carves the field differently (instrument-derived; glosses ours)
1. **Turning is a square, never a circle.** Turning space is "1.4미터×1.4미터 이상의 활동공간" (or 1.5 × 1.5). Elsewhere it is "휠체어가 회전할 수 있는 공간" with no number, or a turn named by its angle (180도). The words 회전반경, 지름 and 원 never appear for this. 활동공간 (activity space) is one word that covers approach, turning, side transfer and landing space.
2. **Tread is a width and the step is two elements.** The text gives "디딤판의 너비" and "챌면의 높이", and a separate riser-angle rule, "챌면의 기울기 … 60도 이상". Open risers are excluded by a positive duty: "챌면을 반드시 설치".
3. **One word, 손잡이, covers handrail, grab bar and door handle.** Only the host element fixes the sense. 수평손잡이 is a stair extension and also a toilet grab bar.
4. **Contrast is colour difference, never luminance.** The texts say "색상과 질감은 … 다르게", "바닥재의 색상과 비슷하여 구별하기 어려운 경우에는 다른 색상", and that tactile tiles are yellow by default. 휘도, 명도 and 반사율 do not occur.
5. **Force and reverberation are absent.** Doors are controlled by time ("닫히는 시간이 3초 이상") and by "가벼운 재질". The only acoustic quantity is "주변소음도 75데시벨", which exempts telephones.
6. **Ramp length gives way to rise.** Landings come "높이 0.75미터 이내마다", and "경사로의 길이" appears only as a handrail trigger (1.8 m). A steeper 1/8 ramp is allowed only for existing buildings when "상시보조서비스" is provided, so staffing is a compliance condition.
7. **Width is split by object.** 유효폭 is used for routes, corridors and stairs. 통과유효폭 is used for doors and is paired with "전면 유효거리". Lift cars, WCs and showers use 유효바닥면적 (폭 × 깊이). The corridor and passage are one object, "복도 및 통로". The exterior route, 접근로, is defined by its end points.
8. **The drafting is two-tier and sorted.** The Rule's 비고 rules that every "할 수 있다" item is a 권장사항 (recommendation). The Decree's matrix marks each facility type 의무 or 권장 per building class, under five categories: 매개시설, 내부시설, 위생시설, 안내시설 and 그 밖의 시설. Applicability turns on use and "바닥면적의 합계", and new builds are split from existing ones (신축 / 기존시설). There are three compliance routes outside the prescriptions: 적용의 완화 (approved relaxation), "세부기준보다 안전하고 편리한 대안", and 시험적용.
9. **One statutory user class.** "장애인등" means 장애인ㆍ노인ㆍ임산부 등. The annexes name specific users where it matters: 저시력인, 난청자, 경기용 휠체어 사용자, 보행곤란자, 동행인. Korean-specific objects include "온돌방보다 침대방", 수유실 and 기저귀교환대, and 영유아용 거치대.
10. **Illuminance is regulated only at lifts** ("최소 150LX"). Shelter applies only to exterior ramps (지붕과 차양). Edge protection is "추락방지턱 또는 측벽".

## Defects found in the METHOD
- D1. The register's near-duplicates recur here, as in FR and JA. C02, C11 and C14 share one formula ("미끄러지지 아니하는 재질로 평탄하게 마감"), so FOUND is inflated.
- D2. The sanctioned verifier cannot read PDFs. `locate_quote` returns `missing` for every quote from the four PDFs, so D2, D1 and R2 rest on build.py alone. Whitespace-stripped matching was necessary because pdftotext breaks lines inside words. It is also slightly permissive, because it could join across a word boundary.
- D3. Table extraction interleaves cells. In D2 the label column cuts the rule text, and the 의무/권장 matrix splits each cell vertically (의/무). Several quotes had to stop at cell breaks, and the matrix is unquotable.
- D4. The held KO parameter aliases (경사로 기울기, 복도 폭, 문 폭, 회전 공간, 조작력, 잔향 시간, 휘도 대비, 색온도) occur in no text read. Each is a word-for-word rendering of the English, which is the OR-12b failure. The instrument says 경사로의 기울기, 복도의 유효폭 and 통과유효폭.
- D5. The instrument list is not derivable. research_code_leads holds no KR lead, and standards-registry.md gives only the portal root plus an unverified claim about a 2024 "daily life access" shift. The list came from the Act's own delegation chain (art 8 → Decree 별표 2, Rule 별표 1/2).
- D6. The search-log priors for the grep batch were written after the run, not before. This is corrected in the log and is weaker than R14 asks.
- D7. Spacing varies inside one instrument: "수평면으로된" / "수평면으로 된", and "높이차이" / "높이 차이". Exact-string attestation would split them unless spacing variants are folded.

## Self-attack: the five likeliest ways this record is wrong
1. **Figures unread.** R1 refers to about 15 drawings ("아래의 그림과 같이"), and R2 has a drawing. A term or a turning-circle diagram that lives only in an image is missed, so "never a circle" holds for the text only.
2. **Concept mapping is my judgment.** For example: 활동공간 → clear space for approach, 수납공간 → lockers, 보행장애물 → B651 4.5, 손잡이 → handrails. Some FOUND rows may be wider or narrower than marked.
3. **Currency rests on today's portal state.** The in-force dates come from the bytes' own headers. An amendment that is promulgated but not yet in force (ancYnChk=1) was not checked.
4. **Locators were assigned by hand.** Item, 목 and (n) numbers come from my reading. Only the PDF page is computed. A 목 letter could be off where the PDF layout breaks a heading from its clause.
5. **Absence is scoped to seven texts.** Drainage, force, reverberation, colour temperature, bollards and speed bumps may sit in the BF certification criteria, KS standards or the transport-mobility act, none of which were read. Coverage for KR is not exhausted.
