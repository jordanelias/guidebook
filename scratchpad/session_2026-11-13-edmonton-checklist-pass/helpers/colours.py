import fitz, json, collections, re, sys
pdf = sys.argv[1]
doc = fitz.open(pdf)
cols = collections.Counter()
rows = []
for pno, page in enumerate(doc):
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"]
                if not t.strip(): continue
                cols[("%06x" % s["color"])] += len(t)
                rows.append((pno, round(l["bbox"][1]), "%06x" % s["color"], t))
print(cols.most_common(8))
json.dump(rows, open(sys.argv[2], "w"))
