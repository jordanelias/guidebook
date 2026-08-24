#!/usr/bin/env bash
# Make the check suite runnable before a session forms any belief about repo health.
#
# WHY THIS IS A HOOK AND NOT PROSE, which is this settings file's own stated rationale:
# an agent must CHOOSE to read prose, and attention degrades as context fills. A hook
# fires on every session regardless of what anyone read or remembers.
#
# WHAT IT PREVENTS, measured on origin/main at d6ef7e9 on 2026-08-25:
#   without pydantic:  5 BLOCKING failures, 10 advisory   -> RESULT: FAIL
#   with pydantic:     0 blocking,           4 advisory   -> RESULT: PASS, 50 green
# The five were validate_schema, validate_evidence_state, audit_adversarial_use,
# decision_capture and doctrine_recheck -- the entire governance battery. A session
# without pydantic sees a red repository it did not break, and CLAUDE.md tells it to
# reproduce a red check before assuming it is theirs. That advice inverts here: the
# reproduction succeeds, on main, and the wrong conclusion is available.
#
# NEVER `pip install -r requirements.txt` IN THIS CONTAINER. It pins PyYAML==6.0.3, and
# pip refuses to uninstall the Debian-managed PyYAML 6.0.1 that is already present and
# already works: "Cannot uninstall PyYAML 6.0.1, RECORD file not found." The whole
# install then aborts and pydantic never lands. Install pydantic alone.
#
# Exits 0 unconditionally. A dependency installer must never be the thing that stops a
# session from starting -- offline, no pip, no network are all survivable; the checks
# simply stay red and say why.
python3 -c 'import pydantic' 2>/dev/null && exit 0
echo "[ensure-deps] pydantic missing — installing (governance battery needs it)" >&2
pip install -q 'pydantic==2.13.3' 2>&1 | tail -2 >&2 || true
python3 -c 'import pydantic' 2>/dev/null \
  && echo "[ensure-deps] pydantic ready" >&2 \
  || echo "[ensure-deps] STILL MISSING. 5 blocking governance checks will fail and it is NOT your change: validate_schema, validate_evidence_state, audit_adversarial_use, decision_capture, doctrine_recheck." >&2
exit 0
