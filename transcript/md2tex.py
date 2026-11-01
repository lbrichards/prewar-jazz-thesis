#!/usr/bin/env python3
# Convert merged_ja.md -> body_ja.tex + bib_ja.tex, preserving every character.
import re, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
OUT = "../latex_ja/"

# ---- figure mapping: page -> (file, caption). Only these pages get an image. ----
FIGS = {
 10: ("fig01_standard_blues_form", "STANDARD BLUES FORM（12小節ブルースの標準和音進行）", 1.0),
 28: ("fig02_tokyo_koshinkyoku", "《東京行進曲》（昭和四年）　西條八十作詞・中山晋平作曲", 1.0),
 30: ("fig03_speed_jidai", "《スピード時代》　高階哲夫作曲・サトウハチロウ作詞（著者採譜）", 0.92),
 32: ("fig04_dinah_solo", "南里文雄の《ダイナ》ソロ採譜　♩=126（著者採譜）", 1.0),
 34: ("fig05_wakare_no_blues", "《別れのブルーズ》　服部良一作曲・藤浦洸作詞（著者採譜）", 0.78),
}
SKIP_FIG_PAGES = {31, 33, 36, 54, 55}  # markers that are text, not images

SENT_END = tuple("。！？」）.!?)")

def esc(s):
    # protect * emphasis first
    s = re.sub(r'\*\*(.+?)\*\*', lambda m: '\x01'+m.group(1)+'\x02', s)
    s = re.sub(r'\*(.+?)\*',    lambda m: '\x03'+m.group(1)+'\x04', s)
    for a,b in [('\\','\\textbackslash '),('&','\\&'),('%','\\%'),('#','\\#'),
                ('_','\\_'),('$','\\$'),('{','\\{'),('}','\\}'),('~','\\textasciitilde '),
                ('^','\\textasciicircum ')]:
        s = s.replace(a,b)
    s = s.replace('\x01','\\textbf{').replace('\x02','}')
    s = s.replace('\x03','\\textit{').replace('\x04','}')
    return s

def heading_cmd(txt):
    t = txt.strip()
    if re.match(r'^第[一二三四五六七八九十]+章', t) or t.startswith('文献目録'):
        return '\\section', t
    if re.match(r'^[A-D][\.．]', t):
        return '\\subsection', t
    if re.match(r'^[0-9]+[\.．]', t):
        return '\\subsubsection', t
    return '\\subsection', t

CHORD = re.compile(r'^[　\s]*[（(]?[A-G][b#♭]?m?(7|△|dim)?[,，\sABCDEFG#♭b7mFm・（）()]*$')
LABELS = ('和音進行','歌詞','（歌）','(歌)','（著者採譜）','(著者採譜)','（トランペット間奏）')
def is_verse(line):
    s=line.strip()
    if not s: return False
    if any(s.startswith(x) or s==x for x in LABELS): return True
    if len(s)<=40 and CHORD.match(s) and re.search(r'[A-G]',s): return True
    return False

def read_lines():
    raw=open("merged_ja.md",encoding="utf-8").read()
    raw=re.sub(r'<!--.*?-->','',raw,flags=re.S)        # drop all HTML comments (multi-line too)
    for ln in raw.split("\n"):
        ln=ln.rstrip()
        st=ln.strip()
        if re.fullmatch(r'-{3,}', st): continue           # stray md horizontal rules
        if re.fullmatch(r'\[(CLIPPED|UNSURE|reconstruction|degraded|\.\.\.)[^\]]*\]', st): continue
        yield ln

def convert():
    body, bib = [], []
    cur = body
    para=[]; quote=[]; verse=[]
    in_bib=False
    def flush_para():
        nonlocal para
        if para:
            cur.append(esc("".join(para))); cur.append("")
            para=[]
    def flush_quote():
        nonlocal quote
        if quote:
            cur.append("\\begin{gquote}")
            # \x00 marks an internal paragraph break; survives esc(), restored to \par after
            body=esc("".join(quote)).replace("\x00","\\par{}")
            cur.append(body)
            cur.append("\\end{gquote}"); cur.append("")
            quote=[]
    vmode=["verseblock"]
    def flush_verse():
        nonlocal verse
        if verse:
            items=[]; gap=[]; blank=False
            for v in verse:
                if not v.strip(): blank=True; continue
                items.append(v.strip()); gap.append(blank); blank=False
            if items:
                env=vmode[0]
                cur.append("\\begin{%s}"%env)
                for i,txt in enumerate(items):
                    term = ("\\\\[0.9em]" if gap[i+1] else "\\\\") if i<len(items)-1 else ""
                    cur.append(esc(txt)+term)
                cur.append("\\end{%s}"%env); cur.append("")
            verse=[]
    tbl=[]
    def flush_table():
        nonlocal tbl
        if tbl:
            rows=[r for r in tbl if not re.match(r'^\s*\|[\s:|-]+\|\s*$',r)]  # drop |---| separator
            parsed=[[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
            ncol=max(len(r) for r in parsed)
            if ncol<=1:
                colspec="@{}p{0.9\\linewidth}@{}"
            elif ncol==2:
                colspec="@{}p{0.26\\linewidth}@{\\hspace{1em}}p{0.62\\linewidth}@{}"
            else:
                colspec="@{}"+("l "*ncol)+"@{}"
            cur.append("\\par\\smallskip{\\small\\begin{longtable}{%s}"%colspec)
            for ri,r in enumerate(parsed):
                cells=[esc(c) for c in r]+[""]*(ncol-len(r))
                line=" & ".join(cells)+" \\\\"
                cur.append(line)
                if ri==0: cur.append("\\hline")
            cur.append("\\end{longtable}}"); cur.append("")
            tbl=[]
    def flush_all():
        flush_para(); flush_quote(); flush_verse(); flush_table()

    verse_fence=[False]
    for raw in read_lines():
        line=raw
        s=line.strip()
        # explicit verse / list fences
        if s==":::verse":
            flush_all(); vmode[0]="verseblock"; verse_fence[0]=True; continue
        if s==":::list":
            flush_all(); vmode[0]="listblock"; verse_fence[0]=True; continue
        if s==":::" and verse_fence[0]:
            flush_verse(); verse_fence[0]=False; vmode[0]="verseblock"; continue
        if verse_fence[0]:
            verse.append(line); continue
        # markdown tables
        if s.startswith("|") and s.count("|")>=2:
            flush_para(); flush_quote(); flush_verse()
            tbl.append(line); continue
        else:
            flush_table()
        # headings
        if line.lstrip().startswith("#"):
            flush_all()
            txt=line.lstrip().lstrip("#").strip()
            cmd,t=heading_cmd(txt)
            if t.startswith("文献目録"):
                in_bib=True; cur=bib
            cur.append(f"{cmd}{{{esc(t)}}}"); cur.append("")
            continue
        # figure markers
        mfig=re.match(r'\[\[FIGURE page=(\d+)',s)
        if mfig:
            flush_all()
            pg=int(mfig.group(1))
            if pg in FIGS and pg not in SKIP_FIG_PAGES:
                fn,cap,w=FIGS[pg]
                cur += ["\\begin{figure}[H]","\\centering",
                        f"\\includegraphics[width={w}\\linewidth]{{figures/{fn}}}",
                        f"\\caption{{{esc(cap)}}}","\\end{figure}",""]
            continue
        # quote lines
        if s.startswith(">"):
            flush_para(); flush_verse()
            seg=re.sub(r'^>\s?','',line)
            if quote and seg.startswith('　'):   # new quote paragraph
                quote.append('\x00')
            quote.append(seg)
            continue
        else:
            flush_quote()
        # blank
        if not s:
            # blank doesn't force para break by itself (handled by sentence-end rule),
            # but if current para ends a sentence, close it.
            if para and "".join(para).rstrip().endswith(SENT_END):
                flush_para()
            if verse: flush_verse()
            continue
        # bibliography entries
        if in_bib:
            flush_para()
            item=re.sub(r'^[-*・]\s*','',line).strip()
            if item in ('洋書','和書','邦書','雑誌','特集等','特集','レコード'):
                cur.append(f"\\bibsubhead{{{esc(item)}}}"); cur.append("")
            elif item:
                cur.append(f"\\bibentry{{{esc(item)}}}")
            continue
        # verse / chord / label lines
        if is_verse(line):
            flush_para(); flush_quote()
            verse.append(line)
            continue
        else:
            flush_verse()
        # normal text line
        if line.startswith('　') or line.startswith(' '):
            flush_para(); para.append(s)
        else:
            if para and not "".join(para).rstrip().endswith(SENT_END):
                para.append(s)            # continuation
            else:
                flush_para(); para.append(s)  # new paragraph (prev ended a sentence)
    flush_all()

    with open(OUT+"body_ja.tex","w",encoding="utf-8") as f:
        f.write("\n".join(body)+"\n")
    with open(OUT+"bib_ja.tex","w",encoding="utf-8") as f:
        f.write("\n".join(bib)+"\n")
    print("body lines:",len(body),"bib lines:",len(bib))

convert()
