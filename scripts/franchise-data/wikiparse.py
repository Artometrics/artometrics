import re,json,collections
def strip_tpl(s,names=('efn','refn','sfn','notetag','#tag')):
    out=[];i=0
    while i<len(s):
        m=re.match(r'\{\{\s*('+'|'.join(re.escape(n) for n in names)+r')\b',s[i:],re.I)
        if m:
            d=0
            while i<len(s):
                if s.startswith('{{',i):d+=1;i+=2
                elif s.startswith('}}',i):d-=1;i+=2
                else:i+=1
                if d==0:break
            continue
        out.append(s[i]);i+=1
    return ''.join(out)
def clean(s):
    s=s.replace('{{ndash}}','–').replace('{{estimation}}','').replace('{{nbsp}}',' ')
    s=re.sub(r'<ref[^>/]*/>','',s);s=re.sub(r'<ref[^>]*>.*?</ref>','',s,flags=re.S)
    s=strip_tpl(s)
    s=re.sub(r'\{\{US\$\|([^|}]+)[^}]*\}\}',r'$\1',s)
    s=re.sub(r'\{\{sort\s*\|[^|]*\|([^}]*)\}\}',r'\1',s)
    s=re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]',r'\2',s);s=re.sub(r'\[\[([^\]]+)\]\]',r'\1',s)
    s=re.sub(r"''+",'',s);s=re.sub(r'<br\s*/?>',' ',s);s=re.sub(r'<[^>]+>','',s)
    s=re.sub(r'\{\{[^{}]*\}\}','',s)
    return s
def amt(t):
    m=re.search(r'\$\s*([0-9.,]+)\s*(billion|million)',t,re.I)
    if not m:return None
    v=float(m.group(1).replace(',',''));return v if m.group(2).lower()=='billion' else v/1000
def parse(w):
    rows=[]
    for b in re.split(r'\n\|-',w):
        m=re.search(r'^\s*!\s*scope="?row"?\s*\|\s*(.+)$',b,re.M)
        if not m:continue
        name=re.sub(r'\s+',' ',clean(m.group(1))).strip()
        body=b[m.end():]
        cells=re.split(r'\n\|(?!\})',body)
        cells=[c for c in cells if c.strip()!='' or True][1:]
        if len(cells)<3:continue
        year=re.sub(r'[^0-9].*','',clean(cells[0]).strip())
        total=amt(clean(cells[1]))
        bd=[];
        for line in clean(cells[2]).split('\n'):
            line=line.strip().lstrip('*').strip()
            if not line:continue
            mm=re.match(r'(.+?)\s*[–—-]\s*(\$.*)',line)
            if mm and amt(mm.group(2)) is not None: bd.append((mm.group(1).strip(),amt(mm.group(2))))
        orig=re.sub(r'\s+',' ',clean(cells[3])).strip() if len(cells)>3 else ''
        creators=re.sub(r'\s+',' ',clean(cells[4])).strip() if len(cells)>4 else ''
        owners=re.sub(r'\s+',' ',clean(cells[5])).strip() if len(cells)>5 else ''
        rows.append(dict(franchise=name,year_created=year,total=total,breakdown=bd,original_media=orig,creators=creators,owners=owners))
    return rows

def parse_2019(w):
    rows=[]
    w=w.replace('{{ndash}}','–')
    for b in re.split(r'\n\|-',w):
        cells=re.split(r'\n[|!](?![}-])',b)[1:]
        if len(cells)<4: continue
        name=re.sub(r'\s+',' ',clean(cells[0])).strip()
        tot=amt(clean(cells[2]))
        if not name or tot is None: continue
        bd=[]
        for line in clean(cells[3]).split('\n'):
            line=line.strip().lstrip('*').strip();mm=re.match(r'(.+?)\s*[–—-]\s*(\$.*)',line)
            if mm and amt(mm.group(2)) is not None: bd.append((mm.group(1).strip(),amt(mm.group(2))))
        rows.append(dict(franchise=name,total=tot,breakdown=bd))
    return rows
