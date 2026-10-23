#!/bin/bash
# regress_2026-10-22.sh -- re-run the 2026-10-22 stress test on scratch copies. Never writes the repository.
# usage: regress_2026-10-22.sh <repo> <outdir>
set -u
REPO=${1:-/home/user/guidebook}; R=${2:?outdir}; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$R"/cells "$R"/lens
SESSION=session_2026-10-22-regression; STAMP='2026-10-22 05:00:00'
echo "canonical sha256 before: $(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)"
cp "$REPO/data/guidebook.db" "$R/lens.db"; cp "$REPO/data/guidebook.db" "$R/cells.db"
eng() { local db=$1 od=$2 label=$3 p=$4; shift 4
  (cd "$REPO" && GUIDEBOOK_DB_PATH=$db python3 scripts/assess/assess_cell.py --db "$db" --emit-sql "$od/$label.sql" \
     --parameter-id "$p" --slug stress-test "$@" --session $SESSION --stamp "$STAMP" --report-json "$od/$label.json" \
     > "$od/$label.log" 2>&1); echo "$label rc=$?"; }
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
echo "== 2. every parameter under MOB (the populated scratch)"
for p in $(python3 -c "import sqlite3;print(' '.join(str(r[0]) for r in sqlite3.connect('file:$REPO/data/guidebook.db?mode=ro',uri=True).execute(\"select parameter_id from base_parameters where status='active' order by 1\")))"); do
  eng "$R/cells.db" "$R/cells" p${p}_MOB $p --identity MOB; done
python3 -I - "$R/cells.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
for r in c.execute("select parameter_id, state, marker, derivation_paths, value_max, substr(value_note,1,90) "
                   "from specifications where retired_at is null order by 1"): print(r)
PY
echo "== 3. fixtures G1-G13";  python3 -I "$HERE/fixtures_g1_g13.py" "$REPO"
echo "== 4. notation probes";  python3 -I "$HERE/notation_probe.py" "$REPO"
echo "== 5. walkability"
(cd "$REPO" && python3 workplan/pipeline-state-graph/walkability.py data/guidebook.db > "$R/walk_canonical.txt" 2>&1
 python3 workplan/pipeline-state-graph/walkability.py "$R/cells.db" > "$R/walk_populated.txt" 2>&1)
grep -c "render *NO PATH" "$R/walk_canonical.txt" "$R/walk_populated.txt"
echo "== 6. render attempt"; [ -f "$HERE/render_attempt.py" ] && python3 -I "$HERE/render_attempt.py" "$R/cells.db" | head -30
echo "== 7. write path: capture, emit, apply, rebuild in a scratch clone"
rm -rf "$R/clone"; mkdir -p "$R/clone"
git -C "$REPO" archive HEAD CLAUDE.md requirements.txt data governance references schemas scripts | tar -x -C "$R/clone"
(cd "$R/clone" && GUIDEBOOK_DB_PATH="$R/cells.db" python3 scripts/research/emit_batch_sql.py --scratch "$R/cells.db" \
   --canonical data/guidebook.db --out "$R/batch.sql" 2>&1 | tail -2)
grep -oE '^INSERT INTO "?[a-z_]+' "$R/batch.sql" | sort | uniq -c
(cd "$R/clone" && python3 scripts/emit_data_migration.py --session $SESSION.md --summary "regression replay" \
   --input "$R/batch.sql" 2>&1 | tail -1 && python3 scripts/migrate_db.py --session $SESSION 2>&1 | tail -2)
(cd "$R/clone" && timeout 900 python3 scripts/migrate_db.py --rebuild "$R/rebuilt.db" 2>&1 | tail -1)
python3 -I - "$R/clone/data/guidebook.db" "$R/rebuilt.db" <<'PY'
import sqlite3, sys
a, b = (sqlite3.connect(f"file:{p}?mode=ro", uri=True) for p in sys.argv[1:3])
ts = [t for (t,) in a.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
d = [(t, a.execute(f'select count(*) from "{t}"').fetchone()[0], b.execute(f'select count(*) from "{t}"').fetchone()[0]) for t in ts]
print("EXAMINED tables:", len(d), "| differing:", [x for x in d if x[1] != x[2]])
PY
echo "canonical sha256 after:  $(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)"
