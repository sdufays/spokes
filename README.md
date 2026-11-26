# 🚲 MIT Spokes knowledge base

Everything a Spokes team needs to plan and ride the trip, consolidated from **every Spokes blog (2013–2026)**, the **shared Spokes Google Drive** (all year folders, Hub, Tanzania, Master Guides) and **Spokes email**. Junk was discarded; everything kept has its **year** attached. **Recent years first** everywhere.

## Start here
1. **[Themes](themes/)** — one file per topic with TL;DR, key numbers by year, playbook, timeline, what worked, contacts, templates:
   - [Timeline & master checklist](themes/01-timeline-and-checklist.md)
   - [Team roles, meetings & communication](themes/02-team-roles-and-meetings.md)
   - [Fundraising](themes/03-fundraising.md)
   - [Grants](themes/04-grants.md)
   - [Corporate sponsorship & in-kind donations](themes/05-sponsorship.md)
   - [Budget & finances](themes/06-budget-and-finances.md)
   - [MIT & Edgerton Center admin](themes/07-mit-edgerton-admin.md)
   - [Route planning](themes/08-route-planning.md)
   - [Housing & hosts](themes/09-housing-and-hosts.md)
   - [Learning festivals & curriculum](themes/10-learning-festivals.md)
   - [Gear & bikes](themes/11-gear-and-bikes.md)
   - [Support car & logistics](themes/12-support-car-and-logistics.md)
   - [Food](themes/13-food.md)
   - [Training, safety & health](themes/14-training-safety-health.md)
   - [Media, social media, website & blog](themes/15-media-social-website.md)
   - [Recruiting & onboarding](themes/16-recruiting-and-onboarding.md)
   - [Top lessons learned & advice from every past team (cross-cutting; strongest, most repeated advice first)](themes/17-lessons-learned.md)
2. **[2027 working folder](2027/)**: this year's **[meeting notes](2027/meetings/)** (what happened + follow-ups) and **[fundraising outreach spreadsheet](2027/fundraising/)** (every MIT department/lab/office with best contact and past giving).
3. **[Contacts](contacts/)** — 3025 people & orgs (sponsors, hosts, LF partners, MIT staff, alumni, bike shops…), with years and outcomes. Spreadsheet: [contacts.csv](contacts/contacts.csv).
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
| [2027](years/2027/) | 0 | 4 | 13 | 0 |
| [2026](years/2026/) | 77 | 62 | 2 | 29 |
| [2025](years/2025/) | 82 | 103 | 2 | 35 |
| [2024](years/2024/) | 78 | 138 | 4 | 0 |
| [2023](years/2023/) | 0 | 57 | 1 | 57 |
| [2022](years/2022/) | 63 | 165 | 0 | 48 |
| [2019](years/2019/) | 0 | 87 | 0 | 2 |
| [2018](years/2018/) | 0 | 121 | 0 | 1 |
| [2017](years/2017/) | 12 | 180 | 0 | 16 |
| [2016](years/2016/) | 0 | 47 | 0 | 3 |
| [2015](years/2015/) | 13 | 14 | 0 | 0 |
| [2014](years/2014/) | 20 | 54 | 0 | 0 |
| [2013](years/2013/) | 27 | 40 | 0 | 13 |
| [2012](years/2012/) | 0 | 1 | 0 | 0 |

**Known gaps:** 2016, 2018, 2019 and 2023 blogs no longer exist online (sites deleted, never archived). No 2020–2021 material was found anywhere (likely no trip those years). The 2024 Drive folder was read through the connector only, so its long spreadsheets (fundraising tracker, budget log) are truncated — download "Spokes 2024" from Drive as a zip to complete them. Google Forms responses can't be exported by the connector. `2013/OrganizedContacts.xlsx` is password-protected.

## How it stays up to date
- **Email:** every morning at 8:00 a job on Sarah's Mac (`tools/mail/daily.sh`, launchd `com.sdufays.spokes-mail`) picks up new Spokes emails (saved by the Apple Mail rule "Spokes → archive"), files them under `email/`, adds contacts, adds dated bullets to the relevant theme's *Recent updates*, rebuilds and pushes.
- **Rebuild indexes after editing:** `.venv/bin/python tools/build.py`
- **Rewrite a theme:** `tools/run_themes.sh 03-fundraising`
- Raw scrapes/exports live in `raw/` and `~/spokes_sources/` (not committed).
