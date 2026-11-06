import sys,re,html
s=open(sys.argv[1],encoding='utf-8').read()
s=re.sub(r'(?s)<meta>.*?</meta>','',s)
s=re.sub(r'\s+',' ',s)
s=re.sub(r'</(?:[a-z]+:)?(p|heading|num|intro|content|subsection|section|chapter|item|point|docTitle|docNumber|paragraph|preface|preamble)>','\n',s)
s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
s='\n'.join(l.strip() for l in s.split('\n') if l.strip())
open(sys.argv[2],'w',encoding='utf-8').write(s+'\n')
