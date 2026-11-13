"""Step 1: admission (as the first run), slug links, the owner-supplied search."""
import sys
from common import run, STEM, REF
dry = '--dry' in sys.argv
URL = 'https://www.edmonton.ca/sites/default/files/public-files/assets/PDF/ChecklistAccessibilityUniversalDesign.pdf'
rc, o = run('add-source', '--author', 'corp|City of Edmonton Accessibility Advisory Committee',
            '--institution', 'City of Edmonton Accessibility Advisory Committee',
            '--publisher', 'City of Edmonton', '--publisher-location', 'Edmonton, Alberta',
            '--url', URL, '--url-accessed', '2026-11-13', '--pages', '9',
            '--source-type', 'guideline', '--year', '2022',
            '--title', 'Checklist for Accessibility & Universal Design', '--jurisdiction', 'CA',
            '--evidence-type', 'grey', '--scope', 'intrinsic', '--grey-flag', '1',
            '--grey-reason', 'Municipal advisory committee checklist (City of Edmonton Accessibility Advisory Committee): neither a code, a standard nor a study; supplied by the owner; no DOI.',
            '--doi-resolution-outcome', 'NO-MATCH', '--lang-detected', 'en',
            '--lang-detection-method', 'read on the rendered pages (zero-based indices 0 to 8) and in the text layer',
            '--metadata-quality', 'GREY', '--verification-method', 'direct-render',
            '--verification-status', 'VERIFIED', '--session', STEM, step='add-source', dry=dry)
print('add-source', rc, o[-600:])
if dry:
    sys.exit()
SLUGS = [
 ('stair-ramp-threshold-biomechanics-accessibility', 'Item 6.1 states ramp slopes (1 in 20, a preferred maximum of 1 in 16, 1 in 12 attributed to the Alberta building code) and item 6.2 a 9 m landing interval; item 2.9 a 13 mm threshold rise; item 4.3 stair rise and run.'),
 ('threshold-door-hardware', 'Item 2.3 states doorway clearance (850 mm, 920 mm preferred), 2.4 lever handles, 2.8 an automatic door operator button height, 2.9 a 13 mm threshold rise.'),
 ('accessible-bathroom-and-grab-bar', 'Item 8.6 states the accessible washroom stall (minimum 1700 mm x 1500 mm, toilet height 400 to 460 mm, grab bars, an outward-swinging door); item 8.5 sink, mirror and dispenser heights.'),
 ('reach-range-and-accessible-controls', 'Items 2.8, 5.4, 9.1, 9.3, 9.4 and 9.5 state mounting heights for door buttons, elevator controls, phones, a drinking fountain, a counter and light switches.'),
 ('luminance-contrast-and-pattern', 'The source requires colour contrast at many elements (items 1.2, 2.10, 4.1, 4.7, 5.1, 5.5, 6.4, 7.2, 9.8, 11.2) and states no luminance or reflectance figure for it.'),
]
for s, why in SLUGS:
    rc, o = run('link-source-slug', '--ref-id', REF, '--slug', s, '--rationale', why, '--session', STEM)
    print('slug', s, rc, o.replace('\n', ' ')[:200])
rc, o = run('log-search', '--language', 'EN', '--jurisdiction', 'CA', '--engine', 'owner-supplied',
            '--depth-method', 'scoping', '--origin', 'owner-supplied', '--backfill', '1',
            '--prior-expectation', 'No prior: no search was run. The owner supplied this document; the field is recorded after the document was read and is not a forecast.',
            '--query-text', URL, '--slug', 'stair-ramp-threshold-biomechanics-accessibility',
            '--admitted-ref-id', REF, '--results-found', '1', '--results-screened', '1', '--results-admitted', '1',
            '--findings-note', 'Owner-supplied document admitted as REF-01037; no search was run. The subject slug is given only because log-search demands one (--slug, --parameter or --mined-ref-id) for every row, including --origin owner-supplied (writer defect, first filed as the first run\'s GAP-104 and refiled by this replay). CO1-NOT-APPLICABLE: the document states no co-production by disabled people (it says the City of Edmonton Accessibility Advisory Committee created it) and no Co-1 claim is made; whether such a committee could carry Co-1 standing is the owner\'s open question AQ-5. A Co-1, T2 or Co-2 pass for the topic was not part of this from-evidence run.',
            '--session', STEM, step='log-search')
print('log-search', rc, o[-500:])
