# ReachOut: organizational context for sponsor research

This file grounds the sponsor-finding agent (`.claude/skills/find-sponsors/`) in who ReachOut actually is, so fit-scoring stays anchored to reality rather than generic "any charity" criteria.

## Who ReachOut is

ReachOut is a national mentoring and education charity working in under-resourced areas of **London, Greater Manchester, and Liverpool**. Since this project's brief is scoped to London and Manchester, the agent should only surface corporate prospects with a real presence (HQ or major office) in those two cities, even though ReachOut itself also operates in Liverpool.

- **Model**: schools-based collective mentoring plus group activities, delivered largely by trained volunteer mentors drawn from the local community (including corporate volunteers).
- **Age range**: 9–18, with particular focus on 9–14 year-olds constrained by circumstance.
- **Outcomes**: builds socio-emotional skills — empathy, responsibility, problem solving, initiative, teamwork, emotion management.
- **Registered charity**: England & Wales, no. 1096492 ("REACHOUT YOUTH").
- Website: https://www.reachoutuk.org/ · About: https://www.reachoutuk.org/about-reachout/

## What makes a corporate partner a good fit

The best prospects share ReachOut's actual delivery model — local, school-based, mentoring-driven, socio-emotional-skills-focused — not just "does CSR" in the abstract. In rough priority order:

1. **Existing youth mentoring / social mobility CSR programme** with a London and/or Manchester office actively participating (strongest signal — proves the giving muscle and delivery model already exist).
2. **Recent (last ~18 months) increase in CSR/charitable-giving commitment** — new foundation, multi-year pledge, larger budget — with any youth, education, or social mobility angle, even if not mentoring-specific.
3. **Active or upcoming charity-partner selection process** (e.g. "charity of the year" applications, RFPs) — these are time-sensitive and worth flagging even if the historical focus area isn't a perfect match, since the field is open.
4. **Employee volunteering culture** (paid volunteering days, mentoring schemes) that could plausibly resource ReachOut's mentor pipeline directly.
5. General CSR/community programmes with no clear youth angle are weak fits — note them only if there's a specific reason (e.g. major Manchester employer with no current youth partner).

## Explicit scope rules

- **Location**: company must have an HQ or a genuine major office/operational presence in London and/or Manchester. A UK-wide programme that happens to touch these cities via a named local partner counts; a company with only a registered address and no real presence does not.
- **No sector restriction** — cast a wide net (financial/professional services, law, tech, retail, real estate, sport/leisure, media, etc. are all in scope).
- **No size restriction** — large FTSE-listed corporates and smaller/mid-size firms are both in scope; a smaller company with a proven, multi-year local-youth-charity partnership (e.g. matching ReachOut's own scale) can be as good a fit as a giant with a huge but generic CSR budget.
- **No pre-existing exclusion list** — as of the first run (July 2026) there is no known list of companies ReachOut has already approached or ruled out. If/when one exists, it should live in `data/excluded.csv` and the agent should check against it before adding a company.
