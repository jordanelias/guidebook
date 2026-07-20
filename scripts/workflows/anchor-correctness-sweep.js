export const meta = {
  name: 'anchor-correctness-sweep',
  description: 'Verify correctness of every T1/T2/Co-1/Co-2 anchor evidence_source (re-retrieval + identity + tier/type + language + jurisdiction), then adversarially refute each flagged defect',
  phases: [
    { title: 'Verify', detail: 'per-batch retrieval + field-correctness check against the live source' },
    { title: 'Refute', detail: 'adversarial re-check of each flagged defect' },
  ],
}

// args = flat array of anchor ref_ids (233). May arrive as an array or a JSON string.
let REFIDS = args
if (typeof REFIDS === 'string') { try { REFIDS = JSON.parse(REFIDS) } catch (e) { REFIDS = [] } }
if (!Array.isArray(REFIDS)) REFIDS = []
const BATCH = 8
const batches = []
for (let i = 0; i < REFIDS.length; i += BATCH) batches.push(REFIDS.slice(i, i + BATCH))
log(`anchor-correctness-sweep: ${REFIDS.length} refs in ${batches.length} batches of ${BATCH}`)

const DEFECT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['rows_checked', 'unretrievable', 'defects'],
  properties: {
    rows_checked: { type: 'array', items: { type: 'string' } },
    unretrievable: { type: 'array', items: { type: 'string' },
      description: 'ref_ids whose source could not be re-retrieved this session (tool blocked / no resolver) — NOT judged fabricated, just unverifiable now' },
    defects: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['ref_id', 'field', 'severity', 'current_value', 'proposed_value', 'evidence', 'model_dependent'],
        properties: {
          ref_id: { type: 'string' },
          field: { type: 'string', description: "one of: retrievability, pub_title, author_display, pub_year, journal_name, doi, url, tier, evidence_type, lang_detected, jurisdiction, standard_number, other" },
          severity: { type: 'string', enum: ['critical', 'major', 'minor'] },
          current_value: { type: 'string' },
          proposed_value: { type: 'string' },
          evidence: { type: 'string', description: 'what the real retrieval showed + the tool used' },
          model_dependent: { type: 'boolean', description: 'true if the fix depends on the unsettled tier-model decisions (weighted-strength, scoping/rapid/narrative-review tiering GAP-298, practice-stream GAP-299)' },
        },
      },
    },
  },
}

const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['verdicts'],
  properties: {
    verdicts: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['ref_id', 'field', 'upheld', 'note'],
        properties: {
          ref_id: { type: 'string' },
          field: { type: 'string' },
          upheld: { type: 'boolean', description: 'true if the defect+proposed fix survives independent re-retrieval; false if refuted' },
          note: { type: 'string' },
        },
      },
    },
  },
}

const DOCTRINE = `TIER LADDER (governance/tier-system.md):
- T1 = primary research at high control level (RCT, controlled experiment). Co-1 = disability-led lived experience / DPO output.
- T2 = synthesis above primaries: systematic reviews / meta-analyses (evidence_type sr_meta) OR named-ORGANISATION evidence-based standards / DPO or professional-body standards (standard_eb). Co-2 = OT/professional-body CPGs (co2).
- T3 = lower-control primary: 'clinical' (observational, cross-sectional, qualitative, single-centre) or 'grey' (grey-literature primary).
- T4 intl standards (ISO/IEC/CEN), T5 national frameworks (BS 8300, DIN 18040), T6 statutory code (ADA, GB 50763).
KEY CORRECTNESS TRAPS to flag:
- A row typed sr_meta (T2) that is actually a SCOPING / RAPID / NARRATIVE / literature review -> flag (field=evidence_type or tier), model_dependent=true (GAP-298 open).
- A row typed standard_eb (T2) that is actually a statutory CODE (belongs T6) or an individual-authored academic paper (belongs T1/T3) -> flag.
- A firm/consultancy design guide typed as code/standard -> flag, model_dependent=true (practice-stream GAP-299).
- lang_detected not matching the true SOURCE language (langdetect often ran on English catalogue metadata; errors go BOTH ways) -> flag.
- jurisdiction not matching the source's real origin -> flag.`

function verifyPrompt(batch, idx) {
  return `You are a guilty-until-proven CORRECTNESS auditor of an evidence database for disability built-environment best-practice research. Verify these ${batch.length} anchor-tier sources for correctness. Batch ${idx}. Ref IDs: ${batch.join(', ')}.

STEP 1 — read the rows. Run python3 to read each row from the live DB (you share the repo working directory):
  python3 -c "import sqlite3,json; c=sqlite3.connect('data/guidebook.db'); import sys; ids=${JSON.stringify(batch)};
  cols=['ref_id','tier','evidence_type','pub_title','pub_subtitle','author_display','author_count','pub_year','journal_name','publisher','doi','pmid','url','standard_number','lang_detected','jurisdiction','verification_status','grey_flag'];
  [print(json.dumps(dict(zip(cols, c.execute('select '+','.join(cols)+' from evidence_sources where ref_id=?',(i,)).fetchone())), ensure_ascii=False)) for i in ids]"

STEP 2 — for EACH row, re-retrieve the real source via a REAL tool call and compare. Load tools with ToolSearch: "select:WebSearch,WebFetch" and (for biomedical) "select:mcp__PubMed__search_articles,mcp__PubMed__get_article_metadata". Use PubMed for clinical/biomedical (check the indexed publication type!), WebSearch/WebFetch (resolve the DOI) for standards, guidelines, DPO outputs, non-English, and books.
Check these dimensions and report any MISMATCH as a defect:
  (a) retrievability — does the DOI/URL/citation resolve to a real, matching source? If it cannot be retrieved this session (tool blocked, no resolver), put the ref_id in unretrievable — do NOT guess and do NOT call it fabricated.
  (b) identity — pub_title, author_display (first author at least), pub_year, journal_name, doi all match the real source.
  (c) tier / evidence_type — is the stored tier+type what the source ACTUALLY is? Apply the doctrine below; mark model_dependent=true where noted.
  (d) lang_detected — the TRUE language of the source text (not the English catalogue metadata).
  (e) jurisdiction — the source's real jurisdiction of origin.

${DOCTRINE}

RULES: Never invent a correction you did not verify by retrieval. Evidence field must name the tool + what it returned. Only report a defect when the live source contradicts the stored value; if a field is correct, say nothing about it. Return rows_checked (all ref_ids you read), unretrievable (couldn't verify), and defects.`
}

function refutePrompt(defects, idx) {
  return `You are an adversarial refuter. A prior auditor flagged the following proposed corrections to an evidence database (batch ${idx}). For EACH, independently re-retrieve the real source (ToolSearch: "select:WebSearch,WebFetch" and PubMed for biomedical) and try to REFUTE the correction. Default to upheld=false if you cannot independently confirm it. Only upheld=true when your own retrieval reproduces the defect AND the proposed value. Flagged defects (JSON): ${JSON.stringify(defects)}. Return a verdict per (ref_id, field).`
}

const results = await pipeline(
  batches,
  (batch, _orig, idx) => agent(verifyPrompt(batch, idx), { label: `verify:b${idx}`, phase: 'Verify', schema: DEFECT_SCHEMA }),
  (res, batch, idx) => {
    if (!res || !res.defects || res.defects.length === 0) {
      return { batch: idx, verify: res, verdicts: { verdicts: [] } }
    }
    return agent(refutePrompt(res.defects, idx), { label: `refute:b${idx}`, phase: 'Refute', schema: VERDICT_SCHEMA })
      .then(v => ({ batch: idx, verify: res, verdicts: v || { verdicts: [] } }))
  }
)

// Aggregate
const clean = results.filter(Boolean)
const allDefects = []
const unretrievable = []
const checked = []
for (const r of clean) {
  const v = r.verify || {}
  ;(v.rows_checked || []).forEach(x => checked.push(x))
  ;(v.unretrievable || []).forEach(x => unretrievable.push(x))
  const vmap = {}
  ;(r.verdicts?.verdicts || []).forEach(vd => { vmap[vd.ref_id + '|' + vd.field] = vd })
  for (const d of (v.defects || [])) {
    const vd = vmap[d.ref_id + '|' + d.field]
    allDefects.push({ ...d, upheld: vd ? vd.upheld : null, refute_note: vd ? vd.note : 'not re-checked' })
  }
}
const confirmed = allDefects.filter(d => d.upheld === true)
log(`sweep done: ${checked.length} checked, ${unretrievable.length} unretrievable, ${allDefects.length} defects flagged, ${confirmed.length} adversarially upheld`)
return { checked_count: checked.length, unretrievable, defects: allDefects, confirmed_defects: confirmed }
