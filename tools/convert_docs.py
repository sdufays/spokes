"""Convert office/PDF/text files under a source dir into markdown text in a mirror dir.

Usage: python tools/convert_docs.py <src_dir> <out_dir>
Writes <out_dir>/<same relative path>.md for docx/xlsx/pptx/pdf/txt/tex/csv files,
and <out_dir>/_inventory.tsv listing every file (path, ext, size, converted?).
"""
import os, sys, traceback
src, out = os.path.realpath(sys.argv[1]), os.path.realpath(sys.argv[2])
SKIP_DIRS = {"__MACOSX"}

def docx_text(p):
    import docx
    d = docx.Document(p); lines = [para.text for para in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            lines.append(" | ".join(c.text.strip().replace("\n", " ") for c in row.cells))
    return "\n".join(lines)

def xlsx_text(p):
    import openpyxl
    wb = openpyxl.load_workbook(p, data_only=True, read_only=True); parts = []
    for ws in wb.worksheets:
        parts.append(f"## Sheet: {ws.title}")
        for row in ws.iter_rows(values_only=True):
            if any(v not in (None, "") for v in row):
                parts.append(" | ".join("" if v is None else str(v) for v in row))
    return "\n".join(parts)

def pptx_text(p):
    from pptx import Presentation
    parts = []
    for i, s in enumerate(Presentation(p).slides, 1):
        parts.append(f"## Slide {i}")
        for sh in s.shapes:
            if sh.has_text_frame: parts.append(sh.text_frame.text)
    return "\n".join(parts)

def pdf_text(p):
    from pypdf import PdfReader
    return "\n\n".join((pg.extract_text() or "") for pg in PdfReader(p).pages)

CONV = {".docx": docx_text, ".xlsx": xlsx_text, ".pptx": pptx_text, ".pdf": pdf_text}
inv = []
for root, dirs, files in os.walk(src):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for f in files:
        if f == ".DS_Store": continue
        p = os.path.join(root, f); rel = os.path.relpath(p, src)
        ext = os.path.splitext(f)[1].lower(); size = os.path.getsize(p); ok = ""
        try:
            if ext in CONV: text = CONV[ext](p)
            elif ext in (".txt", ".tex", ".csv", ".md"): text = open(p, errors="replace").read()
            else: text = None
            if text is not None:
                o = os.path.join(out, rel + ".md"); os.makedirs(os.path.dirname(o), exist_ok=True)
                with open(o, "w") as fh: fh.write(f"<!-- source: {rel} -->\n{text}\n")
                ok = "yes" if text.strip() else "empty"
        except Exception as e:
            ok = "error: " + str(e)[:80]
        inv.append(f"{rel}\t{ext}\t{size}\t{ok}")
os.makedirs(out, exist_ok=True)
open(os.path.join(out, "_inventory.tsv"), "w").write("path\text\tbytes\tconverted\n" + "\n".join(sorted(inv)) + "\n")
print(len(inv), "files inventoried;", sum(1 for l in inv if l.endswith("\tyes")), "converted")
