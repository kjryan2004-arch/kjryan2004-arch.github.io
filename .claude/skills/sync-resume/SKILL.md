---
name: sync-resume
description: Compare a newly-provided resume PDF against the Experience, Education, Involvement, and Certifications content already on kjryan2004-arch.github.io (Kiefer Ryan's personal site) and reconcile any differences. Use whenever a new resume file is downloaded or handed over and the user wants the site to reflect it, or asks "does my site match my resume," "update my site from my resume," or "is my site up to date." Do NOT use this for one-off manual edits the user explicitly describes themselves (e.g. "change my Bob Evans dates to X") — that's a direct edit, not a reconciliation.
---

# Sync the site against a new resume

The site's Experience/Education/Involvement/Certifications content and the
student's resume PDF are two independently-edited sources of the same facts.
They drift. This skill's job is to find every place they disagree and settle
each one explicitly — never to silently prefer one source over the other.

## Real precedent from this project

The first time this came up: the site said Lead Advisor Consulting was
"January 2025 — Present," but a newly-downloaded resume said "January –
August 2025." Rather than guessing, the resolution was to ask which was
current, and the answer was "the 2026 resume is newest, use that" — which
became the standing rule below. Separately, that same resume surfaced a
**Certifications** section (three Circana Unify+ credentials) that didn't
exist on the site at all yet — not a conflict, just missing content that
needed adding.

Expect both kinds of drift: **contradictions** (a date, a bullet, a detail
that disagrees) and **additions** (something real on the resume that never
made it to the site, or something on the site — like the site's more
detailed Skills & Tools tag list — that's intentionally richer than the
resume's terser bullet list and should probably stay that way).

## Steps

**1. Extract the resume's text.** Read the PDF directly — it's almost always
a real text layer (unlike the project-deck PDFs `add-case-study` deals with,
which are usually flattened slide images).

**2. Read the site's current content.** Pull the `#experience` and
`#education` sections of `index.html` — dates, bullets, org names,
certifications, skills tags.

**3. Diff them section by section**, and sort every difference into one of
three buckets:
- **Contradiction** — same fact, different value (a date range, a bullet's
  numbers, a role title). Flag it explicitly; do not silently pick a side.
- **Resume has it, site doesn't** — likely a real gap (see the
  Certifications example above). Default toward adding it.
- **Site has it, resume doesn't** — often intentional richness (the site's
  Skills & Tools tags are more granular than a resume bullet, and several
  entries carry a quantified `work-achievement` stat that a resume bullet
  form can't hold). Don't delete site content just because the resume is
  terser — only flag it if it looks like the resume corrected something the
  site got wrong.

**4. For every contradiction, ask which source wins** — don't assume. The
established default once asked is **the newest resume wins**, but confirm
that's still true rather than hard-coding it forever; resumes can also be
stale or mid-edit.

**5. Apply only the confirmed changes.** Keep the site's existing structure
and tone (the `t-head`/`work-achievement`/logo-chip patterns already in
place) — this is a content sync, not a redesign.

**6. Run `site-qa` after, if the edits touched anything beyond plain text** —
a date/bullet-only change doesn't need it, but if a role's `data-skills`
attribute or logo changed, verify the skills filter still matches correctly.

**7. Confirm before publishing**, per this project's standing habit.
