# Brief: tag & extract MIT Spokes daily blog posts

MIT Spokes = student team biking across the US running "learning festivals" (STEM activities for kids). A 2027 team (organizers + riders) will use your output to plan and do their trip. Your job: read each blog post in your batch file fully and extract what's useful.

Input: a batch file listing blog post paths (one per line). Read every post completely (Read tool).
Tag vocabulary: /Users/Sarah/spokes/tools/TAGS.md — read it first and use ONLY those tags (+ `place:` tags).

Output: write ONE JSON Lines file (path given in your assignment), one JSON object per post, exactly these keys:
```
{"path": "<the path from the batch file>",
 "summary": "<1-2 sentences, plain and specific: what happened that day>",
 "tags": ["route", "weather", "place:kentucky", ...],
 "from": "<start town, ST or null>", "to": "<end town, ST or null>",
 "miles": <number or null>, "elevation_ft": <number or null>,
 "slept_at": "<where they stayed: e.g. 'First Baptist Church, Hazard KY (church host)', 'Koomer Ridge campground', 'Warmshowers host', 'MIT alum home'; null if not said>",
 "learning_festival": "<where/with whom/what activities, or null>",
 "contacts": ["<named hosts/orgs/people who helped, with town>", ...],
 "planning_notes": ["<concrete, reusable fact or lesson for a future team>", ...],
 "relevance": "high|medium|low"}
```
- planning_notes: the gold. Concrete things a future team could act on: road/route warnings (dangerous roads, gravel, no shoulder, dogs), water/food gaps, good/bad hosts or campgrounds, bike-shop help, weather patterns, costs, what gear failed/worked, LF tips, team/logistics lessons, sponsor/donor mentions. Keep each note short and self-contained, include the place. Empty list if none.
- relevance: high = lots of planning info; medium = some; low = mostly personal/reflective.
- Don't invent facts. null when not stated.
- Use the Write tool to write the whole .jsonl file at the end (or append in chunks with Bash heredoc if large). Valid JSON per line (escape quotes).

Final reply: just "<n> posts done" plus any posts you couldn't read.
