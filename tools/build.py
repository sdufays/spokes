"""Assemble the Spokes knowledge base from raw/ into the browsable repo layout.

Usage: python tools/build.py        (run from repo root; idempotent, regenerates outputs)

Inputs (raw/, not committed):
  raw/blogs/<year>/*.md            scraped posts
  raw/blog_tags/*.jsonl            per-post tags/extraction from the blog agents
  raw/drive/<label>/**.md          kept Drive docs (+ _contacts.csv, _highlights.md, _images_keep.csv)
  raw/email/**                     email digests (optional)
Outputs:
  blogs/<year>/*.md, blogs/README.md, blogs/by-place/*.md, blogs/by-tag/*.md
  docs/<label>/**.md, docs/README.md
  contacts/contacts.csv, contacts/README.md, contacts/<category>.md
  years/<year>/README.md
  catalog.csv   (one row per blog post / doc: kind, year, title, tags, relevance, summary, path)
"""
import csv, glob, json, os, re, shutil
from collections import defaultdict
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
REL = {"high": 0, "medium": 1, "low": 2}

def fix(o):
    """Repair surrogate-pair escapes (emoji) left by JSON/YAML round-trips."""
    if isinstance(o, str):
        try: return o.encode("utf-16", "surrogatepass").decode("utf-16")
        except UnicodeError: return o.encode("utf-8", "replace").decode("utf-8")
    if isinstance(o, list): return [fix(x) for x in o]
    if isinstance(o, dict): return {k: fix(v) for k, v in o.items()}
    return o

def split_fm(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m: return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
        if not isinstance(fm, dict): fm = {}
        fm = fix(fm)
    except yaml.YAMLError:
        fm = {}
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if k.strip() and v.strip(): fm[k.strip()] = v.strip().strip('"\'')
    return fm, m.group(2)

def dump_fm(fm):
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n"

def as_list(v):
    if v is None: return []
    if isinstance(v, list): return [str(x) for x in v]
    return [t.strip() for t in str(v).strip("[]").split(",") if t.strip()]

def year_of(v, default=None):
    m = re.search(r"(19|20)\d\d", str(v or ""))
    return int(m.group(0)) if m else default

def md_cell(s):
    return str(s or "").replace("|", "/").replace("\n", " ").strip()

def reset(d):
    if os.path.isdir(d): shutil.rmtree(d)
    os.makedirs(d)

catalog = []

# ---------------------------------------------------------------- blogs
tags_by_path = {}
for f in glob.glob("raw/blog_tags/*.jsonl"):
    for line in open(f):
        line = line.strip()
        if not line: continue
        try: rec = fix(json.loads(line))
        except json.JSONDecodeError: continue
        tags_by_path[os.path.basename(rec.get("path", ""))] = rec

reset("blogs")
posts = []
for src in sorted(glob.glob("raw/blogs/*/*.md")):
    fm, body = split_fm(open(src).read())
    t = tags_by_path.get(os.path.basename(src), {})
    year = int(fm.get("year") or src.split("/")[2])
    fm.update({k: t.get(k) for k in ("summary", "tags", "from", "to", "miles", "elevation_ft", "slept_at",
                                     "learning_festival", "contacts", "planning_notes", "relevance") if k in t})
    fm["year"] = year
    glance = []
    if t:
        route = " → ".join(x for x in (t.get("from"), t.get("to")) if x)
        bits = [b for b in (route, f"{t['miles']} mi" if t.get("miles") else "",
                            f"{t['elevation_ft']} ft climbing" if t.get("elevation_ft") else "") if b]
        glance.append(f"> **{year}** · {fm.get('date','')}" + (f" · {' · '.join(bits)}" if bits else ""))
        if t.get("summary"): glance.append(f"> {t['summary']}")
        if t.get("slept_at"): glance.append(f"> 🏠 **Slept:** {t['slept_at']}")
        if t.get("learning_festival"): glance.append(f"> 🧪 **Learning festival:** {t['learning_festival']}")
        for n in t.get("planning_notes") or []: glance.append(f"> - 📌 {n}")
        if t.get("tags"): glance.append(f"> Tags: {', '.join(t['tags'])}")
    dst = os.path.join("blogs", str(year), os.path.basename(src))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    body = body.lstrip()
    title_line, _, rest = body.partition("\n")
    with open(dst, "w") as fh:
        fh.write(dump_fm(fm) + "\n" + title_line + "\n\n" + ("\n".join(glance) + "\n\n" if glance else "") + rest.lstrip())
    p = dict(fm, path=dst)
    posts.append(p)
    catalog.append({"kind": "blog", "year": year, "date": fm.get("date", ""), "title": fm.get("title", ""),
                    "tags": ";".join(as_list(fm.get("tags"))), "relevance": fm.get("relevance", ""),
                    "summary": fm.get("summary", ""), "path": dst})

def post_line(p, prefix="../"):
    route = " → ".join(x for x in (p.get("from"), p.get("to")) if x)
    return f"[{md_cell(p.get('title'))}]({prefix}{p['path'][len('blogs/'):]})" + (f" — {route}" if route else "")

years = sorted({p["year"] for p in posts}, reverse=True)
with open("blogs/README.md", "w") as fh:
    fh.write("# Spokes daily blogs — all years\n\nNewest year first. Each post starts with an **at-a-glance box** "
             "(route, miles, where they slept, learning festival, 📌 planning notes).\n\n"
             "- **By state:** [blogs/by-place/](by-place/) — every road/host/hazard note for a state, city or park, newest year first\n"
             "- **By tag:** [blogs/by-tag/](by-tag/)\n\n")
    for y in years:
        ps = sorted([p for p in posts if p["year"] == y], key=lambda p: str(p.get("date")))
        fh.write(f"## {y} ({len(ps)} posts)\n\n| Date | Day | Post | Miles | Relevance | Tags |\n|---|---|---|---|---|---|\n")
        for p in ps:
            tags = [t for t in as_list(p.get("tags")) if not t.startswith("place:")][:6]
            fh.write(f"| {p.get('date','')} | {p.get('day') or ''} | {post_line(p, '')} | {p.get('miles') or ''} | "
                     f"{p.get('relevance','')} | {', '.join(tags)} |\n")
        fh.write("\n")

by_tag, by_state = defaultdict(list), defaultdict(list)
for p in posts:
    for t in as_list(p.get("tags")):
        (by_state[t[6:]] if t.startswith("place:") else by_tag[t]).append(p)
for folder, groups, kind in (("by-tag", by_tag, "tag"), ("by-place", by_state, "place")):
    os.makedirs(f"blogs/{folder}", exist_ok=True)
    for key, ps in sorted(groups.items()):
        safe = re.sub(r"[^a-z0-9-]+", "-", key.lower()).strip("-") or "other"
        ps = sorted(ps, key=lambda p: (-p["year"], str(p.get("date"))))
        with open(f"blogs/{folder}/{safe}.md", "w") as fh:
            fh.write(f"# Blogs — {kind}: {key}\n\n{len(ps)} posts, newest year first.\n\n")
            cur = None
            for p in ps:
                if p["year"] != cur:
                    cur = p["year"]; fh.write(f"\n## {cur}\n\n")
                fh.write(f"### {p.get('date','')} — {post_line(p, '../')}\n")
                if p.get("summary"): fh.write(f"{p['summary']}\n")
                if p.get("slept_at"): fh.write(f"- 🏠 Slept: {p['slept_at']}\n")
                for n in p.get("planning_notes") or []: fh.write(f"- 📌 {n} *({p['year']})*\n")
                fh.write("\n")

# ---------------------------------------------------------------- docs
reset("docs")
docs = []
for src in sorted(glob.glob("raw/drive/**/*.md", recursive=True)):
    rel = os.path.relpath(src, "raw/drive")
    parts = rel.split(os.sep)
    if any(x.startswith("_") for x in parts): continue
    if re.search(r"/blogs?/", rel) and re.match(r"\d{4}_day-?\d", parts[-1]): continue  # dup of blogs/
    fm, body = split_fm(open(src).read())
    label = parts[0]
    year = year_of(fm.get("year"), year_of(label, 0))
    dst = os.path.join("docs", rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    d = {"year": year, "label": label, "title": fm.get("title") or os.path.basename(src)[:-3],
         "relevance": str(fm.get("relevance") or "").lower(), "tags": as_list(fm.get("tags")),
         "summary": fm.get("summary", ""), "path": dst, "link": fm.get("drive_link", "")}
    docs.append(d)
    catalog.append({"kind": "doc", "year": year, "date": fm.get("modified", ""), "title": d["title"],
                    "tags": ";".join(d["tags"]), "relevance": d["relevance"], "summary": d["summary"], "path": dst})

with open("docs/README.md", "w") as fh:
    fh.write("# Spokes documents (from the shared Drive)\n\nCleaned copies of every useful Drive file, newest year "
             "first. ★ = high relevance. Each file has frontmatter with year, tags, summary and the original Drive link.\n\n")
    for label in sorted({d["label"] for d in docs}, key=lambda l: (-(year_of(l, 9999)), l)):
        ds = sorted([d for d in docs if d["label"] == label], key=lambda d: (REL.get(d["relevance"], 3), d["path"]))
        fh.write(f"## {label} ({len(ds)} docs)\n\n| | Doc | Year | Tags | Summary |\n|---|---|---|---|---|\n")
        for d in ds:
            star = "★" if d["relevance"] == "high" else ""
            fh.write(f"| {star} | [{md_cell(d['title'])}]({d['path'][5:]}) | {d['year']} | {', '.join(d['tags'][:5])} | {md_cell(d['summary'])[:220]} |\n")
        fh.write("\n")

# ---------------------------------------------------------------- email
reset("email")
emails = []
for src in sorted(glob.glob("raw/email/**/*.md", recursive=True)):
    if os.path.basename(src).startswith("_"): continue
    fm, body = split_fm(open(src).read())
    dst = os.path.join("email", os.path.relpath(src, "raw/email"))
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)
    e = {"year": year_of(fm.get("year"), 0), "date": fm.get("date", ""), "title": fm.get("title", ""),
         "tags": as_list(fm.get("tags")), "relevance": str(fm.get("relevance") or ""), "summary": fm.get("summary", ""), "path": dst}
    emails.append(e)
    catalog.append({"kind": "email", "year": e["year"], "date": e["date"], "title": e["title"], "tags": ";".join(e["tags"]),
                    "relevance": e["relevance"], "summary": e["summary"], "path": dst})
if emails:
    with open("email/README.md", "w") as fh:
        fh.write("# Spokes emails\n\nThreads from Sarah's MIT mailbox that mention Spokes, newest first. Updated daily by the mail job.\n\n"
                 "| Date | Year | Thread | Summary |\n|---|---|---|---|\n")
        for e in sorted(emails, key=lambda e: str(e["date"]), reverse=True):
            fh.write(f"| {e['date']} | {e['year']} | [{md_cell(e['title'])}]({e['path'][6:]}) | {md_cell(e['summary'])[:200]} |\n")

# ---------------------------------------------------------------- contacts
FIELDS = ["name", "organization", "category", "role_or_notes", "email", "phone", "city_state", "years",
          "outcome", "sources"]
merged = {}
def add_contact(row, year, source):
    name, email = (row.get("name") or "").strip(), (row.get("email") or "").strip().lower()
    org = (row.get("organization") or "").strip()
    if not (name or org or email): return
    key = email or (name.lower() + "|" + org.lower())
    c = merged.setdefault(key, {k: "" for k in FIELDS} | {"_years": set(), "_sources": [], "_outcomes": []})
    for k in ("name", "organization", "category", "role_or_notes", "email", "phone", "city_state"):
        v = (row.get(k) or "").strip()
        if v and (not c[k] or (k == "role_or_notes" and v not in c[k] and len(c[k]) < 300)):
            c[k] = v if not c[k] else c[k] + "; " + v
    if year: c["_years"].add(year)
    o = (row.get("outcome") or "").strip()
    if o and o not in c["_outcomes"]: c["_outcomes"].append(f"{o} ({year})" if year else o)
    if source and source not in c["_sources"]: c["_sources"].append(source)

for f in glob.glob("raw/**/_contacts*.csv", recursive=True):
    if "/_parts/" in f or "/_work/" in f: continue
    label = f.split("/")[2]
    for row in csv.DictReader(open(f, newline="", errors="replace")):
        add_contact(row, year_of(row.get("year"), year_of(label)), (row.get("source_file") or "").strip()
                    + (f" <{row['source_link'].strip()}>" if (row.get("source_link") or "").strip() else ""))
for p in posts:
    for c in p.get("contacts") or []:
        add_contact({"name": c, "category": "mentioned-in-blog"}, p["year"], p["path"])

reset("contacts")
rows = []
for c in merged.values():
    c["years"] = ", ".join(str(y) for y in sorted(c["_years"], reverse=True))
    c["outcome"] = "; ".join(c["_outcomes"])
    c["sources"] = "; ".join(c["_sources"][:6])
    c["_latest"] = max(c["_years"]) if c["_years"] else 0
    c["category"] = (c["category"] or "other").split(";")[0].strip().lower()
    rows.append(c)
rows.sort(key=lambda c: (c["category"], -c["_latest"], c["name"].lower()))
with open("contacts/contacts.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
cats = defaultdict(list)
for c in rows: cats[c["category"]].append(c)
with open("contacts/README.md", "w") as fh:
    fh.write(f"# Spokes contacts — {len(rows)} people & organizations\n\nMerged from every Drive contact list, sponsor/"
             "host/LF tracker, email and blog. Deduplicated by email (else name+org). Most recent year first within "
             "each category. Full data: [contacts.csv](contacts.csv) (open in Sheets/Excel and filter).\n\n")
    for cat, cs in sorted(cats.items(), key=lambda kv: -len(kv[1])):
        fh.write(f"- [{cat}]({re.sub(r'[^a-z0-9-]+', '-', cat)}.md) — {len(cs)}\n")
for cat, cs in cats.items():
    with open(f"contacts/{re.sub(r'[^a-z0-9-]+', '-', cat)}.md", "w") as fh:
        fh.write(f"# Contacts — {cat} ({len(cs)})\n\n| Name | Org | Role / notes | Email | Phone | Where | Years | Outcome |\n|---|---|---|---|---|---|---|---|\n")
        for c in cs:
            fh.write("| " + " | ".join(md_cell(c[k])[:200] for k in ("name", "organization", "role_or_notes", "email",
                                                                     "phone", "city_state", "years", "outcome")) + " |\n")

# ---------------------------------------------------------------- years
reset("years")
all_years = sorted({d["year"] for d in docs if d["year"]} | set(years), reverse=True)
for y in all_years:
    os.makedirs(f"years/{y}", exist_ok=True)
    with open(f"years/{y}/README.md", "w") as fh:
        fh.write(f"# Spokes {y}\n\n")
        for h in sorted(glob.glob(f"raw/drive/*/_highlights*.md")) + sorted(glob.glob("raw/email/_highlights*.md")):
            label = h.split("/")[2] if "/drive/" in h else "email"
            if label == "email":
                hl = [l for l in open(h).read().splitlines() if re.search(rf"\({y}\b", l)]
                if hl: fh.write("## Highlights (from email)\n\n" + "\n".join(hl) + "\n\n")
                continue
            if year_of(label) == y:
                fh.write(f"## Highlights (from Drive {label})\n\n" + split_fm(open(h).read())[1].strip() + "\n\n")
        ds = sorted([d for d in docs if d["year"] == y], key=lambda d: (REL.get(d["relevance"], 3), d["title"]))
        if ds:
            fh.write(f"## Documents ({len(ds)})\n\n")
            for d in ds:
                fh.write(f"- {'★ ' if d['relevance']=='high' else ''}[{md_cell(d['title'])}](../../{d['path']}) — {md_cell(d['summary'])[:160]}\n")
            fh.write("\n")
        ps = sorted([p for p in posts if p["year"] == y], key=lambda p: str(p.get("date")))
        if ps:
            fh.write(f"## Blog posts ({len(ps)})\n\n")
            for p in ps:
                fh.write(f"- {p.get('date','')} · {post_line(p, '../../blogs/')}" + (f" · {p['miles']} mi" if p.get("miles") else "") + "\n")

# ---------------------------------------------------------------- catalog
catalog.sort(key=lambda r: (-int(r["year"] or 0), r["kind"], str(r["date"])))
with open("catalog.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["kind", "year", "date", "title", "tags", "relevance", "summary", "path"])
    w.writeheader(); w.writerows(catalog)
print(f"blogs={len(posts)} docs={len(docs)} contacts={len(rows)} years={all_years}")

# ---------------------------------------------------------------- README (front page)
themes = [l.split("\t") for l in open("tools/themes.tsv").read().strip().splitlines()]
cov = defaultdict(lambda: {"blog": 0, "doc": 0, "email": 0})
for r in catalog: cov[int(r["year"] or 0)][r["kind"]] += 1
media_n = defaultdict(int)
for f in glob.glob("media/*/**/*.*", recursive=True): media_n[year_of(f.split("/")[1], 0)] += 1
with open("README.md", "w") as fh:
    fh.write(f"""# 🚲 MIT Spokes knowledge base

Everything a Spokes team needs to plan and ride the trip, consolidated from **every Spokes blog (2013–2026)**, the **shared Spokes Google Drive** (all year folders, Hub, Tanzania, Master Guides) and **Spokes email**. Junk was discarded; everything kept has its **year** attached. **Recent years first** everywhere.

## Start here
1. **[Themes](themes/)** — one file per topic with TL;DR, key numbers by year, playbook, timeline, what worked, contacts, templates:
""")
    for slug, desc, _ in themes:
        name = desc.split(" — ")[0]
        exists = os.path.exists(f"themes/{slug}.md")
        fh.write(f"   - [{name}](themes/{slug}.md)" + ("" if exists else " *(pending)*") + "\n")
    fh.write(f"""2. **[2027 working folder](2027/)** — this year's meeting notes and plans.
3. **[Contacts](contacts/)** — {len(rows)} people & orgs (sponsors, hosts, LF partners, MIT staff, alumni, bike shops…), with years and outcomes. Spreadsheet: [contacts.csv](contacts/contacts.csv).
4. **[Master guides](docs/master-guide/)** — the official how-to guides written by past teams (updated through 2026).

## Browse
| What | Where |
|---|---|
| Daily blogs, all years, each with an at-a-glance box (route, miles, where they slept, 📌 planning notes) | [blogs/](blogs/) |
| Road / host / hazard notes for a state, city or park | [blogs/by-place/](blogs/by-place/) |
| Blog posts by topic (dogs, weather, housing, mechanicals…) | [blogs/by-tag/](blogs/by-tag/) |
| Drive documents (budgets, trackers, guides, curricula, meeting notes) | [docs/](docs/) |
| One page per year: highlights, all docs, all posts | [years/](years/) |
| Spokes email threads | [email/](email/) |
| Photos, logos, flyers, maps worth keeping | [media/](media/) |
| Everything in one spreadsheet (filter by year/tag/kind) | [catalog.csv](catalog.csv) |

## Search
```bash
tools/find.py warmshowers                     # anything mentioning warmshowers, newest first
tools/find.py "giving tuesday" --year 2025    # only 2025
tools/find.py --tag sponsorship --kind doc    # all sponsorship documents
tools/find.py dog --kind blog --since 2024    # blog posts about dogs since 2024
tools/find.py trek --contacts                 # search contacts
```
(Uses the repo's `.venv`; or just use GitHub search / `grep -ri`.)

## Coverage
| Year | Blog posts | Drive docs | Emails | Media |
|---|---|---|---|---|
""")
    for y in sorted([y for y in cov if y], reverse=True):
        fh.write(f"| [{y}](years/{y}/) | {cov[y]['blog']} | {cov[y]['doc']} | {cov[y]['email']} | {media_n.get(y, 0)} |\n")
    fh.write("""
**Known gaps:** 2016, 2018, 2019 and 2023 blogs no longer exist online (sites deleted, never archived). No 2020–2021 material was found anywhere (likely no trip those years). The 2024 Drive folder was read through the connector only, so its long spreadsheets (fundraising tracker, budget log) are truncated — download "Spokes 2024" from Drive as a zip to complete them. Google Forms responses can't be exported by the connector. `2013/OrganizedContacts.xlsx` is password-protected.

## How it stays up to date
- **Email:** every morning at 8:00 a job on Sarah's Mac (`tools/mail/daily.sh`, launchd `com.sdufays.spokes-mail`) picks up new Spokes emails (saved by the Apple Mail rule "Spokes → archive"), files them under `email/`, adds contacts, adds dated bullets to the relevant theme's *Recent updates*, rebuilds and pushes.
- **Rebuild indexes after editing:** `.venv/bin/python tools/build.py`
- **Rewrite a theme:** `tools/run_themes.sh 03-fundraising`
- Raw scrapes/exports live in `raw/` and `~/spokes_sources/` (not committed).
""")
