"""Extract a zip safely: sanitize names, block path traversal, recurse into nested zips.

Usage: python tools/safe_unzip.py <zip> <dest_dir> [skip_ext,skip_ext,...]
"""
import os, re, sys, zipfile
SKIP = set(sys.argv[3].lower().split(",")) if len(sys.argv) > 3 else set()

def clean(part):
    part = part.replace("\x00", "")
    part = re.sub(r'[<>:"\\|?*\x00-\x1f]', "_", part).strip()
    if len(part.encode()) > 150:  # macOS limit is 255 bytes per name; keep extension
        stem, ext = os.path.splitext(part)
        part = stem.encode()[:140].decode("utf-8", "ignore").rstrip() + "~" + ext[:9]
    return part if part not in ("", ".", "..") else "_"

def extract(zpath, dest):
    n = 0
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            name = info.filename
            if not (info.flag_bits & 0x800):  # not flagged UTF-8: try cp437->utf8 repair
                try: name = name.encode("cp437").decode("utf-8")
                except (UnicodeEncodeError, UnicodeDecodeError): pass
            parts = [clean(p) for p in name.split("/") if p]
            if not parts: continue
            out = os.path.join(dest, *parts)
            if not os.path.realpath(out).startswith(os.path.realpath(dest) + os.sep):
                continue
            if os.path.splitext(name)[1].lower().lstrip(".") in SKIP:
                continue
            if name.endswith("/"):
                os.makedirs(out, exist_ok=True); continue
            try:
                os.makedirs(os.path.dirname(out), exist_ok=True)
                with z.open(info) as src, open(out, "wb") as dst:
                    dst.write(src.read())
            except OSError as e:
                print("SKIPPED", name, e, file=sys.stderr); continue
            n += 1
            if out.lower().endswith(".zip"):
                n += extract(out, out + ".extracted")
    return n

print(extract(sys.argv[1], os.path.realpath(sys.argv[2])), "files extracted")
