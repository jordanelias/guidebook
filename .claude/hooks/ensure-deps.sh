#!/usr/bin/env bash
# Make the check suite runnable before a session forms any belief about repo health.
#
# WHY A HOOK AND NOT PROSE, which is this settings file's own stated rationale: an agent
# must CHOOSE to read prose, and attention degrades as context fills. A hook fires on
# every session regardless of what anyone read or remembers.
#
# WHAT IT PREVENTS, measured on origin/main at d6ef7e9 on 2026-08-25:
#   without pydantic:  5 BLOCKING failures, 10 advisory   -> RESULT: FAIL
#   with pydantic:     0 blocking,           4 advisory   -> PASS, 50 green
# The five were validate_schema, validate_evidence_state, audit_adversarial_use,
# decision_capture and doctrine_recheck -- the entire governance battery. A session
# without them sees a red repository it did not break, and CLAUDE.md tells it to
# reproduce a red check before assuming it is theirs. That advice INVERTS here: the
# reproduction succeeds, on main, and the wrong conclusion is available.
#
# THE DEPENDENCY LIST HAS ONE HOME: governance/check-registry.yaml, whose `batteries:`
# block declares `deps:` per battery. requirements.txt is a SECOND home and it already
# disagreed -- it names pydantic and PyYAML and omits jsonschema, which the registry
# declares for the `research` battery and which attestation validation needs. Found on
# 2026-08-25 by an attestation validation failing on a fresh container. Read the registry
# (rule 5: point, do not copy); fall back to a literal list only if it cannot be parsed.
#
# NEVER `pip install -r requirements.txt` IN THIS CONTAINER. It pins PyYAML==6.0.3, and
# pip refuses to uninstall the Debian-managed PyYAML 6.0.1 that is already present and
# already works: "Cannot uninstall PyYAML 6.0.1, RECORD file not found." The whole install
# then aborts and nothing lands. Install the individual packages.
#
# Exits 0 unconditionally. A dependency installer must never be the thing that stops a
# session starting -- offline, no pip, no network are all survivable; the checks stay red
# and say why.

cd "${CLAUDE_PROJECT_DIR:-.}" 2>/dev/null || true

DEPS=$(python3 - <<'PY' 2>/dev/null
try:
    import yaml
    d = yaml.safe_load(open("governance/check-registry.yaml"))
    out = set()
    for b in (d.get("batteries") or {}).values():
        for dep in (b or {}).get("deps") or []:
            out.add(str(dep).strip())
    print(" ".join(sorted(out)))
except Exception:
    pass
PY
)
# Fallback only if the registry could not be read. Keep in step with it if it is ever used.
[ -z "$DEPS" ] && DEPS="pydantic jsonschema"

MISSING=""
for d in $DEPS; do
  python3 -c "import $d" 2>/dev/null || MISSING="$MISSING $d"
done
[ -z "$MISSING" ] && exit 0

echo "[ensure-deps] missing:$MISSING — installing (the check batteries declare them)" >&2
for d in $MISSING; do pip install -q "$d" 2>&1 | tail -1 >&2 || true; done

STILL=""
for d in $DEPS; do python3 -c "import $d" 2>/dev/null || STILL="$STILL $d"; done
if [ -z "$STILL" ]; then
  echo "[ensure-deps] ready" >&2
else
  echo "[ensure-deps] STILL MISSING:$STILL. Blocking checks will fail and it is NOT your change." >&2
fi
exit 0
