#!/usr/bin/env bash
# Guidebook bootstrap — full logic, extracted from PI inline block per session 2026-05-20.
#
# Invoked by PI v10.14+ thin caller. Reads PAT from env (set by thin caller).
# Idempotent. Halt on critical fetch failure; log [GAP] on non-critical.
#
# Extracting bootstrap to repo means future bootstrap drift (numerator updates,
# state-query grep updates, status-block formatting) ships as normal commits
# without requiring a PI bump and owner-paste deployment cycle.
#
# Bootstrap-exempt cases (per PI standing rule): governance work on PI /
# preferences / architecture themselves; tooling questions not touching repo
# state; workflow conversations that do not touch repo content.

set -uo pipefail

PAT="${PAT:?PAT env var required (thin caller in PI sets this from /mnt/project/GitHub_pat)}"
REPO="${REPO:-jordanelias/guidebook}"

echo "Session start: loading Guidebook context"

# ---------------------------------------------------------------------------
# Backend: gh if available, else curl
# ---------------------------------------------------------------------------
if command -v gh >/dev/null 2>&1; then
  echo "$PAT" | gh auth login --with-token 2>/dev/null || true
  _GET()       { gh api "repos/$REPO/contents/$1" --jq .content 2>/dev/null | base64 -d >"$2" 2>/dev/null; [ -s "$2" ]; }
  _GET_BIN()   { gh api "repos/$REPO/contents/$1" -H "Accept: application/vnd.github.raw" >"$2" 2>/dev/null; [ -s "$2" ]; }
  _GH_LEN()    { gh api "repos/$REPO/contents/$1" --jq 'length' 2>/dev/null || echo 0; }
  _GH_SKILLS() { gh api "repos/$REPO/contents/skills" --jq '[.[] | select(.type=="file" and (.name | endswith("_SKILL.md")))] | length' 2>/dev/null || echo "?"; }
else
  echo "[ASSUMPTION: gh CLI unavailable — using curl]"
  AUTH="Authorization: Bearer $PAT"
  _GET()       { curl -fsSL -H "$AUTH" "https://api.github.com/repos/$REPO/contents/$1" 2>/dev/null \
                   | python3 -c "import sys,json,base64;sys.stdout.buffer.write(base64.b64decode(json.load(sys.stdin)['content']))" >"$2" 2>/dev/null; [ -s "$2" ]; }
  _GET_BIN()   { curl -fsSL -H "$AUTH" -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/$REPO/contents/$1" -o "$2" 2>/dev/null; [ -s "$2" ]; }
  _GH_LEN()    { curl -fsSL -H "$AUTH" "https://api.github.com/repos/$REPO/contents/$1" 2>/dev/null \
                   | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo 0; }
  _GH_SKILLS() { curl -fsSL -H "$AUTH" "https://api.github.com/repos/$REPO/contents/skills" 2>/dev/null \
                   | python3 -c "import sys,json; d=json.load(sys.stdin); print(sum(1 for f in d if isinstance(f,dict) and f.get('type')=='file' and f.get('name','').endswith('_SKILL.md')))" 2>/dev/null || echo "?"; }
fi

# ---------------------------------------------------------------------------
# Critical fetches (halt on any failure)
# ---------------------------------------------------------------------------
_GET "sessions/LATEST" /tmp/latest.txt                            || { echo "HALT: sessions/LATEST"; exit 1; }
SESSION=$(tr -d '\n\r ' </tmp/latest.txt)
_GET "sessions/$SESSION" /tmp/session.md                          || { echo "HALT: sessions/$SESSION"; exit 1; }
_GET "references/project-standards.md" /tmp/standards.md          || { echo "HALT: project-standards.md"; exit 1; }
_GET "references/skill-registry.md" /tmp/registry.md              || { echo "HALT: skill-registry.md"; exit 1; }
_GET "audits/bpc-rewrite-workplan-2026-05-11.md" /tmp/workplan.md || { echo "HALT: bpc-rewrite-workplan"; exit 1; }

# ---------------------------------------------------------------------------
# State queries from SQLite
# ---------------------------------------------------------------------------
P1="?"; PMP_BACKLOG="?"; ATT_ONLY="?"; UNVERIFIED="?"; VERS_BACKFILL="?"
RDC_TOTAL="?"; RDC_PAYWALL="?"; ES_TOTAL="?"; REASONING_BPC_TARGET="?"; REASONING_CON_TARGET="?"

if _GET_BIN "data/guidebook.db" /tmp/guidebook.db; then
  Q() { python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"$1\").fetchone()[0])" 2>/dev/null || echo "?"; }
  ES_TOTAL=$(Q "SELECT COUNT(*) FROM evidence_sources")
  P1=$(Q "SELECT COUNT(*) FROM gaps WHERE priority='P1' AND status NOT LIKE 'CLOSED%'")
  PMP_BACKLOG=$(Q "SELECT COUNT(DISTINCT i.item_code) FROM items i WHERE i.pmp_last_walk_at IS NULL AND i.status NOT IN ('archived','superseded')")
  ATT_ONLY=$(Q "SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality='AUTHOR-TITLE-ONLY'")
  UNVERIFIED=$(Q "SELECT COUNT(*) FROM evidence_sources WHERE verification_status IS NULL OR verification_status=''")
  VERS_BACKFILL=$(Q "SELECT COUNT(*) FROM evidence_sources WHERE superseded_by_ref_id IS NOT NULL OR edition IS NOT NULL")
  REASONING_BPC_TARGET=$(Q "SELECT COUNT(*) FROM slugs WHERE status='ACTIVE'")
  REASONING_CON_TARGET=$(Q "SELECT COUNT(*) FROM connections")
  RDC_EXISTS=$(python3 -c "import sqlite3;print(1 if sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='reasoning_doc_citations'\").fetchone() else 0)" 2>/dev/null)
  if [ "$RDC_EXISTS" = "1" ]; then
    RDC_TOTAL=$(Q "SELECT COUNT(*) FROM reasoning_doc_citations")
    RDC_PAYWALL=$(Q "SELECT COUNT(*) FROM reasoning_doc_citations WHERE paywall_purchase_candidate=1")
  else
    RDC_TOTAL=0; RDC_PAYWALL=0
  fi
else
  echo "[GAP: data/guidebook.db — not fetched]"
fi

REASONING_BPC=$(_GH_LEN "references/bpc-reasoning")
REASONING_CON=$(_GH_LEN "references/connection-reasoning")
SKILLS_ACTIVE=$(_GH_SKILLS)

# ---------------------------------------------------------------------------
# Status block
# ---------------------------------------------------------------------------
# Numerator (ES_TOTAL) is dynamic — pulled from the DB instead of hardcoded —
# so dedup, ingest, or retirement migrations don't require a PI bump or
# bootstrap-script edit just to keep the ratio accurate. The Phase E / Phase D
# denominators (active-slug count, connection count) are likewise DB-derived,
# retiring the stale /95 and /245 constants (the 14 frozen population/partition
# aggregates are correctly excluded — Phase E targets ACTIVE slugs only).
echo "=== STATUS ==="
echo "session: $SESSION"
grep -E "^## (Headline|Known broken|Next-action|Next action)" /tmp/session.md
echo "P1 OPEN: $P1"
echo "PMP backlog: $PMP_BACKLOG"
echo "Evidence AUTHOR-TITLE-ONLY: $ATT_ONLY / $ES_TOTAL  (ineligible for synthesis per rule #10)"
echo "Evidence verification_status NULL: $UNVERIFIED / $ES_TOTAL"
echo "Versioning backfilled: $VERS_BACKFILL / 675  (Track 1)"
echo "reasoning_doc_citations rows: $RDC_TOTAL  (Track 3)"
echo "PAYWALL candidates flagged: $RDC_PAYWALL"
echo "BPC reasoning docs: $REASONING_BPC / $REASONING_BPC_TARGET  (Phase E target — active slugs)"
echo "Connection reasoning docs: $REASONING_CON / $REASONING_CON_TARGET  (Phase D target — connections)"
echo "Skills: $SKILLS_ACTIVE active  (count of skills/*_SKILL.md, excludes skills/deprecated/)"
echo "Workplan: bpc-rewrite-workplan-2026-05-11 (LIVE) | superseded: workplan-co0007-v4"
