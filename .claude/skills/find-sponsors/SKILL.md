---
name: find-sponsors
description: Research and log new corporate sponsorship prospects for ReachOut (youth mentoring charity, London & Manchester). Use when asked to find sponsors, find CSR partners, research corporate partnership leads, or update the ReachOut prospect list.
---

# Find corporate sponsors for ReachOut

This skill is the "agent": a repeatable research pass that finds corporate sponsorship prospects for ReachOut and keeps a running, de-duplicated list of them. It is triggered manually (ask Claude to run it, or invoke `/find-sponsors`) — it is not on an automatic schedule. Run it as often as you like; each run should only add genuinely new information.

Read `reachout-context.md` (repo root) first — it defines who ReachOut is, the fit-scoring priorities, and the scope rules (London/Manchester presence required, no sector or size restriction). Don't re-derive that context from scratch each run; treat it as the standing brief, and re-read it in case it's been edited since your training/last run.

## Process

1. **Load current state.** Read `data/prospects.csv`. Note every company already listed (case-insensitive match) and its `status`. If `data/excluded.csv` exists, read it too — never add a company listed there. The goal each run is *new* leads or *new evidence* on existing leads, not repeats.

2. **Search in two modes, both required:**
   - **News mode**: look for recent (favor last ~90 days, but up to ~18 months is fine) announcements of increased charitable giving, new CSR budgets/foundations, "charity of the year" or charity-partner selection processes, and CSR strategy launches, filtered to companies with a London and/or Manchester presence and any youth/education/social-mobility/mentoring angle.
   - **Directory mode**: look for corporations — regardless of whether they're in the news right now — that already run CSR/foundation programmes focused on youth development, mentoring, or social mobility and are based in or have a major office in London and/or Manchester. Rotate across sectors run over run (financial/professional services, law, tech, retail, real estate, sport/leisure, media, retail/consumer, construction/property) so repeated runs don't just resurface the same few well-known names.
   - Use WebSearch for discovery and WebFetch to confirm specifics (office locations, programme details, dates) on promising hits. Don't fabricate details you can't source — if a claim can't be verified with a URL, leave it out or mark it as unverified in the rationale.

3. **For each new candidate**, verify it clears the scope rules in `reachout-context.md` (real London/Manchester presence; any sector/size is fine), then capture:
   - `company`, `sector`, `location` (London / Manchester / Both / National-UK-with-London-or-Manchester-office)
   - `csr_focus_area` — plain description of their giving/CSR angle
   - `evidence_summary` — one or two sentences citing what you found
   - `source_url` — must be a real URL from your search/fetch
   - `date_found` — today's date
   - `fit_score` (1–5, see rubric below)
   - `rationale` — why that score, one sentence
   - `suggested_next_step` — concrete action (e.g. "Apply via open charity-partner call before [date]", "Contact via corporate foundation enquiry form", "Reference their [named programme] when pitching mentoring model fit")
   - `status` — `New Lead` for anything you're adding for the first time

4. **Fit-score rubric** (apply consistently; store the number, not the label):
   - **5** — Live/active youth-mentoring or social-mobility CSR programme, London/Manchester presence, AND either a multi-year commitment or an open/upcoming partner-selection process right now.
   - **4** — Strong CSR in youth/education/social-mobility generally (not necessarily mentoring-specific), London/Manchester presence, and/or a recent (≤18mo) increase in giving commitment.
   - **3** — General CSR/community-giving programme with some youth angle, or a strong youth programme whose London/Manchester presence is real but secondary (e.g. one office, not HQ).
   - **2** — CSR presence but weak/no youth angle, or a youth-focused funder/intermediary rather than a direct corporate (still worth logging as a channel contact, but flag it as such in the rationale).
   - **1** — Weak fit; only log if there's a specific reason to keep an eye on them.

5. **Update `data/prospects.csv`**: append new rows; for existing companies where you found materially new evidence, update their row in place (keep the earliest `date_found`, update `evidence_summary`/`source_url`/`fit_score` if it changed, and note what changed in the commit message) rather than creating a duplicate row.

6. **Snapshot to Google Drive.** The connected Google Drive integration can create files but cannot edit an existing one in place. So: search Drive (`search_files`, query like `title contains 'ReachOut Corporate Sponsor Prospects'`) to see what's there already, then create a new file titled `ReachOut Corporate Sponsor Prospects — YYYY-MM-DD` from the current full CSV content (`create_file`, `contentMimeType: text/csv`, leave conversion enabled so it lands as a native Google Sheet). Tell the user this is a snapshot and that `data/prospects.csv` in the repo is the canonical, continuously-updated source — old dated snapshots can be deleted manually in Drive if they pile up.

7. **Commit and push** the updated `data/prospects.csv` (and `data/excluded.csv` if touched) to the current branch with a message summarizing what was added/changed (e.g. "Add 4 new sponsor prospects: Company A, B, C, D").

8. **Report back to the user**: list what's new this run (company, one-liner, fit score, source), and call out anything time-sensitive (open applications, deadlines) at the top. If nothing new was found, say so plainly rather than padding the list with low-fit filler.

## Quality bar

- Every row needs a real, checkable `source_url`. No source, no row.
- Don't lower the bar just to hit a target count — a run that finds 2 solid leads is better than one that pads to 10 with weak fits.
- Keep `location` honest: "Both" only if the company genuinely has a major presence in both cities, not just a national UK footprint.
