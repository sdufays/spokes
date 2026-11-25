#!/bin/zsh
# Daily job (launchd): export new Spokes emails, fold them into the KB, rebuild, commit as Sarah, push.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
cd "$HOME/spokes" || exit 1
LOG="$HOME/spokes/logs/mail-daily.log"; mkdir -p logs
{
  echo "=== $(date) ==="
  git pull --rebase --quiet || echo "pull failed"
  before=$(ls "$HOME/spokes_sources/mail/messages" 2>/dev/null | sort)
  .venv/bin/python -W ignore tools/mail/scan_mail.py "$HOME/Library/Mail/V10" "$HOME/spokes_sources/mail" --since-days 3
  after=$(ls "$HOME/spokes_sources/mail/messages" | sort)
  comm -13 <(echo "$before") <(echo "$after") | sed "s|^|$HOME/spokes_sources/mail/messages/|" > logs/mail_new.txt
  if [ ! -s logs/mail_new.txt ]; then echo "no new Spokes email"; exit 0; fi
  echo "$(wc -l < logs/mail_new.txt) new emails"
  claude -p "Read /Users/Sarah/spokes/tools/mail/DAILY_BRIEF.md and follow it exactly." --model sonnet \
    --allowedTools "Read" "Write" "Edit" "Glob" "Grep" --permission-mode acceptEdits --add-dir "$HOME/spokes" "$HOME/spokes_sources/mail"
  .venv/bin/python -W ignore tools/build.py
  git add -A && git commit -q -m "Email update $(date +%Y-%m-%d)" && git push -q && echo "pushed"
} >> "$LOG" 2>&1
