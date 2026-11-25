#!/usr/bin/env python3
"""Build 2027/fundraising/2027_mit_department_outreach.xlsx from
raw/dept_research/*.csv (web research, one row per MIT unit) and
raw/dept_research/_history_*.csv (past asks/gifts from the Drive trackers).
Re-run any time; it overwrites the workbook."""
import csv, glob, os, re, sys
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(ROOT, "raw/dept_research")
OUT = os.path.join(ROOT, "2027/fundraising/2027_mit_department_outreach.xlsx")
TODAY = "2026-11-25"

def rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return [{(k or "").strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]

# ---------- canonical keys ----------
COURSE_NAMES = [
    (r"civil|environmental engineering|\bcee\b", "1"), (r"mechanical engineering|\bmeche\b", "2"),
    (r"materials science|\bdmse\b", "3"), (r"^architecture|department of architecture", "4"),
    (r"^chemistry|department of chemistry", "5"), (r"eecs|electrical engineering", "6"),
    (r"^biology|department of biology", "7"), (r"^physics|department of physics", "8"),
    (r"brain and cognitive|brain & cognitive|\bbcs\b", "9"), (r"chemical engineering", "10"),
    (r"urban studies|\bdusp\b", "11"), (r"earth, atmospheric|earth atmospheric|\beaps\b", "12"),
    (r"^economics|department of economics", "14"),
    (r"aeronautics|aero/?astro|aeroastro", "16"), (r"political science", "17"),
    (r"^mathematics|department of mathematics|^math\b", "18"), (r"biological engineering", "20"),
    (r"^history", "21H"), (r"^literature", "21L"), (r"music|theater arts", "21M"),
    (r"global languages", "21G"), (r"anthropology", "21A"), (r"nuclear science", "22"),
    (r"linguistics", "24"), (r"science, technology|science technology|\bsts\b", "STS"),
    (r"comparative media|\bcms\b", "CMS"),
]
DEPT_COURSES = {c for _, c in COURSE_NAMES}

def course_of(name, course):
    c = (course or "").upper().replace("COURSE", "").strip().split("/")[0].split(" ")[0].strip()
    c = re.sub(r"[^0-9A-Z-]", "", c)
    if c.endswith("-") or not c: c = ""
    if c and re.match(r"^\d+[A-Z]?$|^STS$|^CMS$", c):
        c = c if not re.match(r"^\d+-", c) else c.split("-")[0]
        if c in DEPT_COURSES: return c
    n = (name or "").lower().replace("mit ", "").strip()
    for rx, cc in COURSE_NAMES:
        if re.search(rx, n): return cc
    m = re.match(r"^(course\s*)?(\d{1,2}[a-z]?)\b", n)
    if m and m.group(2).upper() in DEPT_COURSES: return m.group(2).upper()
    return ""

ALIASES = {
    "mitnano": "mit.nano", "nano": "mit.nano", "libraries": "mit libraries", "museum": "mit museum",
    "edgerton": "edgerton center", "edgertoncenter": "edgerton center",
    "schoolofengineering": "school of engineering", "soe": "school of engineering",
    "deanofengineering": "school of engineering", "officeofthedeanofengineering": "school of engineering",
    "pkg": "pkg center", "pkgpublicservicecenter": "pkg center", "priscillakinggraypublicservicecenter": "pkg center",
    "climateconsortium": "climate & sustainability consortium", "mitclimatesustainabilityconsortium": "climate & sustainability consortium",
    "climatesustainabilityconsortium": "climate & sustainability consortium", "mcsc": "climate & sustainability consortium",
    "ome": "office of minority education", "officeofminorityeducation": "office of minority education",
    "jwel": "j-wel", "mitjwel": "j-wel", "abdullatifjameelworldeducationlab": "j-wel",
    "urop": "urop", "lincolnlab": "lincoln laboratory", "lincolnlaboratory": "lincoln laboratory",
    "mitlincolnlaboratory": "lincoln laboratory", "misti": "misti", "mitmisti": "misti",
}
def name_key(name):
    n = re.sub(r"\(.*?\)", "", (name or "").lower())
    n = re.sub(r"^(the |mit |massachusetts institute of technology )+", "", n.strip())
    n = re.sub(r"[^a-z0-9]", "", n.replace("&", "and"))
    for rx, canon in RX_ALIASES:
        if re.search(rx, n): return canon
    n = ALIASES.get(n, n)
    for rx, canon in RX_ALIASES:
        if re.search(rx, n): return canon
    return n

RX_ALIASES = [
    (r"^csail", "csail"), (r"^kochinstitute", "koch institute"), (r"^picowerinstitute", "picower institute"),
    (r"gordon.*engineeringleadership|^mitgel$|^gel$", "gordon engineering leadership (gel)"),
    (r"^jwel|^j-wel|worldeducationlab", "j-wel"), (r"kellydouglas", "kelly-douglas fund (shass)"),
    (r"^misti", "misti"), (r"^mites|officeofengineeringoutreachprograms|^oeop", "mites / oeop"),
    (r"minorityeducation|^oaces|officeofacademiccommunityempowerment", "oaces (formerly ome)"),
    (r"pk12", "pk-12 action group / open learning pk-12"),
    (r"^pkg|^priscillakinggray|^publicservicecenter|ideasdevelopmentgrant|globalideaschallenge", "pkg center"),
    (r"^schoolofhumanities|^shassdeansoffice", "shass dean's office"),
    (r"^schwarzmancollegeofcomputing|^sccstudent", "schwarzman college of computing"),
    (r"socialimpactelo|^officeofexperientiallearning", "office of experiential learning (elo)"),
    (r"studentactivitiesoffice|^saoadditional|^uafinancialboard|^undergraduateassociationfinancialboard|studentgroupfundingcouncil|^uacouncildiscretionary", "student group funding council (sgfc, formerly ua finboard/sao)"),
    (r"^departmentofathletics|^recreation$", "daper (athletics, pe & recreation)"),
    (r"councilforthearts|^camit", "council for the arts at mit (camit)"),
    (r"^sandbox", "sandbox innovation fund"), (r"^legatum", "legatum center"),
    (r"^departmentofundergraduateeducation|^officeofthevicechancellor", "vice chancellor / dean for undergraduate education"),
    (r"^concourse", "concourse"), (r"educationarcade|^schellerteacher|teachingsystemslab", "scheller teacher education program (step lab)"),
    (r"^integratedlearningneet|^neet", "neet"), (r"^edx$|^opencourseware|^openlearning$", "open learning"),
    (r"^officeofthepresident|^presidentreif", "office of the president"), (r"womeninmath", "undergraduate women in math"),
    (r"^urop", "urop"), (r"swecubator|societyofwomenengineers", "society of women engineers (swecubator)"),
    (r"bakerfoundation|bakermemorial", "baker foundation"), (r"^taubetapi", "tau beta pi fellowship"),
    (r"graduatestudentexperience|^officeofgraduateeducation", "office of graduate education"),
    (r"^act$|^artcultureandtechnology", "art, culture and technology (act)"),
    (r"^climate.*consortium|^mcsc", "climate & sustainability consortium"), (r"^dlab$", "d-lab"),
    (r"^laboratoryforinformationanddecision|^lids$", "lids"), (r"^jpal$|povertyactionlab", "j-pal"),
    (r"^researchlaboratoryofelectronics|^rle$", "rle"), (r"^stars$|admissions", "admissions / stars"),
    (r"^mitesofficeof", "mites / oeop"), (r"^industrialliaison", "industrial liaison program"),
    (r"^schoolofscience|^deanofscience$", "school of science dean's office"),
    (r"^sloanleadership|^sloanschoolofmanagement|^sloandeansoffice", "sloan dean's office"),
    (r"^schoolofengineering|^school of engineering$|^deanofengineering", "school of engineering"),
]

def key_of(name, course="", utype=""):
    ut = (utype or "").lower()
    if ut == "program":
        c = course_of(name, "")
        return f"course:{c}" if c else f"name:{name_key(name)}"
    if ut not in ("department", "mit-department", ""):
        return f"name:{name_key(name)}"
    c = course_of(name, course)
    return f"course:{c}" if c else f"name:{name_key(name)}"

def money(s):
    s = (s or "").replace(",", "")
    m = re.search(r"\d+(\.\d+)?", s)
    return float(m.group()) if m else None

# ---------- load ----------
research = []
for p in sorted(glob.glob(os.path.join(RD, "*.csv"))):
    if os.path.basename(p).startswith("_"): continue
    for r in rows(p):
        if not r.get("unit"): continue
        r["_file"] = os.path.basename(p)
        research.append(r)
history = []
for p in sorted(glob.glob(os.path.join(RD, "_history_*.csv"))):
    history += rows(p)
print(f"research rows {len(research)}  history rows {len(history)}", file=sys.stderr)

MIT_CATS = {"mit-department", "mit-lab-center", "mit-office", "mit-grant-fund"}
# every research row is kept; rows that point at the same unit share history only via the primary row
def base(name): return re.split(r"\s+[-–—]\s+", name or "", maxsplit=1)[0]
def rkey(r):
    k = key_of(r["unit"], r.get("course_number"), r.get("unit_type"))
    if k.startswith("name:") and re.search(r"\s[-–—]\s", r["unit"]):
        kb = key_of(base(r["unit"]), r.get("course_number"), r.get("unit_type")); k = kb
    return k
groups = defaultdict(list)
for r in research:
    r["_score"] = sum(bool(r.get(c)) for c in ("best_contact_email", "alt_contact_email", "head_email", "funding_form_url"))
    groups[rkey(r)].append(r)
units = {}
for k, rs in groups.items():
    rs.sort(key=lambda r: (r.get("unit_type", "") != "department", bool(re.search(r"\s[-–—]\s", r["unit"])), -r["_score"]))
    units[k] = rs[0]
    for i, r in enumerate(rs[1:], 2):
        r["_secondary_of"] = rs[0]["unit"]; units[f"{k}#{i}"] = r

hist_by = defaultdict(list)
for h in history:
    if h.get("org_category") in MIT_CATS or not h.get("org_category"):
        hist_by[key_of(h.get("org"), h.get("course_number"), h.get("org_category"))].append(h)

# add MIT units that only appear in history
for k, hs in hist_by.items():
    if k not in units:
        h = sorted(hs, key=lambda x: x.get("year", ""), reverse=True)[0]
        units[k] = {"unit": h["org"], "school": "", "unit_type": h.get("org_category", "").replace("mit-", ""),
                    "course_number": h.get("course_number", ""), "best_contact_name": h.get("contact_name", ""),
                    "best_contact_title": h.get("contact_title", ""), "best_contact_email": h.get("contact_email", ""),
                    "why_this_contact": f"From {h.get('year')} Spokes tracker (not re-verified online)",
                    "fit_for_spokes": "", "notes": "", "_file": "history-only", "_score": 0}

if os.environ.get("DEBUG_KEYS"):
    for k in sorted(k for k, u in units.items() if u.get("_file") == "history-only"):
        hs = hist_by[k]; print(f"HO {k:45} {len(hs):3} {hs[0]['org'][:45]:45} {sum((money(h.get('amount_given')) or 0) for h in hs):8.0f}", file=sys.stderr)
    for k in sorted(k for k in units if "#" not in k and units[k].get("_file") != "history-only"):
        print(f"RS {k:45} {units[k]['unit'][:50]:50} hist={len(hist_by.get(k, []))}", file=sys.stderr)
# ---------- team majors -> suggested sender ----------
MAJORS = {"6": "Sarah / Gloria (6-4), Michelle (6-2), Kevin (6-3)", "2": "Max (2), Liv (2/11), Kevin (2A)",
          "8": "Neelu (8)", "11": "Liv (11), Noah (11/14)", "14": "Noah (14)"}
TEAM = ["Sarah", "Michelle", "Kevin", "Noah", "Gloria", "Liv", "Neelu", "Max"]

def hist_summary(hs):
    by_year = defaultdict(list)
    for h in hs:
        a = money(h.get("amount_given"))
        o = h.get("outcome", "")
        txt = f"${a:,.0f}" if a else (o or "asked")
        by_year[h.get("year", "?")].append(txt)
    return " · ".join(f"{y}: {', '.join(dict.fromkeys(v))}" for y, v in sorted(by_year.items(), reverse=True))

def hist_notes(hs):
    out = []
    for h in sorted(hs, key=lambda x: x.get("year", ""), reverse=True):
        n = h.get("notes", "")
        if n and n not in out: out.append(f"({h.get('year')}) {n}")
    return " | ".join(out)[:900]

def priority(u, hs):
    outs = {(h.get("year", ""), h.get("outcome", "")) for h in hs}
    dont = any(o == "dont-ask-again" and y >= "2025" for y, o in outs) or \
        re.search(r"don.?t ask|do not ask", hist_notes(hs), re.I)
    gave = any(money(h.get("amount_given")) for h in hs)
    gave_recent = any(money(h.get("amount_given")) and h.get("year", "") >= "2022" for h in hs)
    fit = (u.get("fit_for_spokes") or "").lower()
    if dont: return "Skip"
    if gave_recent or (fit == "high" and (gave or u.get("funding_form_url"))): return "A"
    if gave or fit == "high": return "B"
    if fit == "medium": return "C"
    return "D"

# ---------- workbook ----------
F = "Arial"
HDR = PatternFill("solid", fgColor="1F3864"); HFONT = Font(name=F, bold=True, color="FFFFFF", size=10)
INPUT = PatternFill("solid", fgColor="FFF2CC"); BASE = Font(name=F, size=10); LINK = Font(name=F, size=10, color="0563C1", underline="single")
PRI_FILL = {"A": "C6EFCE", "B": "DDEBF7", "C": "F2F2F2", "D": "FFFFFF", "Skip": "F8CBAD"}
thin = Side(style="thin", color="D9D9D9"); BORDER = Border(bottom=thin)
wb = Workbook()

def header(ws, cols, widths):
    ws.append(cols)
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=1, column=i); cell.fill = HDR; cell.font = HFONT
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    ws.row_dimensions[1].height = 32; ws.freeze_panes = "C2"

# --- Departments sheet ---
ws = wb.active; ws.title = "Departments 2027"
COLS = ["Key", "Unit", "Priority", "School", "Course", "Type", "Best contact", "Title", "Email", "Phone",
        "Why this contact", "Backup contact", "Backup email", "Head (cc)", "Head email", "General email",
        "Funding form", "Suggested sender (major)", "Responsible Spokey", "Status", "Bump?", "Date emailed",
        "Amount 2027 ($)", "Notes 2027", "Past giving total ($)", "Years gave", "Giving history", "Past notes / policies",
        "Fit", "Fit reason", "Contact vs 2026", "Research notes", "Sources", "Checked"]
W = [14, 34, 8, 16, 7, 11, 24, 28, 26, 13, 30, 22, 24, 22, 22, 22, 18, 24, 14, 13, 9, 11, 11, 28, 12, 8, 26, 45, 7, 34, 11, 40, 30, 10]
header(ws, COLS, W)
ci = {c: i + 1 for i, c in enumerate(COLS)}
order = {"A": 0, "B": 1, "C": 2, "D": 3, "Skip": 4}
items = []
for k, u in units.items():
    pk = k.split("#")[0]
    hs = [] if "#" in k else hist_by.get(k, [])
    pr = priority(units[pk], hist_by.get(pk, []))
    items.append((order[pr], u.get("school", "") or "zz", pk, "#" in k, u["unit"].lower(), k, u, hs, pr))
items.sort()
for n, (_, _, pk, _, _, k, u, hs, pr) in enumerate(items, start=2):
    c = pk.split(":", 1)[1] if pk.startswith("course:") else ""
    vals = {
        "Key": k, "Unit": u["unit"], "Priority": pr, "School": u.get("school", ""), "Course": c or u.get("course_number", ""),
        "Type": u.get("unit_type", ""), "Best contact": u.get("best_contact_name", ""), "Title": u.get("best_contact_title", ""),
        "Email": u.get("best_contact_email", ""), "Phone": u.get("best_contact_phone", ""), "Why this contact": u.get("why_this_contact", ""),
        "Backup contact": " — ".join(x for x in (u.get("alt_contact_name", ""), u.get("alt_contact_title", "")) if x),
        "Backup email": u.get("alt_contact_email", ""),
        "Head (cc)": " — ".join(x for x in (u.get("head_name", ""), u.get("head_title", "")) if x), "Head email": u.get("head_email", ""),
        "General email": u.get("general_email", ""), "Funding form": u.get("funding_form_url", ""),
        "Suggested sender (major)": MAJORS.get(c, ""), "Giving history": hist_summary(hs) if "#" not in k else f"Same unit as '{units[pk]['unit']}' (history is on that row)", "Past notes / policies": hist_notes(hs),
        "Fit": u.get("fit_for_spokes", ""), "Fit reason": u.get("fit_reason", ""), "Contact vs 2026": u.get("contact_status_vs_2026", ""),
        "Research notes": u.get("notes", ""), "Sources": u.get("source_urls", ""), "Checked": u.get("checked_on", "") or ("" if u["_file"] != "history-only" else "not re-checked"),
    }
    for col, v in vals.items():
        ws.cell(row=n, column=ci[col], value=v)
    gh = "'Giving History'"
    ws.cell(row=n, column=ci["Past giving total ($)"], value=f"=SUMIFS({gh}!$H:$H,{gh}!$A:$A,$A{n})").number_format = '$#,##0;-$#,##0;"-"'
    ws.cell(row=n, column=ci["Years gave"], value=f'=COUNTIFS({gh}!$A:$A,$A{n},{gh}!$H:$H,">0")')
    ws.cell(row=n, column=ci["Amount 2027 ($)"]).number_format = '$#,##0;-$#,##0;"-"'
    for i in range(1, len(COLS) + 1):
        cell = ws.cell(row=n, column=i)
        cell.font = BASE; cell.alignment = Alignment(vertical="top", wrap_text=COLS[i - 1] in ("Why this contact", "Past notes / policies", "Fit reason", "Research notes", "Notes 2027", "Giving history", "Title"))
        cell.border = BORDER
    for col in ("Responsible Spokey", "Status", "Bump?", "Date emailed", "Amount 2027 ($)", "Notes 2027"):
        ws.cell(row=n, column=ci[col]).fill = INPUT
    ws.cell(row=n, column=ci["Priority"]).fill = PatternFill("solid", fgColor=PRI_FILL[pr])
    for col in ("Email", "Backup email", "Head email", "General email"):
        e = ws.cell(row=n, column=ci[col])
        first = re.split(r"[,; ]+", e.value or "")[0]
        if "@" in first: e.hyperlink = f"mailto:{first}"; e.font = LINK
    fcell = ws.cell(row=n, column=ci["Funding form"])
    if (fcell.value or "").startswith("http"): fcell.hyperlink = fcell.value; fcell.font = LINK
last = ws.max_row
ws.auto_filter.ref = f"A1:{get_column_letter(len(COLS))}{last}"
ws.column_dimensions["A"].hidden = True
dv = DataValidation(type="list", formula1='"Not contacted,Emailed,Bumped,Meeting,Pending,Yes,No,Skip"', allow_blank=True)
dv2 = DataValidation(type="list", formula1='"' + ",".join(TEAM) + '"', allow_blank=True)
dv3 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
for d, col in ((dv, "Status"), (dv2, "Responsible Spokey"), (dv3, "Bump?")):
    ws.add_data_validation(d); L = get_column_letter(ci[col]); d.add(f"{L}2:{L}{last}")
ws.cell(row=1, column=ci["Priority"]).comment = Comment(
    "A = gave since 2022, or high fit with a funding form/past gift. B = gave before 2022 or high fit. "
    "C = medium fit. D = low fit / unknown. Skip = told Spokes not to ask again (2025-2026).", "Spokes KB")
ws.cell(row=1, column=ci["Past giving total ($)"]).comment = Comment("Sum of amounts in the Giving History tab for this unit (all years).", "Spokes KB")

# --- Giving History sheet ---
gh = wb.create_sheet("Giving History")
HC = ["Key", "Org", "Category", "Course", "Year", "Outcome", "Asked ($)", "Given ($)", "In-kind", "Contact", "Title", "Email",
      "Responsible Spokey", "Date contacted", "Notes", "Source file"]
header(gh, HC, [14, 32, 14, 7, 6, 13, 10, 10, 18, 22, 24, 26, 14, 12, 50, 40])
hist_sorted = sorted(history, key=lambda h: (h.get("year", ""), money(h.get("amount_given")) or 0), reverse=True)
for n, h in enumerate(hist_sorted, start=2):
    is_mit = h.get("org_category") in MIT_CATS or not h.get("org_category")
    k = key_of(h.get("org"), h.get("course_number"), h.get("org_category")) if is_mit else f"ext:{name_key(h.get('org'))}"
    vals = [k, h.get("org"), h.get("org_category"), h.get("course_number"), h.get("year"), h.get("outcome"),
            money(h.get("asked_amount")), money(h.get("amount_given")), h.get("in_kind"), h.get("contact_name"),
            h.get("contact_title"), h.get("contact_email"), h.get("responsible_spokey"), h.get("date_contacted"),
            h.get("notes"), h.get("source_file")]
    for i, v in enumerate(vals, 1):
        c = gh.cell(row=n, column=i, value=v); c.font = BASE
        c.alignment = Alignment(vertical="top", wrap_text=i == 15); c.border = BORDER
    for i in (7, 8): gh.cell(row=n, column=i).number_format = '$#,##0;-$#,##0;"-"'
gh.auto_filter.ref = f"A1:P{gh.max_row}"; gh.column_dimensions["A"].hidden = True

# --- Other past donors (non-MIT) summary ---
od = wb.create_sheet("Other Past Donors")
OC = ["Org", "Category", "Years asked", "Total given ($)", "Last outcome", "Best known contact", "Email", "Phone", "Notes"]
header(od, OC, [32, 14, 16, 12, 14, 26, 28, 14, 70])
ext = defaultdict(list)
for h in history:
    if h.get("org_category") not in MIT_CATS and h.get("org_category"):
        ext[name_key(h.get("org"))].append(h)
ext_rows = []
for k, hs in ext.items():
    hs = sorted(hs, key=lambda x: x.get("year", ""), reverse=True)
    tot = sum(money(h.get("amount_given")) or 0 for h in hs)
    contact = next((h for h in hs if h.get("contact_email") or h.get("contact_name")), hs[0])
    ext_rows.append((-tot, hs[0].get("org"), hs, tot, contact))
for n, (_, org, hs, tot, ct) in enumerate(sorted(ext_rows), start=2):
    vals = [org, hs[0].get("org_category"), ", ".join(dict.fromkeys(h.get("year", "") for h in hs)), None,
            hs[0].get("outcome"), " — ".join(x for x in (ct.get("contact_name"), ct.get("contact_title")) if x),
            ct.get("contact_email"), ct.get("contact_phone"), hist_notes(hs)]
    for i, v in enumerate(vals, 1):
        c = od.cell(row=n, column=i, value=v); c.font = BASE; c.alignment = Alignment(vertical="top", wrap_text=i == 9); c.border = BORDER
    od.cell(row=n, column=4, value=f"=SUMIFS('Giving History'!$H:$H,'Giving History'!$A:$A,\"ext:{name_key(org)}\")").number_format = '$#,##0;-$#,##0;"-"'
od.auto_filter.ref = f"A1:I{od.max_row}"; od.freeze_panes = "B2"

# --- Tracking (summary) ---
tr = wb.create_sheet("Tracking", 0)
tr.column_dimensions["A"].width = 38; tr.column_dimensions["B"].width = 16; tr.column_dimensions["C"].width = 70
D = "'Departments 2027'"; SL = get_column_letter(ci["Status"]); AL = get_column_letter(ci["Amount 2027 ($)"]); PL = get_column_letter(ci["Priority"])
lines = [
    ("MIT department outreach — Spokes 2027", None, f"Built {TODAY} from past Spokes trackers (2013–2026) + web research of MIT pages. Re-run tools/build_dept_sheet.py to rebuild from raw/dept_research/."),
    (None, None, None),
    ("Department goal ($)", 15000, "Input (blue). Assumption: departments gave ~$20K in 2025 and ~$10K in 2026; change as the team decides."),
    ("Committed so far ($)", f"=SUM({D}!{AL}2:{AL}{last})", "Sum of 'Amount 2027 ($)' on the Departments tab"),
    ("% of department goal", "=IF(B3=0,0,B4/B3)", None),
    (None, None, None),
    ("Units listed", f"=COUNTA({D}!B2:B{last})", None),
    ("Priority A (gave recently / strong fit)", f'=COUNTIF({D}!{PL}2:{PL}{last},"A")', None),
    ("Priority B", f'=COUNTIF({D}!{PL}2:{PL}{last},"B")', None),
    ("Skip (asked us not to re-ask)", f'=COUNTIF({D}!{PL}2:{PL}{last},"Skip")', None),
    (None, None, None),
    ("Emailed", f'=COUNTIF({D}!{SL}2:{SL}{last},"Emailed")+COUNTIF({D}!{SL}2:{SL}{last},"Bumped")', None),
    ("Pending / meeting", f'=COUNTIF({D}!{SL}2:{SL}{last},"Pending")+COUNTIF({D}!{SL}2:{SL}{last},"Meeting")', None),
    ("Yes", f'=COUNTIF({D}!{SL}2:{SL}{last},"Yes")', None),
    ("No", f'=COUNTIF({D}!{SL}2:{SL}{last},"No")', None),
    (None, None, None),
    ("Past MIT-unit giving, all years ($)", "=SUMIFS('Giving History'!H:H,'Giving History'!C:C,\"mit-*\")", "From the Giving History tab"),
]
for r, (a, b, c) in enumerate(lines, start=1):
    if a: tr.cell(row=r, column=1, value=a).font = Font(name=F, size=10, bold=r == 1)
    if b is not None:
        cell = tr.cell(row=r, column=2, value=b); cell.font = Font(name=F, size=10, color="0000FF" if not str(b).startswith("=") else "000000")
        cell.number_format = "0.0%" if r == 5 else ('$#,##0' if r in (3, 4, 17) else "0")
    if c: tr.cell(row=r, column=3, value=c).font = Font(name=F, size=9, italic=True, color="595959"); tr.cell(row=r, column=3).alignment = Alignment(wrap_text=True)
tr["B3"].fill = INPUT
tr.cell(row=1, column=1).font = Font(name=F, size=13, bold=True)

legend = [
    "HOW TO USE",
    "1. Departments 2027 tab: one row per MIT department, lab, center or office. Sorted by Priority, then school.",
    "2. Fill in only the yellow columns: Responsible Spokey, Status, Bump?, Date emailed, Amount 2027, Notes 2027.",
    "   Example: Responsible Spokey = Max · Status = Emailed · Bump? = No · Date emailed = 12/2 · Amount 2027 = 500 · Notes = 'said ask again in Jan'.",
    "3. Email the 'Best contact'; cc the 'Head (cc)'. Send from someone in that major when possible ('Suggested sender').",
    "4. Check 'Past notes / policies' first: some units asked us not to re-ask, fund only their own majors, or use a form.",
    "5. 'Giving history' and 'Past giving total' come from the Giving History tab (every past ask, 2013–2026).",
    "6. Other Past Donors tab: companies, foundations, bike shops, alumni clubs and grants from past years.",
    "Template email: docs/2026/fundraising/2026_email_templates.md · Cost object: 2530032 (internal transfers).",
    "Contacts were checked online on 2026-11-25. People change jobs, so if an email bounces, check the unit's website.",
]
for i, t in enumerate(legend):
    c = tr.cell(row=20 + i, column=1, value=t); c.font = Font(name=F, size=10, bold=i == 0)
tr.sheet_view.showGridLines = False

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print(f"wrote {OUT}: {last - 1} units, {len(history)} history rows, {len(ext_rows)} other donors", file=sys.stderr)
