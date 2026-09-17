---
name: site-personality
description: Add fun, personality, and interactivity to kjryan2004-arch.github.io (Kiefer Ryan's personal site) while keeping it professional enough for a job search. Use this whenever the user asks to make the site "more fun," "more interactive," "spice it up," "add some personality," "add an easter egg," "make people stick around," or anything in that spirit — even if they don't name a specific feature. Do NOT use this for routine content edits like fixing a typo, updating a job title, or adding a new experience entry — those stay simple and don't need this lens.
---

# Site personality

This site is a hiring-facing portfolio, not a toy. The goal here is real: make it fun and
interactive enough that a visitor stays and remembers it, without ever tipping into "cute but
unhireable." Every change made under this skill has to hold both of those at once.

## Before doing anything: propose, don't just build

Fun and personality are personal — what feels right to one person feels cringe to another. So
whenever this skill triggers, **come with 2-3 concrete concept options** and get sign-off on
the specific idea (and roughly how it'll look/behave) before writing code. This matches how
this project already likes to work: content and design get confirmed before they're built and
published, not after.

A concept pitch should be one or two sentences each, concrete enough to picture — not "we could
add some animations" but "a subtle highlight that follows your cursor along the experience
timeline" or "a hover-triggered stat card that flips to show the story behind the number."

## The two kinds of "fun" this site wants

1. **Motion and micro-interactions** — small reactions to scroll, hover, or click that make the
   site feel alive without being loud. Think: something shifting subtly on hover, a reveal on
   scroll, a transition that feels considered.
2. **A small interactive widget tied to marketing/analytics** — something a visitor actually
   *does*, not just watches, and that doubles as a quiet demonstration of the skills on the
   resume (reading data, building something people engage with). Default toward this over a
   generic unrelated game or quiz, since it does double duty: entertaining *and* on-brand.
   Examples in that spirit: a mini interactive chart the visitor can toggle/filter, a
   "guess the metric before you scroll" reveal, something built from the real stats already on
   the site (3,500+ subscribers, 300% growth, etc.) rather than invented numbers.

An easter egg (something only found if a visitor pokes around — a hidden animation, a
keyboard-shortcut surprise, a wink tied to the mascot detail already on the site) is a good
lightweight option too, precisely because it costs nothing for the visitor who never finds it.

## The one rule that can't bend: mobile

Whatever gets added has to work and look good on a phone-sized viewport. Check this before
calling anything done — resize down or use device emulation, don't just eyeball the desktop
view. A fun feature that's unusable or broken on mobile is a worse outcome than not adding it.

## Softer goals — use judgment, but keep these in mind

- **Credibility at a glance.** Someone skimming for ten seconds should still read this as "a
  serious candidate," not "someone who prioritized cute over competent."
- **Load speed.** Nothing so heavy (autoplay video, big animation libraries, huge assets) that
  the site feels sluggish, especially on mobile data.
- **Resume info stays easy to find.** Fun additions should sit alongside the substance
  (experience, education, contact), never bury or distract from it.

These aren't hard blockers the way mobile is — they're things to weigh when a concept pitch is
borderline, not reasons to reject every idea that has *any* cost on one of them.

## What a bad result looks like here (avoid these specifically)

- **Generic AI-template slop.** This is the exact thing the site was redesigned away from once
  already — gradient hero blobs, glowing pill badges, cookie-cutter SaaS card-with-shadow
  layouts. New elements should extend the site's existing visual language (Fraunces serif +
  Inter body + IBM Plex Mono labels, the ink/paper/rust-accent palette, the editorial/timeline
  layout — see `index.html`), not introduce a different aesthetic on top of it.
- **Gimmick for gimmick's sake.** If a feature doesn't have a clear answer to "why would this
  make someone want to stay," it's filler, not fun. Confetti, spinning logos, and "look, it's
  interactive!" widgets with no point fail this test even if they're technically impressive.
- **Janky motion.** Animations that stutter, lag, or feel cheap read as unpolished, which
  undercuts credibility more than having no animation at all.

## Implementation notes

- This is a static site with no build step (plain HTML/CSS/JS served directly from GitHub
  Pages) — keep additions in that same vanilla style, no frameworks or bundlers.
- Reuse the CSS custom properties already defined in `index.html` (`--ink`, `--paper`,
  `--accent`, etc.) and the existing font stack rather than introducing new ones, so new
  features feel native to the page instead of bolted on.
- After building, actually resize the browser (or use responsive/device-emulation view) to
  confirm the new feature works at phone width before considering the work done.
- Follow the project's standing habit: walk the user through what's about to change and confirm
  before committing and publishing to GitHub Pages.
