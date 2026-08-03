#!/usr/bin/env python3
"""
validate_commits.py — Validate commit messages against the project's convention.

PI commit convention: `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

Checks (per audit_2026-04-30 R7):
  V1  Headline matches `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]` regex
  V2  Skill-name prefix exists in skills/ or is a known governance/operational prefix
  V3  Timestamp in headline is a valid YYYY-MM-DD HH:MM
  V4  Timestamp is not in the future
  V5  Author email matches `jordanelias@*` OR is a recognised Claude attribution

Exit codes:
  0 — all checks pass on the inspected window
  1 — V1/V2/V3/V4 violations exceed tolerance (default: 5%)
  2 — script error (e.g., git not available)

CLI:
  --since DATE       Only check commits since DATE (default: 7 days ago)
  --until DATE       Only check commits until DATE (default: HEAD)
  --tolerance PCT    Allowed non-compliance percentage (default: 5)
  --report           Always exit 0; just print report
  --strict           Tolerance 0%; any violation fails
  --json             Emit JSON report instead of human-readable

Per A12 §4 model_routing: this script is itself a D-OP/DG-AUTO validator addition.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Convention regex: skill-name: action [YYYY-MM-DD HH:MM]
HEADLINE_RE = re.compile(
    r"^(?P<skill>[a-z0-9][a-z0-9\-_]*?):\s+"
    r"(?P<action>.+?)\s+"
    r"\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]\s*$"
)
# Timestamp parse — strict; rejects "[2026-04-24 07:12M]" etc.
TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")

# Recognised non-skill prefixes: project-standards (file-name as prefix), session
# (when session-consolidator omitted), opus-adjudication (legacy alias).
KNOWN_NON_SKILL_PREFIXES = {
    "session",  # legacy session bare-prefix
    "project-standards",  # file-name prefix
    "isw",  # ISW briefing prefix
    "opus-adjudication",  # legacy alias for opus-synthesis pre-2026-04
    "opus-synthesis",
    "bpc-corrector",
    "appendix-editor",
    "bibliography-compiler",
    "spec-db-curator",
    "voice-style",
}

# Recognised author signatures
JORDANELIAS_RE = re.compile(r"jordanelias")
CLAUDE_RE = re.compile(r"^Claude \(.+\)$")


def run_git(*args: str, cwd: Path | None = None) -> str:
    try:
        result = subprocess.run(
            ["git"] + list(args),
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except FileNotFoundError:
        sys.exit("ERROR: git not available")
    except subprocess.CalledProcessError as e:
        sys.exit(f"ERROR: git {' '.join(args)} failed: {e.stderr}")


def discover_skill_prefixes(repo_root: Path) -> set[str]:
    """Skill prefixes are filenames in skills/ minus the _SKILL.md suffix."""
    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        return set()
    prefixes: set[str] = set()
    for f in skills_dir.iterdir():
        if f.is_file() and f.name.endswith("_SKILL.md"):
            prefixes.add(f.name[: -len("_SKILL.md")])
    return prefixes


def fetch_commits(since: str | None, until: str | None, repo_root: Path | None) -> list[dict[str, Any]]:
    """Fetch commits with %H, %an, %ae, %aI, %s on separate fields via NUL separator."""
    fmt = "%H%x00%an%x00%ae%x00%aI%x00%s"
    args = ["log", f"--pretty=format:{fmt}"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    out = run_git(*args, cwd=repo_root)
    commits = []
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\x00")
        if len(parts) != 5:
            continue
        sha, name, email, date_iso, subject = parts
        commits.append({
            "sha": sha,
            "author_name": name,
            "author_email": email,
            "author_date": date_iso,
            "headline": subject,
        })
    return commits


def check_commit(commit: dict[str, Any], skill_prefixes: set[str]) -> dict[str, Any]:
    """Return dict with sha and list of failed checks."""
    failures: list[str] = []
    headline = commit["headline"]

    # V1: headline regex
    m = HEADLINE_RE.match(headline)
    if not m:
        failures.append("V1_FORMAT")
        return {**commit, "failures": failures, "skill": None, "ts": None}

    skill = m.group("skill")
    action = m.group("action")
    ts_str = m.group("ts")

    # V2: known skill prefix
    if skill not in skill_prefixes and skill not in KNOWN_NON_SKILL_PREFIXES:
        failures.append("V2_UNKNOWN_SKILL")

    # V3: valid timestamp
    try:
        ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except ValueError:
        failures.append("V3_BAD_TIMESTAMP")
        ts = None

    # V4: not future
    if ts is not None:
        now = datetime.now(timezone.utc)
        if ts > now + timedelta(minutes=10):  # 10-minute tolerance for clock skew
            failures.append("V4_FUTURE")

    # V5: known author
    name = commit["author_name"]
    email = commit["author_email"]
    if not (JORDANELIAS_RE.search(email) or JORDANELIAS_RE.search(name) or CLAUDE_RE.match(name)):
        failures.append("V5_UNKNOWN_AUTHOR")

    return {**commit, "failures": failures, "skill": skill, "ts": ts_str, "action": action}


def render_human_report(results: list[dict[str, Any]], total: int, tolerance_pct: float) -> str:
    failures = [r for r in results if r["failures"]]
    pct = (len(failures) / total * 100) if total else 0.0
    lines = [
        f"=== validate_commits.py ===",
        f"Total commits inspected: {total}",
        f"Failures: {len(failures)} ({pct:.1f}%)",
        f"Tolerance: {tolerance_pct}%",
        "",
    ]
    if failures:
        # Group by failure type
        by_type: dict[str, list[dict[str, Any]]] = {}
        for r in failures:
            for f in r["failures"]:
                by_type.setdefault(f, []).append(r)
        lines.append("=== Failure breakdown ===")
        for ftype in sorted(by_type):
            lines.append(f"  {ftype}: {len(by_type[ftype])}")
        lines.append("")
        lines.append("=== Per-commit failures (most recent first) ===")
        for r in failures[:30]:
            lines.append(
                f"  {r['sha'][:12]} | {r['author_date'][:16]} | {','.join(r['failures'])} | "
                f"{r['headline'][:90]}"
            )
        if len(failures) > 30:
            lines.append(f"  ... ({len(failures) - 30} more)")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Validate commit messages against PI convention")
    p.add_argument("--since", help="Only check commits since DATE (default: 7 days ago)")
    p.add_argument("--until", help="Only check commits until DATE (default: HEAD)")
    p.add_argument("--tolerance", type=float, default=5.0, help="Allowed non-compliance %% (default 5)")
    p.add_argument("--report", action="store_true", help="Always exit 0; just print report")
    p.add_argument("--strict", action="store_true", help="Tolerance 0%%; any violation fails")
    p.add_argument("--json", action="store_true", dest="emit_json", help="Emit JSON instead of text")
    p.add_argument("--repo", help="Path to repo root (default: current dir)")
    args = p.parse_args()

    repo_root = Path(args.repo) if args.repo else Path.cwd()
    skill_prefixes = discover_skill_prefixes(repo_root)

    since = args.since or (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    commits = fetch_commits(since=since, until=args.until, repo_root=repo_root)

    results = [check_commit(c, skill_prefixes) for c in commits]
    total = len(results)
    failures = [r for r in results if r["failures"]]
    pct = (len(failures) / total * 100) if total else 0.0

    tolerance = 0.0 if args.strict else args.tolerance
    fails_threshold = pct > tolerance

    if args.emit_json:
        payload = {
            "total": total,
            "failures": len(failures),
            "failure_pct": pct,
            "tolerance_pct": tolerance,
            "violations": [
                {
                    "sha": r["sha"][:12],
                    "date": r["author_date"][:16],
                    "headline": r["headline"],
                    "failures": r["failures"],
                }
                for r in failures
            ],
            "skill_prefixes_known": sorted(skill_prefixes | KNOWN_NON_SKILL_PREFIXES),
        }
        print(json.dumps(payload, indent=2))
    else:
        print(render_human_report(results, total, tolerance))

    if args.report:
        return 0
    return 1 if fails_threshold else 0


if __name__ == "__main__":
    sys.exit(main())
