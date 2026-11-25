#!/usr/bin/env python3
"""Search the Spokes knowledge base. Newest years first.

Examples:
  tools/find.py warmshowers                      # any file mentioning warmshowers
  tools/find.py "giving tuesday" --year 2025     # only 2025 material
  tools/find.py --tag sponsorship --kind doc     # all sponsorship docs, no keyword
  tools/find.py dog --kind blog --since 2024     # blog posts about dogs from 2024 on
  tools/find.py trek --contacts                  # search the contacts list
Options: --year Y | --since Y | --tag T | --kind blog|doc|email|theme | --contacts | -n N (max results)
"""
import argparse, csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("query", nargs="*")
ap.add_argument("--year", type=int); ap.add_argument("--since", type=int)
ap.add_argument("--tag"); ap.add_argument("--kind"); ap.add_argument("--contacts", action="store_true")
ap.add_argument("-n", type=int, default=40)
a = ap.parse_args()
q = " ".join(a.query).strip()
rx = re.compile(re.escape(q), re.I) if q else None

if a.contacts:
    for r in csv.DictReader(open(os.path.join(ROOT, "contacts/contacts.csv"))):
        line = " | ".join(r.values())
        if (not rx or rx.search(line)) and (not a.year or str(a.year) in r["years"]):
            print(f"{r['name']} | {r['organization']} | {r['category']} | {r['email']} | {r['phone']} | {r['city_state']} | {r['years']} | {r['outcome']}")
    sys.exit()

rows = list(csv.DictReader(open(os.path.join(ROOT, "catalog.csv"))))
for d, kind in (("themes", "theme"), ("email", "email")):
    for root, _, files in os.walk(os.path.join(ROOT, d)):
        for f in files:
            if f.endswith(".md") and f != "README.md":
                p = os.path.relpath(os.path.join(root, f), ROOT)
                y = re.search(r"(20\d\d)", p)
                rows.append({"kind": kind, "year": y.group(1) if y else "", "title": f[:-3], "tags": "", "path": p, "summary": "", "relevance": ""})
hits = []
for r in rows:
    y = int(r["year"] or 0)
    if a.kind and r["kind"] != a.kind: continue
    if a.year and y != a.year: continue
    if a.since and y < a.since: continue
    if a.tag and a.tag not in r["tags"].split(";"): continue
    snippet = ""
    if rx:
        try: text = open(os.path.join(ROOT, r["path"]), errors="replace").read()
        except OSError: continue
        m = rx.search(text)
        if not m: continue
        s = max(0, m.start() - 90); snippet = re.sub(r"\s+", " ", text[s:m.end() + 90])
    hits.append((y, r, snippet))
hits.sort(key=lambda h: (-h[0], {"high": 0, "medium": 1}.get(h[1]["relevance"], 2)))
for y, r, snip in hits[:a.n]:
    print(f"[{r['year'] or '----'}] {r['kind']:5} {r['title'][:70]}\n        {r['path']}" + (f"\n        …{snip}…" if snip else ""))
print(f"\n{len(hits)} matches" + (f" (showing {a.n})" if len(hits) > a.n else ""))
