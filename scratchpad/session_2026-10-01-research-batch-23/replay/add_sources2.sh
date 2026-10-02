set -u
cd /home/user/guidebook
SCR=/tmp/claude-0/-home-user-guidebook/5b214a57-ade4-5889-9a78-ce2de4360478/scratchpad
SESSION=session_2026-10-01-research-batch-23
TODAY=2026-10-01
SLUG=accessible-circulation-geometry
DB() { GUIDEBOOK_DB_PATH="$SCR/batch23.db" python3 scripts/db.py "$@"; }

echo "== REF-01023 SE BFS 2024:12"
DB add-source --ref-id REF-01023 --author "corp|Boverket" --year 2024 \
 --title "Boverkets föreskrifter om byggnaders tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga" \
 --series "Boverkets författningssamling" --series-number "BFS 2024:12" \
 --tier 6 --evidence-type code --jurisdiction SE --source-type code \
 --url "https://rinfo.boverket.se/BFS2024-12/pdf/BFS2024-12.pdf" --url-accessed $TODAY \
 --pages "2 kap. 4 § (PDF p. 4 of 9); ikraftträdande 1 juli 2025 (PDF p. 9)" \
 --metadata-quality COMPLETE-STATUTORY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected sv --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id SE-01 --session $SESSION 2>&1 | tail -3

echo "== REF-01024 SE ALM 2"
DB add-source --ref-id REF-01024 --author "corp|Boverket" --year 2011 \
 --title "Boverkets föreskrifter och allmänna råd om tillgänglighet och användbarhet för personer med nedsatt rörelse- eller orienteringsförmåga på allmänna platser och inom områden för andra anläggningar än byggnader" \
 --series "Boverkets författningssamling" --series-number "BFS 2011:5 (ALM 2)" \
 --tier 6 --evidence-type code --jurisdiction SE --source-type code \
 --url "https://www.varberg.se/download/18.2b514d9b18a92e6fafc230fb/1387272663974/BFS2011-5-ALM2.pdf" --url-accessed $TODAY \
 --pages "8 § och 9 § Allmänt råd (PDF p. 4 of 8)" \
 --metadata-quality COMPLETE-STATUTORY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected sv --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id SE-02 --session $SESSION 2>&1 | tail -3

echo "== REF-01025 SE FUB"
DB add-source --ref-id REF-01025 --author "corp|Riksförbundet FUB (För Utvecklingsstörda Barn, Ungdomar och Vuxna)" --year 2007 \
 --title "Yttrande över Boverkets remiss ang. Revidering av Boverkets byggregler avsnitt 3 och 8 med följdändringar i avsnitt 1 och 6" \
 --tier 3 --evidence-type grey --jurisdiction SE --source-type grey \
 --grey-flag 1 --grey-reason "consultation reply (remissvar) to a government agency by a rights organisation, dated Stockholm 2007-01-10; not peer-reviewed; no DOI; hosted on the organisation's own site" \
 --url "https://www.fub.se/files/bilagor/b8_fs_1-07_boverket.pdf" --url-accessed $TODAY \
 --pages "3:1222 (PDF pp. 2-3 of 7)" \
 --metadata-quality GREY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected sv --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id SE-03 --session $SESSION 2>&1 | tail -3

echo "== REF-01026 PT"
DB add-source --ref-id REF-01026 --author "corp|Portugal" --year 2006 \
 --title "Decreto-Lei n.º 163/2006 de 8 de Agosto — Aprova o regime da acessibilidade aos edifícios e estabelecimentos que recebem público, via pública e edifícios habitacionais, revogando o Decreto-Lei n.º 123/97, de 22 de Maio" \
 --tier 6 --evidence-type code --jurisdiction PT --source-type code \
 --publisher "Ordem dos Arquitectos (transcription hosted; not the Diário da República original)" \
 --url "https://ordemdosarquitectos.org/backend/uploads/decretolei_163_2006_a8acccc42f.pdf" --url-accessed $TODAY \
 --pages "Anexo, secção 2.5 Rampas, n.os 2.5.1-2.5.2 (PDF pp. 20-21 of 41)" \
 --metadata-quality GREY --verification-status UNVERIFIED \
 --lang-detected pt --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id PT-01 --session $SESSION 2>&1 | tail -3

echo "== REF-01027 ES DB-SUA"
DB add-source --ref-id REF-01027 --author "corp|Ministerio de Vivienda y Agenda Urbana" --year 2024 \
 --title "Documento Básico SUA Seguridad de utilización y accesibilidad (con comentarios del Ministerio)" \
 --series "Código Técnico de la Edificación" --series-number "DB-SUA, versión con comentarios de 15 julio 2024" \
 --tier 6 --evidence-type code --jurisdiction ES --source-type code \
 --url "https://www.codigotecnico.org/pdf/Documentos/SUA/DccSUA.pdf" --url-accessed $TODAY \
 --pages "SUA 1, apartado 4.3.1 Pendiente (PDF p. 27 of 79); historial de modificaciones y versiones (p. 2)" \
 --metadata-quality COMPLETE-STATUTORY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected es --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id ES-01 --session $SESSION 2>&1 | tail -3

echo "== REF-01028 ES TMA/851/2021"
DB add-source --ref-id REF-01028 --author "corp|Ministerio de Transportes, Movilidad y Agenda Urbana" --year 2021 \
 --title "Orden TMA/851/2021, de 23 de julio, por la que se desarrolla el documento técnico de condiciones básicas de accesibilidad y no discriminación para el acceso y la utilización de los espacios públicos urbanizados" \
 --series "BOE" --series-number "BOE-A-2021-13488" \
 --tier 6 --evidence-type code --jurisdiction ES --source-type code \
 --url "https://www.boe.es/eli/es/o/2021/07/23/tma851/con" --url-accessed $TODAY \
 --pages "artículo 14 Rampas, apartado 2 c); BOE núm. 187, de 06/08/2021; entrada en vigor 02/01/2022" \
 --metadata-quality COMPLETE-STATUTORY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected es --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id ES-02 --session $SESSION 2>&1 | tail -3

echo "== REF-01029 ES CERMI Madrid"
DB add-source --ref-id REF-01029 --author "corp|CERMI Comunidad de Madrid" --year 2018 \
 --title "Metodología para la evaluación e implementación de Accesibilidad Universal en espacios públicos de la ciudad de Madrid" \
 --tier 3 --evidence-type grey --jurisdiction ES --source-type report \
 --grey-flag 1 --grey-reason "report authored by a disability-sector umbrella platform (CERMI Comunidad de Madrid), dated 'Madrid, diciembre de 2018', with municipal support credited on the last page ('Con el apoyo de'); not peer-reviewed; no DOI; hosted on the Ayuntamiento de Madrid site" \
 --url "https://www.madrid.es/UnidadesDescentralizadas/Discapacidad/publicaciones/MetodologiaAccesibilidadEspaciosPublicos/metodologiaaccesibilidadespaciospublicos.pdf" --url-accessed $TODAY \
 --pages "pp. 10 (3.2 Condiciones orográficas) and 24 (Pendientes longitudinales máximas), of 68" \
 --metadata-quality GREY --verification-status VERIFIED --verification-method direct-render \
 --lang-detected es --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id ES-03 --session $SESSION 2>&1 | tail -3

echo "== REF-01030 FR DHUP guide"
DB add-source --ref-id REF-01030 \
 --author "corp|Ministère de la Cohésion des territoires et des Relations avec les collectivités territoriales" \
 --author "corp|Ministère de la Transition écologique et solidaire" --year 2019 \
 --title "Guide illustré — Accessibilité des établissements recevant du public et installations ouvertes au public existants" \
 --tier 5 --evidence-type national_fw --jurisdiction FR --source-type guideline \
 --url "https://www.ecologie.gouv.fr/sites/default/files/publications/2019%2007%20guide_DHUP_erp-existants.pdf" --url-accessed $TODAY \
 --pages "B-2 Cheminements extérieurs, 2° a) Profil en long — Pentes (Arrêté du 8 décembre 2014, art. 2), PDF p. 12 of 65" \
 --metadata-quality COMPLETE --verification-status VERIFIED --verification-method direct-render \
 --lang-detected fr --lang-detection-method native_title_verified \
 --slug $SLUG --local-ref-id FR-01 --session $SESSION 2>&1 | tail -3
