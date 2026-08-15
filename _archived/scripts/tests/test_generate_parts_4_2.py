"""Stage 4.2 — tests for the A.12 reassembly engine (generate_parts.py).

Verifies: stub mode emits the full part set non-empty; output is idempotent
(byte-identical re-run on unchanged DB); full mode refuses when BPCs aren't
COMPLETE; real DB content flows through (item codes, source counts); and the
schema-drift scope note is present in the script. Exit 0 = pass.
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
GEN = os.path.join(REPO, "scripts", "generate_parts.py")
DB = os.environ.get("TEST_DB", "/tmp/work14.db")

fails = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


def run(out, mode="stub"):
    return subprocess.run(
        [sys.executable, GEN, "--db", DB, "--out", out, "--mode", mode],
        capture_output=True, text=True)


if not os.path.exists(DB):
    print(f"SKIP — test DB not present: {DB}")
    sys.exit(0)

a = tempfile.mkdtemp(); b = tempfile.mkdtemp()
r1 = run(a)
check("stub mode exits 0", r1.returncode == 0)

files = sorted(f for f in os.listdir(a) if f.endswith(".md"))
check("emits manifest + 14 parts (15 files)", len(files) == 15)
check("manifest.md present", "manifest.md" in files)
check("all parts present part00..part13",
      all(f"part{n:02d}.md" in files for n in range(0, 14)))
check("every file non-empty", all(os.path.getsize(os.path.join(a, f)) > 0 for f in files))

# idempotency
run(b)
import filecmp
match, mismatch, errors = filecmp.cmpfiles(a, b, files, shallow=False)
check("idempotent (byte-identical re-run)", len(match) == len(files) and not mismatch)

# real content
p04 = open(os.path.join(a, "part04.md")).read()
check("part04 carries real item codes (A-01)", "A-01" in p04 and "Item Specification Library" in p04)
p13 = open(os.path.join(a, "part13.md")).read()
check("part13 carries evidence-source counts", "sources in the evidence base" in p13)
p03 = open(os.path.join(a, "part03.md")).read()
check("part03 BPC index reflects retraction state", "RETRACTED-PRE-REHAB" in p03 or "Rehabilitation" in p03)
man = open(os.path.join(a, "manifest.md")).read()
check("manifest carries DB fingerprint + mode", "fingerprint" in man.lower() and "stub" in man.lower())

# stub markers present (engine is in stub mode)
check("stub markers emitted", any("STUB" in open(os.path.join(a, f)).read() for f in files))

# full-mode gate
rf = run(tempfile.mkdtemp(), mode="full")
check("full mode refuses (exit 3) when BPCs incomplete", rf.returncode == 3)
check("full-mode refusal names the gate", "not COMPLETE" in rf.stderr)

# scope-drift note documented in the engine itself
src = open(GEN).read()
check("schema-drift scope note documented in engine", "page-templates.md" in src and "does NOT" in src)

print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({len(fails)} failed)")
sys.exit(1 if fails else 0)
