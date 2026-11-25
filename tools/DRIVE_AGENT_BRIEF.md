# Brief: process one part of the MIT Spokes shared Google Drive into a local knowledge base

Context: MIT Spokes is a student team that bikes across the US each summer running "learning festivals" (STEM activities for kids). The user is on the Spokes 2027 team (roles: fundraising, finances/budget, food, social media) and wants every piece of info that could help PLAN or DO the trip, organized locally. Recent years matter most. ALWAYS keep the year attached to every fact.

RULES
- READ-ONLY on Google Drive. Never create, edit, move, share, trash or comment on anything in Drive. Only use search_files / get_file_metadata / read_file_content.
- Write output only under the output dir you are given (create it with mkdir -p).
- Folder IDs given are shortcut targets. List children with search_files query `parentId = '<folderId>'` (pageSize 100, excludeContentSnippets true, paginate with nextPageToken). Recurse into subfolders (mimeType application/vnd.google-apps.folder) and follow shortcuts (application/vnd.google-apps.shortcut -> shortcutDetails.targetFileId).
- Read every Doc, Sheet, Slides, PDF, docx, xlsx, pptx, txt with read_file_content.
- Tags: use the vocabulary in /Users/Sarah/spokes/tools/TAGS.md (read it first).

FOR EACH FILE decide: KEEP (anything plausibly useful for planning/doing the trip: budgets, sponsor lists & emails, grant apps, route plans, host/housing lists, LF curricula, gear lists, timelines, checklists, meeting notes with decisions, reflections/lessons learned, templates, contact lists of hosts/sponsors/partners) or DISCARD (empty/untitled docs, pure duplicates, stubs, irrelevant personal stuff, obsolete junk with no lesson). When unsure, KEEP with relevance: low.

FOR EACH KEPT DOCUMENT write `<outdir>/<subfolder-path-slug>/<YYYY>_<file-title-slug>.md`:
```
---
title: "<original title>"
year: <spokes year this belongs to (from folder), int>
drive_path: "<Spokes YYYY/sub/folder/Title>"
drive_link: "<viewUrl>"
type: <doc|sheet|slides|pdf|other>
modified: "<YYYY-MM-DD>"
relevance: <high|medium|low>
tags: [..]
summary: "<1-3 sentences: what it is and why it's useful for 2027>"
---
<full useful content, cleaned into readable markdown (tables for sheets). Keep host/sponsor/partner contact info. Trim boilerplate. For huge sheets keep all meaningful rows.>
```
PRIVACY: this goes in a PRIVATE repo and the user wants contact info KEPT. Keep names, emails, phones, orgs, cities/addresses of everyone relevant to Spokes (past riders/alumni, hosts, sponsors, donors, Edgerton/MIT staff, LF partners/schools, bike shops, press). REMOVE only: SSNs, passport/license numbers, card/bank numbers, medical details of individuals, passwords/logins, and riders' family emergency-contact entries (replace with "[redacted]").

IMAGES/VIDEOS: Inspect images with read_file_content (it returns a description). Inspect every image that might carry info (scans, screenshots, maps, flyers, posters, whiteboards, receipts, sponsor graphics, jersey/shirt designs, logos, LF activity setups, gear layouts). For big albums of camera photos (IMG_/DSC_/PXL_ names, >40 photos) inspect a sample of ~10 and decide at album level. KEEP an image if it could be useful in any way: informational images always; plus a small set of the best group/action/LF photos per year that would be good for fundraising/social media. Do NOT download images. Record decisions in the image list (below). Videos: list only.

ALSO WRITE:
0. `<outdir>/_contacts.csv` — EVERY person/organization with contact info you find anywhere in the folder (docs, sheets, emails, sponsor lists, host lists, contact sheets). Columns: name,organization,category(rider-alum|host|sponsor|donor|mit-staff|lf-partner|school|bike-shop|press|campground|other),role_or_notes,email,phone,city_state,year,outcome(e.g. "hosted us", "said no", "donated $500", blank if unknown),source_file,source_link. One row per person/org per source; CSV-quote fields properly.
1. `<outdir>/_manifest.md` — a table of EVERY file seen: path | type | decision (kept/discarded/image-keep/image-skip/album) | reason (few words) | link.
2. `<outdir>/_images_keep.csv` — columns: file_id,name,drive_path,year,category(map|flyer|graphic|logo|jersey|lf-activity|gear|group-photo|action-photo|screenshot|other),why,view_url
3. `<outdir>/_highlights.md` — the 10-25 most valuable facts/lessons for a 2027 team from this folder, each a bullet ending with "(YEAR, source: <file title>)". Prioritize: money (how much raised, from whom, budget totals), sponsors that said yes, route/housing tactics, timelines/deadlines, mistakes to avoid.

FINAL REPLY (short, <200 words): counts (files seen / docs kept / discarded / images kept / contacts), the 5 most important files, and any files you could not read.

NOTE ON INACCESSIBLE ITEMS: some old folders/files (IDs starting with `0B`) need a Drive "resource key" the connector can't send, so they show as "not found" or list as empty. Don't spend more than 2 attempts on one; record it in _manifest.md as `inaccessible-legacy` with its viewUrl so the user can download it manually.
