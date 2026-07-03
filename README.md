# ReachOut Corporate Sponsor Finder

A repeatable research agent that finds and tracks corporate sponsorship prospects for [ReachOut](https://www.reachoutuk.org/), a youth mentoring charity working in under-resourced areas of London and Manchester (also Liverpool, out of scope for this project).

It looks for two kinds of signal:
- **News**: recent announcements of increased charitable giving, new CSR budgets/foundations, or charity-partner selection processes at companies with a London/Manchester presence.
- **Directory**: companies — in the news or not — that already run CSR programmes focused on youth development, mentoring, or social mobility, and have an HQ or major office in London and/or Manchester.

## How it runs

**Manual trigger only, done here in Claude** — there's no automatic schedule and no separate infrastructure to run or pay for. Whenever you want fresh research, ask in this Claude Code session:

> "Find new sponsor prospects for ReachOut" / `/find-sponsors`

Each run reads `data/prospects.csv` first so it only adds genuinely new leads or new evidence, updates the CSV, commits and pushes it, and gives you a ready-to-paste block of just the new rows to drop into the Google Sheet (see [The Google Sheet](#the-google-sheet) below for why it's a paste-in rather than automatic).

## Repo structure

```
reachout-context.md                    Who ReachOut is, fit-scoring rubric, scope rules
.claude/skills/find-sponsors/SKILL.md  The agent's step-by-step research process
scripts/sync_to_sheet.py               Optional: direct append-only Sheets API sync (see below)
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

**One sheet, permanently growing, never replaced.** [ReachOut Corporate Sponsor Prospects](https://docs.google.com/spreadsheets/d/1GxjJs3GxXpvWKnTGqPnVoCg4eFTi2HZVOnBJehfEAnc/edit) already holds the first 13 seeded leads. `data/prospects.csv` in this repo is the working copy the agent reads/writes each run; the Sheet is the durable, shareable copy for people who don't want to look at GitHub.

The connected Google Drive tools can only *create* files, not edit an existing sheet in place, so keeping it as one accumulating sheet needs one of two approaches:

- **Default (no setup)**: after each manual run, Claude gives you a small block of just the new/changed rows to paste into the bottom of the existing sheet yourself.
- **Optional (one-time setup)**: `scripts/sync_to_sheet.py` uses the real Google Sheets API to append new rows automatically — no copy-paste needed, and it never touches existing rows. To enable it: create a Google Cloud service account with the Sheets API enabled, share the Sheet with its email as Editor, and hand Claude the JSON key + the Sheet ID (`1GxjJs3GxXpvWKnTGqPnVoCg4eFTi2HZVOnBJehfEAnc`) to use for that session. Ask Claude to set this up if you'd rather not paste rows in by hand.

## Updating scope

- To stop re-surfacing companies you've already approached or ruled out, create `data/excluded.csv` (same `company` column) — the skill checks it before adding anything.
- To change geographic or sector scope, edit `reachout-context.md` — the skill reads it as its standing brief.
