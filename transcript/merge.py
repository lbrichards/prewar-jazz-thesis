#!/usr/bin/env python3
"""Merge the per-chunk transcripts into one page-ordered markdown (pages 1..67).
Odd pages come from the clean *_R-based part files; even pages from the de-clipped even_* files."""
import re, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# page -> source file (authoritative, un-clipped)
SRC = {}
for p in [1,3,5,7,9,11]:            SRC[p] = "part1_sheets01-07.md"
for p in [13,15,17,19,21,23]:       SRC[p] = "part2_sheets08-13.md"
for p in [25,27,29,31,33,35]:       SRC[p] = "part3_sheets14-19.md"
for p in [37,39,41,43,45,47]:       SRC[p] = "part4_sheets20-25.md"
for p in [49,51,53,55,57]:          SRC[p] = "part5_sheets26-30.md"
for p in [59,61,63,65,67]:          SRC[p] = "part6_sheets31-35.md"
for p in [2,4,6,8,10,12,14,16,18,20,22]:   SRC[p] = "even_A.md"
for p in [24,26,28,30,32,34,36,38,40,42,44]: SRC[p] = "even_B.md"
for p in [46,48,50,52,54,56,58,60,62,64,66]: SRC[p] = "even_C.md"

PAGE_RE = re.compile(r'^##\s*p\.(\d+)\s*$')

def parse_pages(fn):
    """Return {pagenum: [lines]} using '## p.N' delimiters."""
    pages, cur = {}, None
    with open(fn, encoding="utf-8") as f:
        for line in f:
            m = PAGE_RE.match(line.rstrip())
            if m:
                cur = int(m.group(1)); pages[cur] = []
            elif cur is not None:
                pages[cur].append(line.rstrip("\n"))
    return pages

cache = {}
def get_page(p):
    fn = SRC[p]
    if fn not in cache:
        cache[fn] = parse_pages(fn) if os.path.exists(fn) else {}
    return cache[fn].get(p)

out = []
missing = []
for p in range(1, 68):
    body = get_page(p)
    if body is None:
        missing.append(p); continue
    out.append(f"\n<!-- ===== page {p} ({SRC[p]}) ===== -->")
    # strip trailing blank lines
    while body and not body[-1].strip():
        body.pop()
    out.append("\n".join(body))

with open("merged_ja.md", "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print("Wrote merged_ja.md ; pages:", 67-len(missing), "; missing:", missing)
