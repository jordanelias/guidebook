#!/usr/bin/env python3
"""
scripts/ci_helpers/commit_gate.py — the shared definition of a *checkable commit*.

Both commit gates in ci.yml's `commit-msg` job exempt the same two things:

  E3  bot / automation author  -> exempt
  E4  merge commit (>1 parent) -> exempt

WHY THIS IS ONE FILE. check_doctrine_token.py already had these exemptions;
check_commit_msg.py gained them on 2026-08-01 so the two gates would agree about
what a commit is. The first pass implemented that agreement by copying the regex
into the second file — which makes the agreement a coincidence maintained by
hand, in a repo whose whole check apparatus exists because four hand-kept lists
drifted apart. Two gates that must agree, agreeing via two copies of a pattern,
is the same defect at smaller scale. Editing BOT_RE here changes both.

Deliberately narrow: only what both gates share. Doctrine-token specifics (E1
synthesis paths, E2 doctrine self-modification) stay in check_doctrine_token.py,
because duplicating those into a common module would be the opposite error —
hoisting single-caller logic into shared surface.

Exemption strength, stated plainly: E3 trusts an authorship string. Anyone can
set one (`git -c user.email=x-bot@y`). That is acceptable in a single-author
repo where the gates exist to catch mistakes rather than adversaries, but it is
authorship trust, not authentication, and it should not be relied on as the
latter if this repo ever takes outside contributions.
"""

import re

BOT_RE = re.compile(r"dependabot|github-actions|-bot@")


def is_bot(author: str) -> bool:
    """E3 — the commit was authored by automation."""
    return bool(BOT_RE.search(author or ""))


def is_merge(parent_count: int) -> bool:
    """E4 — a merge commit. Its subject is composed by GitHub, not by the author,
    so neither the message format nor the doctrine token is the author's to get
    right."""
    return parent_count > 1
