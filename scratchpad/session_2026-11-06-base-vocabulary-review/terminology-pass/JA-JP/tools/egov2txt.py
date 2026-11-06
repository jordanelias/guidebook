import json, sys, hashlib
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src, encoding='utf-8'))
lines = []
def text(n):
    if isinstance(n, str): return n
    if n.get('tag') == 'Rt': return ''   # ruby reading (furigana) dropped; base text kept
    sep = ' ' if any(isinstance(c, dict) and c.get('tag') == 'Column' for c in n.get('children', [])) else ''
    return sep.join(text(c) for c in n.get('children', []))
BLOCK = {'ArticleTitle','ArticleCaption','ParagraphNum','ItemTitle','Subitem1Title','Subitem2Title','Subitem3Title','Sentence','Column','ChapterTitle','SectionTitle','SubsectionTitle','LawTitle','LawNum','SupplProvisionLabel','TableColumn','Remarks','RemarksLabel','EnactStatement'}
def walk(n, ctx):
    if isinstance(n, str): return
    tag = n.get('tag'); a = n.get('attr', {})
    if tag == 'Article': ctx = ctx + ['Art.' + a.get('Num', '?')]
    if tag == 'Paragraph': ctx = ctx + ['para' + a.get('Num', '?')]
    if tag == 'Item': ctx = ctx + ['item' + a.get('Num', '?')]
    if tag and tag.startswith('Subitem') and 'Num' in a: ctx = ctx + [tag[-1] + ':' + a['Num']]
    if tag == 'SupplProvision': ctx = ['Suppl' + (a.get('AmendLawNum') or '')]
    if tag in ('ChapterTitle','SectionTitle','ArticleCaption','ArticleTitle','LawTitle','SupplProvisionLabel'):
        lines.append('[%s] %s %s' % ('/'.join(ctx), tag, text(n))); return
    # emit sentence-bearing leaf groups once per Paragraph/Item/Subitem text node
    if tag in ('ParagraphSentence','ItemSentence') or (tag and tag.startswith('Subitem') and tag.endswith('Sentence')) or tag=='TableColumn':
        lines.append('[%s] %s' % ('/'.join(ctx), text(n))); return
    if tag in ('ParagraphNum','ItemTitle') or (tag and tag.startswith('Subitem') and tag.endswith('Title')):
        return
    for c in n.get('children', []): walk(c, ctx)
walk(d['law_full_text'], [])
s = '\n'.join(lines) + '\n'
open(out, 'w', encoding='utf-8').write(s)
print(out, len(lines), hashlib.sha256(s.encode()).hexdigest())
