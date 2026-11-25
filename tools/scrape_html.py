"""Scrape blog posts from plain HTML pages (Wix sites, Wayback Machine snapshots of Tumblr/Wix).

Usage: python tools/scrape_html.py <year> <url_list_file> <out_root>
url_list_file: one URL per line, optionally "<wayback_timestamp> <original_url>" (CDX format).
Writes <out_root>/<year>/<date>_<slug>.md
"""
import json, os, re, sys, time
from urllib.parse import urlparse
import html2text, requests
from bs4 import BeautifulSoup

year, list_file, out_root = sys.argv[1], sys.argv[2], sys.argv[3]
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) spokes-archiver"}
h = html2text.HTML2Text(); h.body_width = 0

def fetch(url):
    for attempt in range(4):
        try:
            r = requests.get(url, headers=UA, timeout=60)
            if r.status_code == 200 and "Temporarily Offline" not in r.text[:3000]:
                return r.text
        except requests.RequestException:
            pass
        time.sleep(5 * (attempt + 1))
    return None

def extract(html):
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "noscript", "nav", "footer", "header", "iframe", "form"]):
        t.decompose()
    title = None
    og = soup.find("meta", property="og:title")
    if og and og.get("content"): title = og["content"]
    elif soup.title: title = soup.title.get_text()
    title = re.sub(r"\s*[|\-–]\s*(Spokes.*|Tumblr|MIT Spokes.*)$", "", (title or "").strip())
    date = None
    for prop in ("article:published_time", "datePublished"):
        m = soup.find("meta", property=prop) or soup.find("meta", itemprop=prop)
        if m and m.get("content"): date = m["content"][:10]; break
    if not date:
        m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
        if m: date = m.group(1)
    node = None
    for sel in ['[data-hook="post-description"]', "article", ".post-content", ".entry-content", ".post", "main"]:
        cands = soup.select(sel)
        if cands:
            node = max(cands, key=lambda n: len(n.get_text())); break
    node = node or soup.body or soup
    body = h.handle(str(node)).strip()
    return title, date, body

def day_num(title):
    m = re.search(r"\bday\s*#?\s*(\d+)", title or "", re.I)
    return int(m.group(1)) if m else None

n = 0
for line in open(list_file):
    parts = line.split()
    if not parts: continue
    if len(parts) == 2:
        ts, orig = parts
        url = f"https://web.archive.org/web/{ts}id_/{orig}"
    else:
        ts, orig = None, parts[0]; url = orig
    slug = re.sub(r"[^a-z0-9-]+", "-", urlparse(orig).path.rstrip("/").split("/")[-1].lower())[:80] or "post"
    html = fetch(url)
    if not html:
        print("FAILED", orig, file=sys.stderr); continue
    title, date, body = extract(html)
    if len(body) < 200:
        print("EMPTY", orig, file=sys.stderr); continue
    real_date = date
    date = date or (f"{ts[:4]}-{ts[4:6]}-{ts[6:8]}" if ts else f"{year}-00-00")
    y = real_date[:4] if real_date else year
    path = os.path.join(out_root, y, f"{date}_{slug}.md")
    if os.path.exists(path): continue
    os.makedirs(os.path.dirname(path), exist_ok=True)
    meta = {"title": title, "date": date, "year": int(y), "day": day_num(title),
            "source": orig, "archived_copy": url if ts else None,
            "date_is_estimate": not real_date}
    with open(path, "w") as f:
        f.write("---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in meta.items()) + "\n---\n\n")
        f.write(f"# {title}\n\n{body}\n")
    n += 1
    time.sleep(1.5 if ts else 0.5)
print(f"{year}: wrote {n}")
