#!/bin/bash
# usage: cells.sh <db> <outdir>   -- engine over every parameter, several lenses, one scratch DB
DB=$1; OUT=$2; mkdir -p $OUT
run() { # label param lensflags...
  label=$1; p=$2; shift 2
  GUIDEBOOK_DB_PATH=$DB python3 scripts/assess/assess_cell.py --db $DB --emit-sql $OUT/$label.sql --parameter-id $p --slug stress-test "$@" --session session_2026-10-22-stress-test --stamp '2026-10-22 02:00:00' --report-json $OUT/$label.json > $OUT/$label.log 2>&1
  echo "$label rc=$?"
}
run p3_MOB 3 --identity MOB
run p3_ICF 3 --icf d450
run p3_NEED 3 --needs A-EFFORT
run p3_MOB_ICF 3 --identity MOB --icf d450
for p in 4 5 6 7 8 9 10 11 12; do run p${p}_MOB $p --identity MOB; done
