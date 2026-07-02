# ReachOut Corporate Sponsor Finder

A repeatable research agent that finds and tracks corporate sponsorship prospects for [ReachOut](https://www.reachoutuk.org/), a youth mentoring charity working in under-resourced areas of London and Manchester (also Liverpool, out of scope for this project).

It looks for two kinds of signal:
- **News**: recent announcements of increased charitable giving, new CSR budgets/foundations, or charity-partner selection processes at companies with a London/Manchester presence.
- **Directory**: companies — in the news or not — that already run CSR programmes focused on youth development, mentoring, or social mobility, and have an HQ or major office in London and/or Manchester.

## How to run it

This is implemented as a Claude Code **skill**, not a background service — trigger it whenever you want fresh research:

> "Find new sponsor prospects for ReachOut" / `/find-sponsors`

Each run reads the existing prospect list first so it only adds genuinely new leads or new evidence, then commits the update to this repo and creates a snapshot Google Sheet. It is intentionally manual-trigger only for now (no fixed schedule) — see [Scheduling](#scheduling-later) if you want to automate it later.

## Repo structure

```
reachout-context.md                  Who ReachOut is, fit-scoring rubric, scope rules
.claude/skills/find-sponsors/SKILL.md  The agent's step-by-step research process
data/prospects.csv                    The running, de-duplicated prospect list (source of truth)
data/excluded.csv                     (create when needed) companies to skip, e.g. already approached/ruled out
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

## Google Sheet snapshots

The connected Google Drive integration can create files but can't edit one in place, so each run creates a **new, dated snapshot** (`ReachOut Corporate Sponsor Prospects — YYYY-MM-DD`) rather than updating one master sheet. Treat `data/prospects.csv` in this repo as the canonical, always-current list; use the Sheet snapshots for sharing with people who don't want to look at GitHub. Feel free to delete old snapshots from Drive periodically.

## Updating scope

- To stop re-surfacing companies you've already approached or ruled out, create `data/excluded.csv` (same `company` column) — the skill checks it before adding anything.
- To change geographic or sector scope, edit `reachout-context.md` — the skill reads it as its standing brief.

## Scheduling (later)

Right now this only runs when you ask. If you want it fully automatic (e.g. weekly), ask Claude to set that up — options are a recurring job in this Claude Code environment, or a scheduled workflow (e.g. GitHub Actions) that invokes the skill on a timer. Not configured yet by design, per initial scoping.
