#!/bin/zsh
# Launch one headless theme writer per row of tools/themes.tsv, all in parallel.
cd "$HOME/spokes"; mkdir -p themes logs
while IFS=$'\t' read -r slug desc tags; do
  [ -n "$1" ] && [[ "$slug" != $1* ]] && continue
  claude -p "Read /Users/Sarah/spokes/tools/THEME_BRIEF.md and follow it exactly. Your theme: \"$desc\". Most relevant tags: $tags (use others too when relevant). Write your file to /Users/Sarah/spokes/themes/$slug.md" \
    --model sonnet --allowedTools "Read" "Write" "Glob" "Grep" "Bash(.venv/bin/python tools/find.py:*)" \
    --permission-mode acceptEdits --add-dir "$HOME/spokes" > "logs/theme_$slug.log" 2>&1 &
done < tools/themes.tsv
wait
ls -la themes
