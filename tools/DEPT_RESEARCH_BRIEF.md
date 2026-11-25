# Brief: MIT department/unit funding contacts for Spokes 2027 (web research)

Context: MIT Spokes is a student team (run through MIT's Edgerton Center) that bikes ~4,000 miles DC → San Francisco each summer and runs free hands-on STEM "learning festivals" for K-12 kids in rural/underserved communities and juvenile detention centers. The 2027 team must raise ~$40-50K and asks MIT departments, labs, centers and offices for small gifts ($150–$5,000), transferred internally to the Spokes cost object. Past wins (year): Edgerton $5,000 (2026), School of Engineering $2,000 (2026), MIT.nano $2,000 (2026), Music & Theater Arts $500 (2026), AeroAstro $500 (2026), Course 4 $150 (2026), Libraries $2,500 (2024), MIT Museum $1,000 (2024), Climate Consortium / History / Urban Science / Materials Science $500 each (2024), Physics $2,500 (2018/2019), Mech E $5,000 (2018).

2027 team majors (use for "who should send it": departments prefer a request from their own major): Course 6-4 (x2), 6-2, 6-3/2A, 2, 2/11, 8, 11/14.

## Your job
For EVERY unit in your assigned slice (below), find the best person to email a student-group funding request, from the official MIT website for that unit (staff/people/administration/contact pages), MIT News, or other official MIT pages. Use WebSearch and WebFetch (fall back to `curl -sL` in Bash if needed). Read-only: never email anyone, never submit forms, never log in.

Contact priority (best first):
1. An explicit student-group / outreach funding form or contact, if the unit has one (record the URL).
2. Director / Assistant Director of Administration & Finance (DAF/ADF), Administrative Officer, Financial Officer.
3. Development / leadership-giving officer for that unit.
4. Department head / director (usually cc'd).
5. Undergraduate/academic administrator, outreach or communications lead.

Also check the 2026 team's contacts for your units in `/Users/Sarah/spokes/docs/master-guide/sub-guides/linked/2026_fundraising-tracking.md` (section "## Departments") and in `/Users/Sarah/spokes/contacts/contacts.csv`: verify whether each listed person still holds that role (set `contact_status` = current | changed | not-found). If someone left, give the replacement.

Mark `fit_for_spokes` high/medium/low with a short reason: mission fit (K-12 STEM outreach, education, public service, rural communities, transportation/cycling, sustainability/climate, maker/engineering), past giving to Spokes, a 2027 team member in that major, or known policies (e.g., "only funds its own majors", "has a funding form", "said don't ask again").

## Output
Write ONE CSV (UTF-8, header row, properly quoted) to the path you are given, one row per unit, columns exactly:
`unit,school,unit_type,course_number,website,best_contact_name,best_contact_title,best_contact_email,best_contact_phone,why_this_contact,alt_contact_name,alt_contact_title,alt_contact_email,head_name,head_title,head_email,general_email,funding_form_url,contact_status_vs_2026,fit_for_spokes,fit_reason,notes,source_urls,checked_on`
- `unit_type`: department | program | lab | center | institute | office | fund | school-dean
- `checked_on`: 2026-11-25
- Only record emails you actually saw on a page (no guessing kerberos patterns). If none found, leave blank and say so in notes.
- `source_urls`: the page(s) where you saw each contact, separated by ` ; `.

Rules: do not put any Spokes team member's name or personal info into web searches (search only unit names and roles). Do not spawn sub-agents. Be thorough: cover every unit in your slice, plus any other relevant MIT unit in your area you discover. Final reply: one line with the row count and the 3-5 most promising leads.
