# ReachOut Corporate Sponsor Finder

A repeatable research agent that finds and tracks corporate sponsorship prospects for [ReachOut](https://www.reachoutuk.org/), a youth mentoring charity working in under-resourced areas of London and Manchester (also Liverpool, out of scope for this project).

It looks for two kinds of signal:
- **News**: recent announcements of increased charitable giving, new CSR budgets/foundations, or charity-partner selection processes at companies with a London/Manchester presence.
- **Directory**: companies — in the news or not — that already run CSR programmes focused on youth development, mentoring, or social mobility, and have an HQ or major office in London and/or Manchester.

## How it runs

**Automatically, every week**, via GitHub Actions (`.github/workflows/find-sponsors.yml`) — no Claude session needs to be open. It:
1. Runs the research pass headlessly (Claude Code CLI + `ANTHROPIC_API_KEY`), updating `data/prospects.csv`.
2. Appends any new prospects to the canonical Google Sheet (`scripts/sync_to_sheet.py`) — **append-only**: existing rows are never overwritten or replaced, so the sheet is a permanent, growing record across every run.
3. Commits and pushes the updated CSV back to the repo.

You can also trigger it **manually** any time — either click "Run workflow" on `find-sponsors.yml` in the GitHub Actions tab, or, in an interactive Claude Code session, ask "Find new sponsor prospects for ReachOut" / `/find-sponsors`.

**Required one-time setup** (see [Setup](#setup-required-secrets)) — the schedule won't do anything useful until these are in place.

## Repo structure

```
reachout-context.md                    Who ReachOut is, fit-scoring rubric, scope rules
.claude/skills/find-sponsors/SKILL.md  The agent's step-by-step research process
.github/workflows/find-sponsors.yml    Weekly (+ manual) CI schedule
.github/ci-research-prompt.md          Prompt used for the headless CI run
scripts/sync_to_sheet.py               Append-only sync of new prospects to the Google Sheet
data/prospects.csv                     The running, de-duplicated prospect list (source of truth)
data/excluded.csv                      (create when needed) companies to skip, e.g. already approached/ruled out
```

## `data/prospects.csv` schema

| column | meaning |
|---|---|
| `company` | Company / organization name |
| `sector` | Industry |
| `location` | `London`, `Manchester`, `Both`, or a national-UK company with a London/Manchester office |
| `csr_focus_area` | What their giving/CSR is about |
| `evidence_summary` | What was found and why it's relevant |
| `source_url` | Where it came from — every row has one, nothing is included without a checkable source |
| `date_found` | When it was first logged |
| `fit_score` | 1–5, see rubric in `reachout-context.md` |
| `rationale` | One-line reason for the score |
| `suggested_next_step` | Concrete action for the partnerships team |
| `status` | `New Lead`, or updated manually as outreach progresses (e.g. `Contacted`, `In Discussion`, `Declined`) |

The first seeded run (2026-07-02) found 13 leads, including one time-sensitive one: **Société Générale UK is currently running an open selection process for its next 5-year charity partner (2026–2031)** — worth reviewing soon.

## The Google Sheet

**One sheet, permanently growing.** [ReachOut Corporate Sponsor Prospects](https://docs.google.com/spreadsheets/d/1GxjJs3GxXpvWKnTGqPnVoCg4eFTi2HZVOnBJehfEAnc/edit) already holds the first 13 seeded leads. Every future run only *appends* companies not already in it — nothing is ever overwritten, replaced, or removed by the sync script. `data/prospects.csv` in this repo is the working copy the agent reads/writes each run; the Sheet is the durable, shareable record built from it. (You can rename the sheet's title in Drive if you want to drop the date from it — that's just cosmetic.)

## Setup required (secrets)

The CI workflow can't run until these are added in **GitHub repo Settings → Secrets and variables → Actions**:

| Name | Type | What it is |
|---|---|---|
| `ANTHROPIC_API_KEY` | Secret | An API key from [console.anthropic.com](https://console.anthropic.com) (needs billing enabled). Powers the weekly headless research run — usage is pay-per-call, roughly one run/week, so cost should be minimal and predictable. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Secret | Full JSON key of a Google Cloud service account (see below) with **Editor** access to the target Sheet. |
| `GOOGLE_SHEET_ID` | Variable (not secret — it's just an ID) | `1GxjJs3GxXpvWKnTGqPnVoCg4eFTi2HZVOnBJehfEAnc` — the ID from the Sheet's URL, unless you'd rather point it at a different sheet. |

**To create the Google service account** (one-time, in [Google Cloud Console](https://console.cloud.google.com)):
1. Create or pick a project, then enable the **Google Sheets API** for it.
2. Create a **Service Account** (IAM & Admin → Service Accounts).
3. Create a JSON key for it and download it — this is the value for `GOOGLE_SERVICE_ACCOUNT_JSON` (paste the whole file contents in as the secret).
4. Open the target Google Sheet, click Share, and give the service account's email (looks like `name@project-id.iam.gserviceaccount.com`) **Editor** access — without this the sync will fail with a permissions error.

**Important**: the `schedule` trigger in GitHub Actions only fires for workflows that exist on the repository's **default branch**. Until this branch is merged, the weekly schedule is dormant — `workflow_dispatch` (manual "Run workflow" button) works on any branch in the meantime, so you can test the full pipeline once secrets are set without waiting for a merge.

## Updating scope

- To stop re-surfacing companies you've already approached or ruled out, create `data/excluded.csv` (same `company` column) — the skill checks it before adding anything.
- To change geographic or sector scope, edit `reachout-context.md` — the skill reads it as its standing brief.
- To change the cadence, edit the `cron:` line in `.github/workflows/find-sponsors.yml`.
