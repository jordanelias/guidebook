#!/usr/bin/env bash
# Stop the stop-hook/push loop at its source. Run once:
#
#     bash scratchpad/wiring-sweep-04rjhv/fix-stop-hook-loop.sh
#
# WHAT THE LOOP IS. ~/.claude/stop-hook-git-check.sh fails the turn while the
# working tree is dirty. In this repository two tracked files append on every
# turn by design:
#
#     transcripts/harness_*/main.jsonl          grows when the agent writes anything
#     scratchpad/<session>/commands.jsonl       grows on every Bash call
#
# So the tree is dirty again the instant the agent answers the hook. The check is
# not one an agent fails to satisfy — it is UNSATISFIABLE BY CONSTRUCTION while a
# session is live, and each cycle costs a commit and a push. On 2026-09-17 it ran
# about fifteen times in one session, ~150-200k tokens, producing nothing but
# transcript commits. CLAUDE.md rule 6 already names this shape: a check that is
# red by construction teaches its reader to ignore it.
#
# WHAT THIS CHANGES. The hook gains a per-repo opt-out list read from git config,
# so it stays strict everywhere else. Unpushed-commit and signature checks are
# untouched: real work is still caught.
#
# Written by the agent rather than applied by it: editing ~/.claude/ is refused
# here as self-modification, which is the right refusal. This is the patch, for a
# human to run.
set -euo pipefail

HOOK="$HOME/.claude/stop-hook-git-check.sh"
[ -f "$HOOK" ] || { echo "no hook at $HOOK — nothing to do"; exit 0; }

if grep -q 'stophook.ignorePath' "$HOOK"; then
  echo "hook already patched"
else
  cp "$HOOK" "$HOOK.bak"
  python3 - "$HOOK" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()

anchor = """# Check for uncommitted changes (both staged and unstaged)
if ! git diff --quiet || ! git diff --cached --quiet; then"""
patch = """# Paths this repo has opted out of the dirty check. The case this exists for is
# an append-only session log that grows on EVERY turn — a transcript, a command
# log. Such a file makes the tree dirty again the instant the agent writes its
# next reply, so the check can never be satisfied while a session is live: an
# infinite generator, and the agent answering it pushes in a loop. Opt in per
# repo, never globally:
#   git config --add stophook.ignorePath transcripts/
#   git config --add stophook.ignorePath '*commands.jsonl'
ignore_spec=()
while IFS= read -r p; do
  [[ -n "$p" ]] && ignore_spec+=(":(exclude)$p")
done < <(git config --get-all stophook.ignorePath 2>/dev/null)
if [[ ${#ignore_spec[@]} -gt 0 ]]; then
  ignore_spec=(':/' "${ignore_spec[@]}")
fi

# Check for uncommitted changes (both staged and unstaged)
if ! git diff --quiet -- "${ignore_spec[@]}" || ! git diff --cached --quiet -- "${ignore_spec[@]}"; then"""
assert anchor in s, "dirty-check anchor not found — hook has changed; patch by hand"
s = s.replace(anchor, patch, 1)

old_u = 'untracked_files=$(git ls-files --others --exclude-standard)'
new_u = 'untracked_files=$(git ls-files --others --exclude-standard -- "${ignore_spec[@]}")'
assert old_u in s, "untracked anchor not found — hook has changed; patch by hand"
s = s.replace(old_u, new_u, 1)
p.write_text(s)
print("hook patched (backup at .bak)")
PY
  bash -n "$HOOK" && echo "syntax OK"
fi

cd "$(dirname "$0")/../.."
git config --get-all stophook.ignorePath | grep -qx 'transcripts/' \
  || git config --add stophook.ignorePath 'transcripts/'
git config --get-all stophook.ignorePath | grep -qx '*commands.jsonl' \
  || git config --add stophook.ignorePath '*commands.jsonl'

echo "repo opt-out list:"
git config --get-all stophook.ignorePath | sed 's/^/  /'
echo
echo "verify — should print CLEAN once only the session logs are dirty:"
echo '  git diff --quiet -- :/ ":(exclude)transcripts/" ":(exclude)*commands.jsonl" && echo CLEAN || echo DIRTY'
