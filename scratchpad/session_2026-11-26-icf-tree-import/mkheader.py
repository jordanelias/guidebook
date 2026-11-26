import json, sys
d = json.load(open(sys.argv[1]))
L = ["-- T-148: the ICF tree imported from the persisted WHO ICF 2026-01 tabulation (OD-74; ledger \"Delegated resolutions 2026-11-23\" and \"Delegated resolutions 2026-11-25\").",
     "-- Source: retrieval-log/session_2026-11-22-icf-umbrella-glossary/38776b09204984dc.zip (sha256 in manifest.jsonl beside it).",
     "-- Written by: db.py import-icf-tree on a scratch copy. Re-derive with --dry-run on a copy; the verb's output is the authority, not these lists.",
     "-- Blocks minted (level-2 and level-3): %d. Held codes parented: %d. Untitled codes named: %d." % (len(d['inserted']), len(d['parented']), len(d['titled'])),
     "-- d910-d920 is not a WHO block (WHO's is d910-d999) and is left as stored: unmatched = %s." % d['unmatched'],
     "-- Titles REPLACED (code | old title | old source | new WHO title). Where the source is access_need_icf.note the old text is still held there:"]
for c, o, s, n in d['replaced']:
    L.append("--   %s | %s | %s | %s" % (c, o.replace("\n", " "), s, n))
L.append("-- Titles CONFIRMED by the payload (code | old title | old source); the stored wording takes WHO's casing and the source becomes the payload:")
for c, o, s in d['confirmed']:
    L.append("--   %s | %s | %s" % (c, o, s))
L.append("-- specifications rows with an icf_code when this batch was made: 0 (RULE_VERSION is left alone).")
print("\n".join(L) + "\n")
