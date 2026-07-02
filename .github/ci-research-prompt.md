You are running non-interactively in GitHub Actions CI for the ReachOut corporate sponsor-finding project. Read `reachout-context.md` and `.claude/skills/find-sponsors/SKILL.md` in this repo for full context on ReachOut's mission, scope rules, and the fit-scoring rubric — treat them as the standing brief.

Perform steps 1–5 of that skill's process only:
1. Load `data/prospects.csv` (and `data/excluded.csv` if it exists) to see what's already tracked.
2. Search the web — both news mode and directory mode as described in the skill — for new corporate sponsorship prospects.
3. Verify each candidate has a real London and/or Manchester presence per the scope rules.
4. Score fit 1–5 using the rubric.
5. Update `data/prospects.csv` in place: append new rows, update existing rows only when you have materially new evidence (dedupe by company name, case-insensitive), keeping the CSV well-formed (same columns, properly quoted fields).

Do **not** attempt any Google Drive/Sheets operations — that integration isn't available in this environment. A separate script (`scripts/sync_to_sheet.py`) handles syncing new rows to the canonical Google Sheet after you finish, and it only ever appends new companies — it never overwrites or replaces existing sheet rows.

Do **not** run `git commit` or `git push` — the calling workflow does that after you finish.

When done, leave `data/prospects.csv` updated on disk and print a short plain-text summary of what you added or changed (or state plainly if nothing new was found this run). This summary will appear in the CI logs.
