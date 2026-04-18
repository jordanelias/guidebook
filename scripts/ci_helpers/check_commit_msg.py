#!/usr/bin/env python3
"""
Validate HEAD commit message format.
Expected: {skill-name}: {action} [{YYYY-MM-DD HH:MM}]
"""
import sys, re, subprocess

result = subprocess.run(
    ["git", "log", "-1", "--format=%s"],
    capture_output=True, text=True
)
msg = result.stdout.strip()
print(f"Checking commit message: {msg!r}")

pattern = r"^[a-z][a-z0-9_-]+:\s+.+\s+\[\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\]$"
if re.match(pattern, msg):
    print("PASS: Commit message format valid")
    sys.exit(0)
else:
    print("FAIL: Commit message does not match required format")
    print(f"  Got:      {msg!r}")
    print(f"  Expected: {{skill-name}}: {{action}} [YYYY-MM-DD HH:MM]")
    print(f"  Example:  workplan-orchestrator: update gap register [2026-04-18 14:30]")
    sys.exit(1)
