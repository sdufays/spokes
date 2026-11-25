# Brief: write ONE consolidated theme file for the Spokes knowledge base

Context: MIT Spokes = student team biking across the US each summer running learning festivals (STEM activities for kids). The 2027 team (organizers + riders; the repo owner does fundraising, finances/budget, food and social media) needs everything about a theme in ONE place, easy to scan, with the YEAR on every fact and recent years first.

Sources in /Users/Sarah/spokes (read-only except your output file):
- `catalog.csv` — every blog post and doc: kind, year, title, tags, relevance, summary, path. Start here: filter by your theme's tags and keywords.
- `docs/<year|master-guide|hub>/**` — full Drive documents. `docs/master-guide/` = the official, most recent how-to guides (edited through 2026): treat them as the backbone.
- `blogs/by-tag/<tag>.md`, `blogs/by-place/*.md` — blog planning notes, already year-labeled.
- `email/**` — digests of Spokes emails (if present).
- `contacts/<category>.md` and `contacts/contacts.csv` — people/orgs.
- `years/<year>/README.md` — per-year highlights.
- Search helper: `.venv/bin/python tools/find.py <words> [--year Y] [--tag T] [--kind doc|blog|email]`
- 2027 working notes: `2027/`

Read broadly (aim for every high/medium relevance doc with your tags, newest years first; skim older years for lessons). Don't invent anything. When sources conflict, say so and cite both with years.

Write your file to the path you're given. Structure:
```
# <Theme>
_Last built: <today>. Sources: N docs, M blog posts, K emails. Recent years first; every fact has its year._

## TL;DR for 2027
5-10 bullets: what to do, by when, key numbers, biggest pitfalls. (each bullet ends with (YEAR[, YEAR]))

## Key numbers by year            ← table, newest year first, only if the theme has numbers (money raised, budget, miles, # hosts, # LFs…)

## Playbook — how to do it          ← step-by-step, synthesized mainly from the most recent master guides + what actually happened; mark each step's source year
## Timeline & deadlines             ← month-by-month (semester before → trip → after), with years
## What worked / what didn't        ← grouped by year, newest first, concrete
## Key contacts                     ← top 10-25 most useful people/orgs with outcome + year; link to contacts/<category>.md for the rest
## Templates & examples             ← links to the actual docs (email templates, budgets, forms, slides)
## Year by year                     ← ### 2026, ### 2025, … down to the oldest: what that team did for this theme, numbers, links
## Sources                          ← bullet list of relative links to every doc/post used
```
Links must be relative from the themes/ folder (e.g. `../docs/2026/finances/2026_expenses_and_budget.md`). Be dense and specific; long is fine (this replaces reading 100 docs), but no filler. Final reply: one line with counts.
