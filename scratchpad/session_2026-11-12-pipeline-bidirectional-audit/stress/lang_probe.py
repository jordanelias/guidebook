#!/usr/bin/env python3
"""Per-script probe of the live text guards. Reads only; prints JSON.
Usage: python3 -I lang_probe.py '<json {label: string}>'
Loads the repo's functions by path and applies them to the given strings:
  - research/retrieval_log.normalise_quote   (quote verification)
  - db._name_tokens / db._VALUE_BEARING_NAME (term-name screens)
Reports normalised form, token set, whether a value-bearing screen fires, and
any set of DIFFERENT input strings that normalise to the SAME text (a collision).
"""
import importlib.util, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3] / "scripts"  # the scripts live inside the checkout they test
sys.path.insert(0, str(R))

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, R / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

out = {"errors": {}}
mods = {}
for n, rel in (("rl", "research/retrieval_log.py"), ("dbmod", "db.py")):
    try:
        mods[n] = load(n, rel)
    except BaseException as e:  # noqa
        out["errors"][n] = repr(e)
strings = json.loads(sys.argv[1])
res = {}
for label, s in strings.items():
    r = {"input": s}
    for fn, key in ((("rl", "normalise_quote"), "rl.normalise_quote"),):
        try:
            r[key] = getattr(mods[fn[0]], fn[1])(s)
        except BaseException as e:  # noqa
            r[key] = f"ERROR {e!r}"
    try:
        r["db._name_tokens"] = sorted(mods["dbmod"]._name_tokens(s))
    except BaseException as e:  # noqa
        r["db._name_tokens"] = f"ERROR {e!r}"
    try:
        r["db._VALUE_BEARING_NAME_fires"] = bool(mods["dbmod"]._VALUE_BEARING_NAME.search(s))
    except BaseException as e:  # noqa
        r["db._VALUE_BEARING_NAME_fires"] = f"ERROR {e!r}"
    res[label] = r
out["per_string"] = res
for key in ("rl.normalise_quote",):
    g = {}
    for label, r in res.items():
        v = r.get(key)
        if isinstance(v, str) and not v.startswith("ERROR"):
            g.setdefault(v, []).append(label)
    out["collisions_" + key] = [v for v in g.values() if len(v) > 1]
# strings whose name-token set is empty (the near-match refusal examines nothing)
out["empty_name_token_sets"] = [l for l, r in res.items() if r["db._name_tokens"] == []]
print(json.dumps(out, ensure_ascii=False, indent=1))
