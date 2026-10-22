#!/bin/bash
# Re-run the 2026-10-22 stress test end to end on scratch copies. Never writes the repository.
# usage: regress_2026-10-22.sh <repo> <outdir>
set -u
REPO=${1:-/home/user/guidebook}; R=${2:?outdir}; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$R"/cells "$R"/lens
SESSION=session_2026-10-22-regression; STAMP='2026-10-22 05:00:00'
SHA0=$(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)
echo "canonical sha256 before: $SHA0"
cp "$REPO/data/guidebook.db" "$R/lens.db"; cp "$REPO/data/guidebook.db" "$R/cells.db"
eng() { # db outdir label param lensflags...
  local db=$1 od=$2 label=$3 p=$4; shift 4
  (cd "$REPO" && GUIDEBOOK_DB_PATH=$db python3 scripts/assess/assess_cell.py --db "$db" --emit-sql "$od/$label.sql" \
     --parameter-id "$p" --slug stress-test "$@" --session $SESSION --stamp "$STAMP" --report-json "$od/$label.json" \
     > "$od/$label.log" 2>&1); echo "$label rc=$?"
}
echo "== 1. lens runs, parameter 3"
eng "$R/lens.db" "$R/lens" MOB 3 --identity MOB
eng "$R/lens.db" "$R/lens" MOB_d450 3 --identity MOB --icf d450
for L in AUT BLIND ADHD; do eng "$R/lens.db" "$R/lens" $L 3 --identity $L; done
eng "$R/lens.db" "$R/lens" d450 3 --icf d450
eng "$R/lens.db" "$R/lens" A-EFFORT 3 --needs A-EFFORT
python3 -I - "$R/lens" <<'PY'
import json, glob, sys, os
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    r = json.load(open(f))[0]
    print(f"{os.path.basename(f)[:-5]:<10} state={r['state']:<11} marker={r['marker']} gov={len(r['governing_refs'])} "
          f"min={r['value_min']} max={r['value_max']} sha={r['derivation_sha'][:12]}")
PY
python3 -I - "$R/lens.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
for r in c.execute("select identity_code, icf_code, needs_code, state, derivation_paths, substr(derivation_rationale,1,60) "
                   "from specifications where retired_at is null order by specification_id"): print(r)
PY
echo "== 2. every parameter under MOB (the populated scratch)"
for p in 3 4 5 6 7 8 9 10 11 12; do eng "$R/cells.db" "$R/cells" p${p}_MOB $p --identity MOB; done
python3 -I - "$R/cells/p3_MOB.json" <<'PY'
import json, sys; r = json.load(open(sys.argv[1]))[0]; print("p3 MOB value_note:", r["value_note"])
PY
echo "== 3. fixtures G1-G13";  python3 -I "$HERE/fixtures_g1_g13.py" "$REPO"
echo "== 4. notation probes";  python3 -I "$HERE/notation_probe.py" "$REPO"
echo "== 5. walkability, canonical and populated"
(cd "$REPO" && python3 workplan/pipeline-state-graph/walkability.py data/guidebook.db > "$R/walk_canonical.txt" 2>&1
 python3 workplan/pipeline-state-graph/walkability.py "$R/cells.db" > "$R/walk_populated.txt" 2>&1)
grep -c "render *NO PATH" "$R/walk_canonical.txt" "$R/walk_populated.txt"
echo "== 6. render attempt on the populated scratch"; python3 -I "$HERE/render_attempt.py" "$R/cells.db" 2>&1 | head -30
echo "== 7. write path replay and rebuild in a scratch clone"
rm -rf "$R/clone"; mkdir -p "$R/clone"
git -C "$REPO" archive HEAD CLAUDE.md requirements.txt data governance references schemas scripts | tar -x -C "$R/clone"
(cd "$R/clone" && GUIDEBOOK_DB_PATH="$R/cells.db" python3 scripts/research/emit_batch_sql.py --scratch "$R/cells.db" \
   --canonical data/guidebook.db --out "$R/batch.sql" 2>&1 | tail -3)
grep -oE '^INSERT INTO "?[a-z_]+' "$R/batch.sql" | sort | uniq -c
(cd "$R/clone" && python3 scripts/emit_data_migration.py --session $SESSION.md --summary "regression replay" \
   --input "$R/batch.sql" 2>&1 | tail -2 && python3 scripts/migrate_db.py --session $SESSION 2>&1 | tail -3)
(cd "$R/clone" && timeout 900 python3 scripts/migrate_db.py --rebuild "$R/rebuilt.db" 2>&1 | tail -2)
python3 -I - "$R/clone/data/guidebook.db" "$R/rebuilt.db" <<'PY'
import sqlite3, sys
a, b = (sqlite3.connect(f"file:{p}?mode=ro", uri=True) for p in sys.argv[1:3])
ts = [t for (t,) in a.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
diff = [(t, a.execute(f'select count(*) from "{t}"').fetchone()[0], b.execute(f'select count(*) from "{t}"').fetchone()[0])
        for t in ts]
print("EXAMINED tables:", len(diff), "| differing:", [d for d in diff if d[1] != d[2]])
PY
echo "canonical sha256 after:  $(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)"
