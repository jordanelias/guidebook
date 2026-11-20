"""Compare two independent English translations of the same original cell.

Run: python3 -I compare_translations.py originals.json opus.json sonnet.json
  originals.json: [{"id": "<table>:<column>:<key>", "lang", "text"}]
  opus.json:      {"<key>": "<english>"}            (first translation, keyed by the id's last part)
  sonnet.json:    [{"id", "text"}]                   (blind second translation)

A cell passes when, after normalising decimal commas, spelled-out fractions and percents, and
metre/centimetre/millimetre spellings, the two texts hold the same numbers and the same unit
tokens. It does NOT judge meaning: a wording difference is printed for a reader. It prints
EXAMINED: <n>. It exits 1 when any cell differs.
"""
import json
import re
import sys

FRAC = {"twelfth": 12, "eighth": 8, "fifteenth": 15, "twentieth": 20, "sixth": 6, "tenth": 10}


def norm(t: str) -> str:
    t = t.lower()
    t = re.sub(r"(\d),(\d)", r"\1.\2", t)
    t = re.sub(r"\bone-(%s)\b" % "|".join(FRAC), lambda m: "1/%d" % FRAC[m.group(1)], t)
    for word, n in (("five", 5), ("four", 4), ("eight", 8)):
        t = re.sub(r"\b%s (?:per ?cent|percent)\b" % word, "%d%%" % n, t)
    t = re.sub(r"(\d)\s*(?:per ?cent|percent)\b", r"\1%", t)
    t = re.sub(r"(\d)\s+%", r"\1%", t)
    t = re.sub(r"\bmetres?\b|\bmeters?\b", "m", t)
    t = re.sub(r"\bcentimet(?:re|er)s?\b", "cm", t)
    t = re.sub(r"\bmillimet(?:re|er)s?\b", "mm", t)
    t = re.sub(r"(\d) (\d{3})\b", r"\1\2", t)
    t = re.sub(r"(\d)\s*:\s*(\d)", r"\1:\2", t)
    return re.sub(r"\b(\d+)\.0+\b", r"\1", t)


def numbers(t: str) -> list:
    return sorted(re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", t))


def units(t: str) -> list:
    return sorted(re.findall(r"%|mm|cm|km|\bm\b|°|degree", t))


def main(orig_path: str, first_path: str, second_path: str) -> int:
    originals = {x["id"]: x for x in json.load(open(orig_path, encoding="utf-8"))}
    first = json.load(open(first_path, encoding="utf-8"))
    second = {x["id"]: x["text"] for x in json.load(open(second_path, encoding="utf-8"))}
    differ = []
    for cell in originals:
        a, b = norm(first[cell.split(":")[-1]]), norm(second[cell])
        if numbers(a) != numbers(b) or units(a) != units(b):
            differ.append(cell)
    for cell in differ:
        print("DIFFERS", cell)
    print(f"EXAMINED: {len(originals)}")
    print(f"differ: {len(differ)}")
    return 1 if differ else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
