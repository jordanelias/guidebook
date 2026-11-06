"""ctx.py <textfile> <regex> [n]: print page (form-feed count + 1), line within page, and the line with neighbours."""
import sys, re
t = open(sys.argv[1], encoding='utf-8').read(); rx = re.compile(sys.argv[2], re.I); n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
pages = t.split('\f'); k = 0
for pi, pg in enumerate(pages, 1):
    L = pg.split('\n')
    for li, l in enumerate(L, 1):
        if rx.search(l):
            k += 1
            if k > n: sys.exit()
            ctx = ' '.join(x.strip() for x in L[max(0, li - 2):li + 1])
            print(f'p{pi} l{li}: {re.sub(" +", " ", ctx)[:330]}')
