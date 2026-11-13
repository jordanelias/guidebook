"""Steps 7 (search harm flag), 9 (leads, mining) and 10 (population match)."""
from common import run, STEM, REF

def show(label, rc, o):
    print(label, rc, o.replace('\n', ' ')[-260:])

show('harm', *run('amend-search', '--exec-id', '204', '--set-harm-finding', '--append-note',
     'R7: the source states harms tied to no parameter: item 1.5 "The more painted surface, the more likely pavement will become slippery", item 4.5 "to alert a potential safety hazard", item 8.2 "so persons who are blind do not become disoriented". Each is held as an observation; one GAP names the three (replay of the digest).',
     '--session', STEM))
LEADS = [
 ('https://www.edmonton.ca/sites/default/files/public-files/assets/PDF/AFE-AccessDesignGuide.pdf', 'Access Design Guide',
  'REF-01037 PDF p. 1, hyperlink on the words Access Design Guide (read from the PDF link annotation)',
  'Named by the source as the City of Edmonton best-practice resource. A lead only: not retrieved, not read.'),
 ('https://ebs.safetycodes.ab.ca/documents/webdocs/PI/Barrier-Free-Design-Guide_WEB-Aug2019.pdf', 'Barrier-Free Design Guide',
  'REF-01037 PDF p. 9, hyperlink on the words Barrier-Free Design Guide (read from the PDF link annotation); the source says it is a free download from the Safety Codes Council and gives the dimensions',
  'Named by the source for appropriate dimensions. A lead only: not retrieved, not read.'),
 ('https://www.edmonton.ca/city_government/initiatives_innovation/city-accessibility-policy', 'Accessibility for People with Disabilities Policy C602',
  'REF-01037 PDF p. 1, hyperlink on the words Accessibility for People with Disabilities Policy C602 (read from the PDF link annotation)',
  'Named by the source for its definition of accessibility. A policy page, not an evidence source for a dimension. A lead only: not retrieved, not read.'),
 (None, 'Alberta Building Code',
  'REF-01037 PDF p. 1 ("Alberta Building Code requires the minimum standards for accessibility") and item 6.1 ("1 in 12 in AB building code"); no link, edition or clause given by the source',
  'Named by the source as the origin of its Code (required) items. A lead only: the edition and clauses are not stated by the source and are not guessed here. T-071 step 3 re-roots the untraced Code figures when it is admitted.'),
]
for url, title, rec, notes in LEADS:
    a = ['add-locator', '--title', title, '--recovered-from', rec, '--status', 'REFERENCE-ONLY', '--notes', notes, '--session', STEM]
    if url:
        a += ['--url', url]
    show('locator ' + title, *run(*a))
show('mining backward', *run('log-mining', '--slug', 'stair-ramp-threshold-biomechanics-accessibility', '--ref', REF, '--direction', 'backward',
     '--notes', 'Backward pass over the references the source names. It has no reference list; it names four documents in running text or by hyperlink: the Alberta Building Code (no edition given), the City of Edmonton Access Design Guide, the Safety Codes Council Barrier-Free Design Guide, and City Policy C602. Each is staged as a lead (add-locator, REFERENCE-ONLY) from the PDF text and link annotations; none was retrieved or read in this run.',
     '--session', STEM))
show('mining forward (deferred)', *run('log-mining', '--slug', 'stair-ramp-threshold-biomechanics-accessibility', '--ref', REF, '--direction', 'forward',
     '--deferred-reason', 'Forward (cited-by) search not run: a municipal grey PDF has no citation index, and this run is from-evidence (owner-supplied document), not a discovery pass.',
     '--session', STEM))
show('population MOB', *run('add-population-match', '--ref-id', REF, '--target-population', 'MOB',
     '--study-population', 'none: a municipal advisory committee checklist; no participants, no measurement',
     '--match-grade', 'PROXY', '--mismatch-note', 'No study population. The figures are committee assertions of the City of Edmonton Accessibility Advisory Committee, some attributed by the source to the Alberta building code. PROXY (R13: no participants). MOB is the only identity linked in this replay (door width and turning, on the source\'s PDF p. 1 sentence naming wheelchairs and scooters).',
     '--session', STEM))
