set -u
cd /home/user/guidebook
SCR=/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad
SESSION=session_2026-10-01-research-batch-23
TODAY=2026-10-01
SLUG=accessible-circulation-geometry
DB() { GUIDEBOOK_DB_PATH="$SCR/batch23.db" python3 scripts/db.py "$@"; }

echo "== REF-01019 KR"
DB add-source --ref-id REF-01019 --author "corp|Republic of Korea" --year 2023 \
 --title "장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행규칙 [별표 1] <개정 2023. 12. 11.> 편의시설의 구조·재질등에 관한 세부기준 (제2조제1항관련)" \
 --tier 6 --evidence-type code --jurisdiction KR --source-type code \
 --url "https://www.nepla.ai/wiki/복지와-건강/사회복지/-유권해석-장애인-노인-임산부-등의-편의증진-보장에-관한-법률-시행규칙-별표-1-편의시설의-구조·재질등에-관한-세부기준-제2조제1항관련-1509xgx0mnol" \
 --url-accessed $TODAY --pages "별표 1 제12호 경사로 나목 기울기, (1)-(2)" \
 --metadata-quality GREY --verification-status UNVERIFIED \
 --lang-detected ko --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id KR-01 --session $SESSION 2>&1 | tail -3

echo "== REF-01020 NL Staatsblad"
DB add-source --ref-id REF-01020 --author "corp|Koninkrijk der Nederlanden (Staatsblad)" --year 2024 \
 --title "Besluit van 25 november 2024 tot wijziging van het Besluit bouwwerken leefomgeving in verband met de uitbreiding van de verplichting van CO2-meters in scholen, wijziging van de regels voor droge blusleidingen en toegankelijkheidseisen van gebouwen en verduidelijking van de regels voor vergunningplichtige gevallen bouwactiviteit en vergunningvrije gevallen omgevingsplanactiviteit (Verzamelbesluit Besluit bouwwerken leefomgeving 2024)" \
 --tier 6 --evidence-type code --jurisdiction NL --source-type code \
 --series "Staatsblad" --series-number "2024, 368" \
 --url "https://zoek.officielebekendmakingen.nl/stb-2024-368.pdf" --url-accessed $TODAY \
 --pages "Artikel I onderdeel R (art. 4.30), PDF pp. 5-6; nota van toelichting onderdeel R, p. 35; Artikel II (inwerkingtreding 1 juli 2025)" \
 --metadata-quality COMPLETE-STATUTORY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected nl --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id NL-01 --session $SESSION 2>&1 | tail -3

echo "== REF-01021 NL IPLO"
DB add-source --ref-id REF-01021 --author "corp|Informatiepunt Leefomgeving (IPLO)" --year 2026 \
 --title "Hellingbaan: regels bij nieuwbouw" \
 --tier 5 --evidence-type national_fw --jurisdiction NL --source-type guideline \
 --url "https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/hellingbaan/" --url-accessed $TODAY \
 --pages "Helling, Tabel: steilte hellingbaan (artikel 4.30 Bbl)" \
 --metadata-quality COMPLETE --verification-status VERIFIED --verification-method direct-render \
 --lang-detected nl --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id NL-02 --session $SESSION 2>&1 | tail -3

exit 0
echo "== REF-01022 NL Ieder(in)"
DB add-source --ref-id REF-01022 --author "corp|Ieder(in)" --year 2023 \
 --title "Internetconsultatie verzamelbesluit Bbl 2024 (reactie van Ieder(in), 9 november 2023, ref. 23-0915/AvdV/SvK)" \
 --tier 1 --evidence-type co1 --jurisdiction NL --source-type letter \
 --co1-provenance "Organisational authorship, evidenced in the retrieved bytes (D-0178): the letter names its author as 'Ieder(in), het netwerk van mensen met een beperking of chronische ziekte' (the network of people with a disability or chronic illness) and is signed by its director, Illya Soffer, as a reply to the Dutch government's internet consultation on the Verzamelbesluit Bbl 2024 -- a CRPD Art 4.3-type consultation output. LIMIT: no individual disabled author or consulted member is named in the letter, so what is evidenced is organisational standing, not participatory production of the ramp position; Ieder(in) speaks for people with any disability or chronic illness, not specifically for wheelchair users." \
 --co1-source-type dpo_position_statement \
 --url "https://internetconsultatie.nl/verzamelbesluit_bouwwerken_leefomgeving_2024/reactie/237535/bestand" --url-accessed $TODAY \
 --pages "p. 1 (bullet 3, hellingbanen / NEN 9120)" \
 --metadata-quality GREY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected nl --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id NL-03 --session $SESSION 2>&1 | tail -3
