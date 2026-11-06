import sys
sys.path.insert(0,'scripts/research')
import retrieval_log as rl
SESS='session_2026-11-06-pipeline-batch-2'
for tag,u in (('awm-app2','https://www.corada.com/documents/anthropometry-of-WhM-project/appendix-two-pathway-width-180-turn'),
              ('core','https://core.ac.uk/download/357366754.pdf'),
              ('awm-index','https://corada.com/documents/anthropometry-of-WhM-project/2-3-3')):
    r=rl.fetch(u,session=SESS,purpose=f'R10 retrieval of a hit from WebSearch W2 ({tag})')
    print(tag, type(r))
