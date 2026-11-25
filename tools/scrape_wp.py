"""Scrape WordPress.com-hosted Spokes blogs into markdown files with YAML frontmatter.

Usage: python tools/scrape_wp.py <site> <out_root>
Writes <out_root>/<year>/<YYYY-MM-DD>_<slug>.md (skips files that already exist).
"""
import json, os, re, sys, time
import html2text, requests

site, out_root = sys.argv[1], sys.argv[2]
API = f"https://public-api.wordpress.com/rest/v1.1/sites/{site}/posts"
h = html2text.HTML2Text(); h.body_width = 0; h.ignore_images = False

def day_num(title):
    m = re.search(r"\bday\s*#?\s*(\d+)", title, re.I)
    return int(m.group(1)) if m else None

page, n_new, n_total = 1, 0, 0
while True:
    r = requests.get(API, params={"number": 100, "page": page, "order": "ASC",
                                  "fields": "ID,date,title,URL,content,categories,tags,author,slug"}, timeout=60)
    posts = r.json().get("posts", [])
    if not posts:
        break
    for p in posts:
        n_total += 1
        date = p["date"][:10]; year = date[:4]
        title = html2text.html2text(p["title"]).strip()
        slug = p["slug"][:80]
        path = os.path.join(out_root, year, f"{date}_{slug}.md")
        if os.path.exists(path):
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        body = h.handle(p["content"]).strip()
        meta = {
            "title": title, "date": date, "year": int(year), "day": day_num(title),
            "author": (p.get("author") or {}).get("name"),
            "categories": sorted((p.get("categories") or {}).keys()),
            "wp_tags": sorted((p.get("tags") or {}).keys()),
            "source": p["URL"], "site": site,
        }
        with open(path, "w") as f:
            f.write("---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in meta.items()) + "\n---\n\n")
            f.write(f"# {title}\n\n{body}\n")
        n_new += 1
    page += 1; time.sleep(0.5)
print(f"{site}: {n_total} posts seen, {n_new} written")
