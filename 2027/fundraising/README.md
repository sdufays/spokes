# Spokes 2027 fundraising

- **[2027_mit_department_outreach.xlsx](2027_mit_department_outreach.xlsx)**: department outreach tracker (upload to Google Drive to share; it opens as a Google Sheet).
  - **Tracking**: totals vs. goal, status counts, how-to legend.
  - **Departments 2027**: 191 MIT departments, labs, centers, offices and MIT funds, sorted by priority. Each row has the best contact to email (checked online 2026-11-25), a backup contact, the head to cc, any funding form, a suggested sender by major, past giving by year, and policy notes such as "don't ask again" or "only funds own majors". Fill in the yellow columns.
  - **Giving History**: every past ask and gift from the Drive trackers, 2013–2026 (934 rows).
  - **Other Past Donors**: companies, foundations, bike shops, alumni clubs and individuals ≥$500 from past years.
- Rebuild: `.venv/bin/python tools/build_dept_sheet.py` (inputs in `raw/dept_research/`; web-research brief in `tools/DEPT_RESEARCH_BRIEF.md`). Rebuilding overwrites anything typed into the workbook, so once the team starts tracking in Google Sheets, edit there instead.
- Email template: `docs/2026/fundraising/2026_email_templates.md`. Cost object for internal transfers: 2530032.
