#!/usr/bin/env python3
"""Derive the remediation plan's dependency batches from the task files. Reads only; writes REMEDIATION-PLAN.md.

    python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py

Nothing here is typed in: ids, titles, kinds, executors, decisions and hard dependencies come from each task
file's own text (section 1 table; section 2 bullets 'Tasks that must be merged', 'Owner decisions' and 'Delegated
resolutions this task rests on'), and the STATE of every decision comes from the ledger's status and check lines
(references/project-standards.md, "Convention 2026-11-12 — how a delegated resolution ..."): the last line of each
kind wins, exactly as the shell gate of that convention reads them (a substring match, like grep -F).
A decision named in the 'Owner decisions' bullet needs the owner's words (OPEN only on ANSWERED BY THE OWNER); one
named in the 'Delegated resolutions' bullet is OPEN on that, or on RESOLVED UNDER DELEGATION with its check not
required / confirmed. A design file named in the dependency bullet (`T-nnn-design.md`) is a stop until it exists.
A dependency written 'none (after T-nnn if both are open ...)' is SOFT: an ordering hint, not a gate.
MERGED is read from git, never typed: a task is merged when a merge commit reachable from HEAD names its branch,
`task/` + the file stem in lower case (the branch every task file's set-up block creates; GitHub's subject is
"Merge pull request #N from <owner>/task/<stem>"). A merged task leaves the open batches and is listed apart; a
dependency on it is satisfied. A SQUASH merge leaves no merge commit; it is read from its single commit, whose
subject is the pull request title plus " (#N)": a task is merged when such a subject reachable from HEAD begins
"T-nnn:" or says "execute workplan T-nnn" (the two title forms the task pull requests have used; a title that only
mentions a task, such as a plan fold's "T-057/T-059/T-060 authored", is not read as a merge). A rebase merge leaves
neither and the task stays open: re-check.
Batch = 1 + the longest chain of hard dependencies. Within a batch, tasks that touch the same file are one
SERIAL LANE (merge in the lane's order); different lanes may be worked in parallel.
"""
import re, subprocess, datetime, collections
from pathlib import Path

ROOT = Path("/home/user/guidebook")
W = ROOT / "workplan/2026-11-12-bidirectional-pipeline"
OUT = W / "REMEDIATION-PLAN.md"
TASKS = sorted(f for f in (W / "tasks").glob("T-[0-9]*-*.md") if not f.name.endswith("-design.md"))
LEDGER = (ROOT / "references/project-standards.md").read_text(encoding="utf-8").splitlines()
REGISTER = sorted(set(re.findall(r"^### (OD-\d+)", (W / "REMEDIATION-WORKPLAN.md").read_text(), re.M)), key=lambda x: int(x[3:]))


def last(od, kind):
    hits = [l for l in LEDGER if f"{od} {kind}:" in l]
    return hits[-1].split(f"{od} {kind}:", 1)[1].strip() if hits else ""


def gate(od, owner_only=False):
    """(open?, reason) per the ledger convention; owner_only: a task that needs the owner's words."""
    s, c = last(od, "STATUS"), last(od, "CHECK")
    if "ANSWERED BY THE OWNER" in s:
        return True, "owner"
    if "RESOLVED UNDER DELEGATION" in s and not owner_only:
        if "not required" in c or "confirmed" in c:
            return True, "delegated; " + c
        return False, "check: " + (c or "none")
    if "RESOLVED UNDER DELEGATION" in s:
        return False, "delegated, but this task needs the owner's words"
    return False, s or "no status line"


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
    designs = sorted(set(re.findall(r"(T-\d+-design\.md)", dep_txt)))
    dep_txt = re.sub(r"T-\d+-design\.md", "", dep_txt)
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
    dl_txt = bullet(s2, "Delegated resolutions")
    m = re.search(r"for n in ([^;]*);", dl_txt)
    dels = set(re.findall(r"OD-\d+", m.group(1))) if m else set()
    paths = sorted(set(re.findall(r"`((?:scripts|schemas|governance|skills|\.claude|\.github)/[A-Za-z0-9_./\-]+\.[a-z]+)`", s4)))
    paths = [p for p in paths if "/migrations/" not in p]
    if "RESEARCH" in cell(t, "Kind"):
        paths = []  # a research task writes rows through the sanctioned path; the tools it calls are not files it edits
    tasks[tid] = dict(
        id=tid, file=f.name, title=title, wave=cell(t, "Wave"), kind="RESEARCH" if "RESEARCH" in cell(t, "Kind") else "TOOLING",
        sonnet="NOT FOR SONNET" not in cell(t, "Executor"), hard=hard, soft=soft, ods=ods, dels=dels - ods, paths=paths,
        designs=[d for d in designs if not (W / "tasks" / d).exists()],
        piloted=bool(re.search(r"\*\*Pilot status\.\*\* \*\*Piloted", t)))

missing = sorted({d for t in tasks.values() for d in t["hard"] if d not in tasks})   # over every task file, merged or not

# --- merged tasks (see the docstring): out of the batches, and a dependency on one is satisfied
_branches = set(re.findall(r"/task/(\S+)\s*$", subprocess.run(["git", "log", "--merges", "--format=%s", "HEAD"], cwd=ROOT,
                                                               capture_output=True, text=True).stdout, re.M))
_squashed = set(re.findall(r"^(?:(T-\d+):|.*\bexecute workplan (T-\d+)\b).*\(#\d+\)\s*$", subprocess.run(
    ["git", "log", "--no-merges", "--format=%s", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout, re.M))
_squashed = {a or b for a, b in _squashed}
done = {tid: tasks.pop(tid) for tid in sorted(tasks, key=lambda x: int(x[2:]))
        if tasks[tid]["file"][:-3].lower() in _branches or tid in _squashed}
for t in tasks.values():
    t["hard"] -= set(done)
    t["soft"] -= set(done)

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


for t in tasks:
    tasks[t]["batch"] = depth(t)
nb = max(t["batch"] for t in tasks.values())

# --- status
def closed(t):
    """Decisions whose gate is CLOSED for this task, with the reason."""
    out = [(o, gate(o, True)[1]) for o in t["ods"] if not gate(o, True)[0]]
    out += [(o, gate(o)[1]) for o in t["dels"] if not gate(o)[0]]
    return sorted(out, key=lambda x: int(x[0][3:]))


def status(t):
    """READY, or every stop that applies, '; '-joined (the first word of each part is its kind)."""
    parts = []
    if closed(t):
        parts.append("OWNER: " + ", ".join(f"{o} ({r})" for o, r in closed(t)))
    if t["designs"]:
        parts.append("DESIGN: " + ", ".join(t["designs"]))
    if not t["sonnet"]:
        parts.append("NOT FOR SONNET")
    return "; ".join(parts) or "READY"


def kinds(t):
    return {p.split(":")[0] for p in status(t).split("; ")}


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
A(f"_Generated {now} from the {len(tasks) + len(done)} task files ({len(tasks)} open, {len(done)} merged) at commit {sha} by `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`. "
  "Nothing below is typed in: re-run the generator (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) after any task file changes, and trust the generator over this text (CLAUDE.md rule 7a)._\n")
A("**What this is.** The entry document for a Sonnet executor. `REMEDIATION-WORKPLAN.md` is the index (why, owner decision register, Definition of Done); `tasks/T-<id>-*.md` is the one self-contained file per task; this file says **in what order, in what groups, and where to stop.** "
  "Evidence base: `01-handshake-ledger.md` and the audit in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/`.\n")
A("## 1. How to execute\n")
A("1. **Merge this workplan first.** Every task file sets `$BASE` to `origin/main` once the workplan is on it, and to the workplan branch before that.")
A("2. **Take one batch at a time, in order.** A batch is the set of tasks whose hard dependencies all lie in earlier batches. Do not start batch *n* until every READY task of batch *n-1* is merged and its after-test is green on `$BASE`.")
A("3. **Inside a batch, work lanes in parallel and tasks in a lane serially.** A lane is a set of tasks that touch the same file (or that a task file says to sequence). Merge a lane's tasks in the order listed; where `REMEDIATION-WORKPLAN.md` gives its own merge order for some of them (Wave 0), that order wins, because it also accounts for the characterisation harness of T-014 which must exist before the changes it compares.")
A("4. **One task, one pull request, one executor, one task file.** Run the task's red test before, the same test after, the gate once (`scripts/preflight.sh --base \"$BASE\" --explain`), and the adversarial pass once before opening the pull request. Rule 9: open the pull request last, then unsubscribe.")
A("5. **Stop at a status that is not READY.** `OWNER: OD-nn (...)` means that decision's ledger gate is CLOSED for this task (the reason is in brackets); it opens when the ledger carries the owner's answer, or, for a decision the task names as delegated, a delegated resolution whose check is not required or confirmed. `DESIGN:` means the named design file does not exist yet. `NOT FOR SONNET` means an Opus-class session or the Fable agent does it. None is an invitation to improvise. The status is computed when this file is generated; the task's own gate, run at its start, is what binds.")
A("6. **Tooling merges before the research it unlocks (rule 10).** A research task never shares a pull request with tooling, and its row writes go only through the write path of CLAUDE.md §4.")
A("7. **The first execution of an unpiloted task is its pilot.** List any defect found in its task file in the pull request.\n")
A("## 2. The batches at a glance\n")
A("| Batch | Tasks | READY | OWNER-blocked (a gate CLOSED) | DESIGN file missing | NOT FOR SONNET | Tooling / research | Lanes |")
A("|---|---|---|---|---|---|---|---|")
for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    c = collections.Counter(k for t in ids for k in kinds(tasks[t]))
    A(f"| {b} | {len(ids)} | {c['READY']} | {c['OWNER']} | {c['DESIGN']} | {c['NOT FOR SONNET']} | {sum(tasks[t]['kind']=='TOOLING' for t in ids)} / {sum(tasks[t]['kind']=='RESEARCH' for t in ids)} | {len(lanes(ids))} |")
A("\nCounts are derived; the commands that check them: `ls workplan/2026-11-12-bidirectional-pipeline/tasks/T-[0-9]*-*.md | wc -l`, and the generator's own output.\n")
A("**Merged** (a merge commit on HEAD names the task's branch, or a squash commit's subject begins `T-nnn:` or says `execute workplan T-nnn` and ends `(#N)`; out of the batches below, and a dependency on one is satisfied; "
  "re-derive: `git log --merges --format=%s HEAD | grep -o 'task/t-[0-9a-z-]*'` and `git log --no-merges --format=%s HEAD | grep -E '^T-[0-9]+:|execute workplan T-[0-9]+' | grep -E '\\(#[0-9]+\\)$'`): "
  + (", ".join(f"[{t}](tasks/{done[t]['file']})" for t in done) or "none") + ".\n")
A(f"**Longest dependency chain ({len(crit)} tasks):** " + " → ".join(f"{t} ({tasks[t]['status']})" for t in crit) + ".\n")
if missing:
    A(f"**Dependencies naming a task with no file (fix the task file):** {', '.join(missing)}\n")

for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    A(f"## Batch {b}\n")
    if b == 1:
        A("**Entry:** the workplan is on the integration base. No open task is a prerequisite (a merged one may be: see **Merged** above).\n")
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
    own = sorted((t for t in ids if closed(tasks[t])), key=lambda x: int(x[2:]))
    des = sorted((t for t in ids if tasks[t]["designs"]), key=lambda x: int(x[2:]))
    stops = []
    if nfs:
        stops.append("not for Sonnet: " + ", ".join(nfs))
    if own:
        stops.append("a decision gate CLOSED: " + ", ".join(f"{t} ({'/'.join(o for o, _ in closed(tasks[t]))})" for t in own))
    if des:
        stops.append("a design file missing: " + ", ".join(f"{t} ({', '.join(tasks[t]['designs'])})" for t in des))
    A("\n**Exit:** every READY task above is merged and its section 6 after-test is green on `$BASE`; `scripts/preflight.sh --base \"$BASE\" --explain` is green on `$BASE`." +
      (f" **Stops in this batch:** {'; '.join(stops)}." if stops else "") + "\n")

A("## Owner decision queue, read from the ledger (what each answer releases)\n")
A("Every register decision (`grep -o -E '^### OD-[0-9]+' REMEDIATION-WORKPLAN.md`), its state by the ledger gate (the last `OD-NN STATUS:` and `OD-NN CHECK:` lines of `references/project-standards.md`), the tasks whose section 2 names it, and every task that waits on those through the hard dependencies. "
  "A decision named in a task's 'Owner decisions' bullet opens that task only on the owner's answer; one named in its 'Delegated resolutions' bullet opens on a delegated resolution whose check is not required or confirmed. "
  "The phone-ready prompts for the CLOSED ones are in `DECISION-CLOSURE.md`.\n")


def desc(ts):
    out, todo = set(), list(ts)
    while todo:
        x = todo.pop()
        for k, v in tasks.items():
            if x in v["hard"] and k not in out:
                out.add(k); todo.append(k)
    return sorted(out - set(ts), key=lambda x: int(x[2:]))


def readers(o):
    return sorted((t for t in tasks if o in tasks[t]["ods"] or o in tasks[t]["dels"]), key=lambda x: int(x[2:]))


blocking = [o for o in REGISTER if any(o in [x for x, _ in closed(tasks[t])] for t in readers(o))]
standing = [o for o in REGISTER if o not in blocking and not gate(o)[0]]
opened = [o for o in REGISTER if gate(o)[0]]
A(f"### Blocking: CLOSED, and a task's gate reads it ({len(blocking)})\n")
A("| Decision | Gate | Tasks it holds | Waiting on those (hard dependencies) | In batches |")
A("|---|---|---|---|---|")
for o in blocking:
    held = [t for t in readers(o) if o in [x for x, _ in closed(tasks[t])]]
    A(f"| {o} | CLOSED ({gate(o)[1]}) | {', '.join(held)} | {', '.join(desc(held)) or '—'} | {', '.join(str(b) for b in sorted({tasks[t]['batch'] for t in held}))} |")
A(f"\n### Standing, blocks no task: CLOSED, and no task's gate reads it ({len(standing)})\n")
A(", ".join(f"{o} ({gate(o)[1]})" for o in standing) or "none")
A(f"\n### Open by the ledger gate ({len(opened)})\n")
A("| Decision | Gate | Read by |")
A("|---|---|---|")
for o in opened:
    A(f"| {o} | OPEN ({gate(o)[1]}) | {', '.join(readers(o)) or 'no task gate'} |")
unreg = sorted({o for t in tasks.values() for o in t["ods"] | t["dels"]} - set(REGISTER), key=lambda x: int(x[3:]))
if unreg:
    A(f"\n**Named by a task but not in the register (fix the register):** {', '.join(unreg)}")
A("")
A("## NOT FOR SONNET\n")
A("| Task | Title | Batch | Decisions (owner's words / delegated) |")
A("|---|---|---|---|")
for t in sorted((t for t in tasks if not tasks[t]["sonnet"]), key=lambda x: int(x[2:])):
    x = tasks[t]
    A(f"| [{t}](tasks/{x['file']}) | {x['title'][:80]} | {x['batch']} | {', '.join(sorted(x['ods'])) or '—'} / {', '.join(sorted(x['dels'])) or '—'} |")
A("\nEach file says who does it. Everything that depends on one of these waits for it (the 'Reachable by Sonnet now' column names the blockers).\n")
A("## Where the pilots stand\n")
A("`grep -L \"Not piloted\" workplan/2026-11-12-bidirectional-pipeline/tasks/T-*.md` lists the tasks a pilot has touched. Results, defects found and what changed in the plan are in section 12 of `REMEDIATION-WORKPLAN.md` and in `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/pilot/`.\n")
OUT.write_text("\n".join(L))
print("tasks", len(tasks), "batches", nb, "missing deps", missing, "crit", len(crit), "merged", list(done))
print("decisions", len(REGISTER), "blocking", blocking, "standing", standing, "open", len(opened), "unregistered", unreg)
for b in range(1, nb + 1):
    ids = [t for t in tasks if tasks[t]["batch"] == b]
    print(b, len(ids), collections.Counter(k for t in ids for k in kinds(tasks[t])))
