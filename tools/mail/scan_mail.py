"""Find every Apple Mail message mentioning Spokes and export it as readable markdown.

Usage: python tools/mail/scan_mail.py <mail_root> <out_dir> [--since-days N]
  mail_root: e.g. ~/Library/Mail/V10   (needs Full Disk Access)
  out_dir:   e.g. ~/spokes_sources/mail  -> writes messages/<date>_<hash>.md,
             attachments/<hash>/<file>, and _seen.txt (message-ids already exported)
Also accepts loose .eml files dropped in <out_dir>/../mail-inbox (from the Mail rule).
"""
import email, email.policy, hashlib, os, re, sys, time
from email.utils import parsedate_to_datetime

mail_root, out_dir = os.path.expanduser(sys.argv[1]), os.path.expanduser(sys.argv[2])
since_days = None
if "--since-days" in sys.argv:
    since_days = float(sys.argv[sys.argv.index("--since-days") + 1])
PAT = re.compile(rb"spokes", re.I)
WORD = re.compile(r"\b(mit\s*)?spokes\b|mitspokes", re.I)
SAVE_EXT = {".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv", ".pptx", ".txt", ".png", ".jpg", ".jpeg", ".gpx"}
os.makedirs(os.path.join(out_dir, "messages"), exist_ok=True)
seen_path = os.path.join(out_dir, "_seen.txt")
seen = set(open(seen_path).read().split("\n")) if os.path.exists(seen_path) else set()

def read_raw(path):
    data = open(path, "rb").read()
    if path.endswith(".emlx"):
        nl = data.find(b"\n")
        try:
            n = int(data[:nl].strip()); data = data[nl + 1: nl + 1 + n]
        except ValueError:
            pass
    return data

def text_of(msg):
    parts = []
    for part in msg.walk():
        if part.is_multipart() or part.get_filename():
            continue
        ct = part.get_content_type()
        if ct in ("text/plain", "text/html"):
            try:
                t = part.get_content()
            except Exception:
                t = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
            if ct == "text/html":
                t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
                t = re.sub(r"(?s)<br\s*/?>|</p>|</div>|</tr>", "\n", t)
                t = re.sub(r"(?s)<[^>]+>", "", t)
                t = re.sub(r"&nbsp;", " ", t); t = re.sub(r"&amp;", "&", t)
            parts.append((ct, t))
    plain = [t for ct, t in parts if ct == "text/plain"]
    return "\n\n".join(plain) if plain else "\n\n".join(t for _, t in parts)

def candidates():
    cutoff = time.time() - since_days * 86400 if since_days else 0
    for root, dirs, files in os.walk(mail_root):
        for f in files:
            if f.endswith(".emlx"):
                p = os.path.join(root, f)
                try:
                    if cutoff and os.path.getmtime(p) < cutoff: continue
                except OSError:
                    continue
                yield p
    inbox = os.path.join(os.path.dirname(out_dir.rstrip("/")), "mail-inbox")
    if os.path.isdir(inbox):
        for f in os.listdir(inbox):
            if f.endswith(".eml"): yield os.path.join(inbox, f)

scanned = found = 0
for p in candidates():
    scanned += 1
    try:
        raw = read_raw(p)
    except OSError:
        continue
    b64 = b"base64" in raw[:200000].lower()
    if not PAT.search(raw) and not b64:
        continue
    try:
        msg = email.message_from_bytes(raw, policy=email.policy.default)
    except Exception:
        continue
    mid = str(msg.get("Message-ID", "")).strip() or hashlib.sha1(raw[:5000]).hexdigest()
    if mid in seen:
        continue
    subj, frm = str(msg.get("Subject", "")), str(msg.get("From", ""))
    to, cc = str(msg.get("To", "")), str(msg.get("Cc", ""))
    try:
        body = text_of(msg)
    except Exception:
        body = ""
    if not WORD.search(" ".join([subj, frm, to, cc, body])):
        continue
    try:
        dt = parsedate_to_datetime(msg.get("Date")); date = dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        date = "0000-00-00 00:00"
    h = hashlib.sha1(mid.encode()).hexdigest()[:12]
    atts = []
    for part in msg.walk():
        fn = part.get_filename()
        if not fn: continue
        atts.append(fn)
        if os.path.splitext(fn)[1].lower() in SAVE_EXT:
            payload = part.get_payload(decode=True)
            if payload and len(payload) < 15_000_000:
                d = os.path.join(out_dir, "attachments", h); os.makedirs(d, exist_ok=True)
                safe = re.sub(r"[^\w.\- ]+", "_", fn)[:120]
                open(os.path.join(d, safe), "wb").write(payload)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    with open(os.path.join(out_dir, "messages", f"{date[:10]}_{h}.md"), "w") as fh:
        fh.write(f"---\nsubject: {subj!r}\nfrom: {frm!r}\nto: {to!r}\ncc: {cc!r}\ndate: '{date}'\n"
                 f"message_id: {mid!r}\nattachments: {atts!r}\n---\n\n{body[:60000]}\n")
    seen.add(mid); found += 1
open(seen_path, "w").write("\n".join(sorted(s for s in seen if s)))
print(f"scanned {scanned} messages, exported {found} new Spokes emails -> {out_dir}")
