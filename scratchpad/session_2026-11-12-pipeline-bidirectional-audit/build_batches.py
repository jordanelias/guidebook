#!/usr/bin/env python3
"""Derive the remediation plan's dependency batches from the task files. Reads only; writes REMEDIATION-PLAN.md.

    python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py

Nothing here is typed in: ids, titles, kinds, executors, owner decisions and hard dependencies come from each
task file's own text (section 1 table; section 2 bullets 'Tasks that must be merged' and 'Owner decisions').
A dependency written 'none (after T-nnn if both are open ...)' is SOFT: an ordering hint, not a gate.
Batch = 1 + the longest chain of hard dependencies. Within a batch, tasks that touch the same file are one
SERIAL LANE (merge in the lane's order); different lanes may be worked in parallel.
"""
import re, subprocess, datetime, collections
from pathlib import Path

ROOT = Path("/home/user/guidebook")
W = ROOT / "workplan/2026-11-12-bidirectional-pipeline"
OUT = W / "REMEDIATION-PLAN.md"
TASKS = sorted((W / "tasks").glob("T-[0-9]*-*.md"))


def section(text, n):
    m = re.search(rf"^## {n}\. .*?$(.*?)(?=^## \d+\. |\Z)", text, re.S | re.M)
    return m.group(1) if m else ""


def cell(text, label):
    m = re.search(rf"^\| {label} \| (.*?) \|\s*$", text, re.M)
    return m.group(1).strip() if m else ""


def bullet(sec2, label):
    m = re.search(rf"^- \*\*{label}[^*]*\*\*(.*?)(?=^- \*\*|\Z)", sec2, re.S | re.M)
    return m.group(1).strip() if m else ""


tasks = {}
for f in TASKS:
    t = f.read_text()
    tid = re.match(r"# (T-\d+)", t).group(1)
    title = re.sub(r"^# T-\d+\s+", "", t.splitlines()[0]).strip()
    s2, s4 = section(t, 2), section(t, 4)
    dep_txt = bullet(s2, "Tasks that must be merged")
    dep_txt = dep_txt.split("Check by running")[0]
    soft = set()
    if dep_txt.lower().lstrip().startswith("none ("):
        soft = set(re.findall(r"T-\d+", dep_txt))
        hard = set()
    elif dep_txt.lower().lstrip().startswith("none"):
        hard = set()
    else:
        hard = set(re.findall(r"T-\d+", dep_txt))
    hard.discard(tid)
    od_txt = bullet(s2, "Owner decisions")
    ods = set() if od_txt.lower().startswith("none") else set(re.findall(r"OD-\d+", od_txt))
    paths = sorted(set(re.findall(r"`((?:scripts|schemas|governance|skills|\.claude|\.github)/[A-Za-z0-9_./\-]+\.[a-z]+)`", s4)))
    paths = [p for p in paths if "/migrations/" not in p]
    if "RESEARCH" in cell(t, "Kind"):
        paths = []  # a research task writes rows through the sanctioned path; the tools it calls are not files it edits
    tasks[tid] = dict(
        id=tid, file=f.name, title=title, wave=cell(t, "Wave"), kind="RESEARCH" if "RESEARCH" in cell(t, "Kind") else "TOOLING",
        sonnet="NOT FOR SONNET" not in cell(t, "Executor"), hard=hard, soft=soft, ods=ods, paths=paths,
        piloted=bool(re.search(r"\*\*Pilot status\.\*\* \*\*Piloted", t)))

# --- batches: longest chain of hard dependencies
memo, stack = {}, set()


def depth(t):
    if t in memo:
        return memo[t]
    if t in stack:
        raise SystemExit(f"CYCLE through {t}")
    stack.add(t)
    d = 1 + max([depth(x) for x in tasks[t]["hard"] if x in tasks] or [0])
    stack.discard(t)
    memo[t] = d
    return d


missing = sorted({d for t in tasks.values() for d in t["hard"] if d not in tasks})
for t in tasks:
    tasks[t]["batch"] = depth(t)
nb = max(t["batch"] for t in tasks.values())

# --- status
def status(t):
    if not t["sonnet"]:
        return "NOT FOR SONNET"
    if t["ods"]:
        return "OWNER: " + ",".join(sorted(t["ods"], key=lambda x: int(x[3:])))
    return "READY"


# a task is 'reachable by Sonnet' if it and every hard ancestor is READY
def anc(t, seen=None):
    seen = seen if seen is not None else set()
    for d in tasks[t]["hard"]:
        if d in tasks and d not in seen:
            seen.add(d)
            anc(d, seen)
    return seen


for tid, t in tasks.items():
    t["status"] = status(t)
    blockers = [a for a in anc(tid) if status(tasks[a]) != "READY"]
    t["reach"] = "yes" if t["status"] == "READY" and not blockers else ("after " + ", ".join(sorted(blockers, key=lambda x: int(x[2:]))) if t["status"] == "READY" else "no")

# --- serial lanes inside a batch: connected components over shared paths and soft deps
def lanes(ids):
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for a in ids:
        for b in ids:
            if a < b and (set(tasks[a]["paths"]) & set(tasks[b]["paths"]) or b in tasks[a]["soft"] or a in tasks[b]["soft"]):
                union(a, b)
    comp = collections.defaultdict(list)
    for i in ids:
        comp[find(i)].append(i)
    key = lambda i: (tasks[i]["kind"] == "RESEARCH", int(i[2:]))
    return sorted((sorted(v, key=key) for v in comp.values()), key=lambda v: key(v[0]))


# --- owner-decision queue
od_blocks = collections.defaultdict(list)
for tid, t in tasks.items():
    for o in t["ods"]:
        od_blocks[o].append(tid)

# --- critical path (longest hard chain)
def chain(t):
    best = []
    for d in tasks[t]["hard"]:
        if d in tasks:
            c = chain(d)
            if len(c) > len(best):
                best = c
    return best + [t]


crit = max((chain(t) for t in tasks), key=len)

sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
L = []
A = L.append
A("# Remediation plan, in batches by dependency\n")
A(f"_Generated {now} from the {len(tasks)} task files at commit {sha} by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`. "
  "Nothing below is typed in: re-run the generator (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) after any task file changes, and trust the generator over this text (CLAUDE.md rule 7a)._\n")
A("**What this is.** The entry document for a Sonnet executor. `REMEDIATION-WORKPLAN.md` is the index (why, owner decision register, Definition of Done); `tasks/T-<id>-*.md` is the one self-contained file per task; this file says **in what order, in what groups, and where to stop.** "
  "Evidence base: `01-handshake-ledger.md` and the audit in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/`.\n")
A("## 1. How to execute\n")
A("1. **Merge this workplan first.** Every task file sets `$BASE` to `origin/main` once the workplan is on it, and to the workplan branch before that.")
A("2. **Take one batch at a time, in order.** A batch is the set of tasks whose hard dependencies all lie in earlier batches. Do not start batch *n* until every READY task of batch *n-1* is merged and its after-test is green on `$BASE`.")
A("3. **Inside a batch, work lanes in parallel and tasks in a lane serially.** A lane is a set of tasks that touch the same file (or that a task file says to sequence). Merge a lane's tasks in the order listed; where `REMEDIATION-WORKPLAN.md` gives its own merge order for some of them (Wave 0), that order wins, because it also accounts for the characterisation harness of T-014 which must exist before the changes it compares.")
A("4. **One task, one pull request, one executor, one task file.** Run the task's red test before, the same test after, the gate once (`scripts/preflight.sh --base \"$BASE\" --explain`), and the adversarial pass once before opening the pull request. Rule 9: open the pull request last, then unsubscribe.")
A("5. **Stop at a status that is not READY.** `OWNER: OD-nn` means the owner's answer (in the form the register gives) must be in `references/project-standards.md` first. `NOT FOR SONNET` means an Opus-class session or the Fable agent does it. Neither is an invitation to improvise.")
A("6. **Tooling merges before the research it unlocks (rule 10).** A research task never shares a pull request with tooling, and its row writes go only through the write path of CLAUDE.md §4.")
A("7. **The first execution of an unpiloted task is its pilot.** List any defect found in its task file in the pull request.\n")
A("## 2. The batches at a glance\n")
A("| Batch | Tasks | READY | OWNER-blocked | NOT FOR SONNET | Tooling / research | Lanes |")
A("|---|---|---|---|---|---|---|")
for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    c = collections.Counter(tasks[t]["status"].split(":")[0] for t in ids)
    A(f"| {b} | {len(ids)} | {c['READY']} | {c['OWNER']} | {c['NOT FOR SONNET']} | {sum(tasks[t]['kind']=='TOOLING' for t in ids)} / {sum(tasks[t]['kind']=='RESEARCH' for t in ids)} | {len(lanes(ids))} |")
A("\nCounts are derived; the commands that check them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | wc -l`, and the generator's own output.\n")
A(f"**Longest dependency chain ({len(crit)} tasks):** " + " → ".join(f"{t} ({tasks[t]['status']})" for t in crit) + ".\n")
if missing:
    A(f"**Dependencies naming a task with no file (fix the task file):** {', '.join(missing)}\n")

for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    A(f"## Batch {b}\n")
    if b == 1:
        A("**Entry:** the workplan is on the integration base. No task is a prerequisite.\n")
    else:
        prev = sorted({d for t in ids for d in tasks[t]["hard"]}, key=lambda x: int(x[2:]))
        A("**Entry:** merged and green on `$BASE`: " + ", ".join(prev) + ".\n")
    A("| Task | Title | Wave | Kind | Status | Reachable by Sonnet now | Hard deps | Pilot |")
    A("|---|---|---|---|---|---|---|---|")
    for t in sorted(ids, key=lambda x: int(x[2:])):
        x = tasks[t]
        A(f"| [{t}](tasks/{x['file']}) | {x['title'][:90]} | {x['wave']} | {x['kind']} | {x['status']} | {x['reach']} | {', '.join(sorted(x['hard'], key=lambda y: int(y[2:]))) or '—'} | {'piloted' if x['piloted'] else 'not piloted'} |")
    A("\n**Lanes** (parallel across, serial within; the shared file is the reason):\n")
    for i, lane in enumerate(lanes(ids), 1):
        shared = sorted(set.intersection(*[set(tasks[t]["paths"]) for t in lane])) if len(lane) > 1 else []
        why = f" — share `{shared[0]}`" if shared else (" — sequenced by a soft dependency or a chain of shared files" if len(lane) > 1 else "")
        A(f"- Lane {b}.{i}: " + " → ".join(lane) + why)
    nfs = sorted((t for t in ids if not tasks[t]["sonnet"]), key=lambda x: int(x[2:]))
    own = sorted((t for t in ids if tasks[t]["sonnet"] and tasks[t]["ods"]), key=lambda x: int(x[2:]))
    stops = []
    if nfs:
        stops.append("not for Sonnet: " + ", ".join(nfs))
    if own:
        stops.append("waiting on the owner: " + ", ".join(f"{t} ({'/'.join(sorted(tasks[t]['ods']))})" for t in own))
    A("\n**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base \"$BASE\" --explain` is green on `$BASE`." +
      (f" **Stops in this batch:** {'; '.join(stops)}." if stops else "") + "\n")

A("## Owner decision queue (what each answer releases)\n")
A("Answer forms and options are in the register in `REMEDIATION-WORKPLAN.md` (grep `^### OD-`). An answer binds only once the ledger quotes it (`references/project-standards.md`).\n")
A("| Decision | Releases | In batches |")
A("|---|---|---|")
for o in sorted(od_blocks, key=lambda x: int(x[3:])):
    A(f"| {o} | {', '.join(sorted(od_blocks[o], key=lambda x: int(x[2:])))} | {', '.join(str(b) for b in sorted({tasks[t]['batch'] for t in od_blocks[o]}))} |")
inreg = set(re.findall(r"^### (OD-\d+)", (W / "REMEDIATION-WORKPLAN.md").read_text(), re.M))
A(f"\nDecisions in the register that no task file lists as a precondition: {', '.join(sorted(inreg - set(od_blocks), key=lambda x: int(x[3:]))) or 'none'}.\n")
A("## NOT FOR SONNET\n")
A("| Task | Title | Batch | Owner decisions |")
A("|---|---|---|---|")
for t in sorted((t for t in tasks if not tasks[t]["sonnet"]), key=lambda x: int(x[2:])):
    x = tasks[t]
    A(f"| [{t}](tasks/{x['file']}) | {x['title'][:80]} | {x['batch']} | {', '.join(sorted(x['ods'])) or '—'} |")
A("\nEach file says who does it. Everything that depends on one of these waits for it (the 'Reachable by Sonnet now' column names the blockers).\n")
A("## Where the pilots stand\n")
A("`grep -L \"Not piloted\" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md` lists the tasks a pilot has touched. Results, defects found and what changed in the plan are in section 12 of `REMEDIATION-WORKPLAN.md` and in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/`.\n")
OUT.write_text("\n".join(L))
print("tasks", len(tasks), "batches", nb, "missing deps", missing, "crit", len(crit))
for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    print(b, len(ids), collections.Counter(tasks[t]["status"].split(":")[0] for t in ids))
