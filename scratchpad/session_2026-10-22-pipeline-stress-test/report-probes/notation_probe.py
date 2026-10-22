"""Notation probes over the engine's reader. Usage: python3 -I notation_probe.py /home/user/guidebook"""
import sys
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/user/guidebook"
for p in ("scripts/assess", "scripts", ""):
    sys.path.insert(0, f"{REPO}/{p}".rstrip("/"))
from assess_cell import bound_on_scale
cases = [("1:12", "rise:run ratio", "<=", "numerical"), ("8.33", "%", "<=", "numerical"),
         ("8.33%", "%", "<=", "numerical"), ("1 in 12", "rise:run ratio", "<=", "numerical"),
         ("12:1", "rise:run ratio", "<=", "numerical"), ("1/12", "rise:run ratio", "<=", "numerical"),
         ("1:12", "ratio", "<=", "numerical"), ("5", "gradient", "<=", "numerical"),
         ("viisi prosenttia", "%", "<=", "numerical"), ("0-4.8", "%", "between", "range"),
         ("1:6 to 1:14", "rise:run ratio", "between", "range"), ("5", "degrees", "<=", "numerical"),
         ("36", "in", ">=", "numerical"), ("900", "mm", ">=", "numerical"), ("1200", "mm", None, "numerical")]
for v, u, c, ct in cases:
    b = bound_on_scale(v, u, c, ct)
    fmt = None if b is None else tuple(None if x is None else float(x) for x in b)
    print(f"{v!r:>20} unit={u!r:<18} cmp={c!r:<10} -> {fmt}")
