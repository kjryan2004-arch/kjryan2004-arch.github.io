---
name: add-case-study
description: Turn a project deck, report, or presentation (PDF or PPTX) into a new Selected Work entry on kjryan2004-arch.github.io (Kiefer Ryan's personal site). Use whenever the user hands over a new file to "add to my portfolio," "add to my site," "put this in Selected Work," or drops a project PDF/deck in Downloads and asks it to become part of the website. Also use when asked to update or re-crop an existing Selected Work entry's images or achievement stat. Do NOT use this for plain content edits (fixing a typo, updating a date, adding an Experience bullet) — those are simple text edits, not a new case study.
---

# Add a case study to Selected Work

This turns a source document (almost always a PDF export of slides) into a new
entry in the `#work` section of `index.html`: two real images, a quantified
achievement stat, and a lightbox entry with achievement bullets — following
the exact pattern already used for the Air Care, Myers's Rum, Rios, and LO
entries.

## The one rule that matters most: never invent a number

Every `work-achievement-num` and every lightbox achievement bullet must trace
back to something actually printed in the source document — a percentage, a
dollar figure, a ranking, a survey stat. If the deck doesn't have a clean
quantified result, use the strongest concrete claim it does make (e.g. "4
flavor SKUs shipped" beats a vague "successful project"). Pulling real numbers
out of the student's own work is the entire point of this skill — it's what
makes the site read as evidence instead of decoration.

## Steps

**1. Get the source file's full page/slide count and extract any embedded text first.**
Try text extraction before rendering images — it's far cheaper and slide decks
sometimes have a real text layer:

```python
import pymupdf  # pip install pymupdf Pillow if missing
doc = pymupdf.open(path)
print(doc.page_count)
for i, page in enumerate(doc):
    text = page.get_text().strip()
    if text:
        print(f"--- page {i+1} ---\n{text[:600]}")
```

If every page comes back empty, the deck is image-only (a Canva/Figma export)
and you'll need to render pages to look at them directly — see
`reference/render_pdf.py`.

**2. Find the cover slide and one strong supporting slide.**
The cover is almost always page 1. For the second image, look for whichever
slide states the clearest quantified result, objective, or recommendation —
not just the prettiest slide. Read a handful of candidate pages as images if
text extraction didn't already surface the number.

**3. Export both pages as compressed JPEGs into the repo.**
Use `reference/render_pdf.py` (it exports a specific page list to
`images/work/<slug>-1.jpg` / `<slug>-2.jpg`, sized to 1600px wide at quality
78 — that's what every existing entry uses, keeping each image well under
250KB). Pick a short `slug` for the project (e.g. `aircare`, `rum`).

**4. Check whether a real company/brand is involved, and get its logo.**
If the project names a real company (a client, a brand, a partner), source
its logo the way the existing four entries do it:
- Try Wikimedia Commons first via `https://commons.wikimedia.org/wiki/Special:FilePath/<Exact_File_Name>.svg` (or `.png`) — URL-encode apostrophes as `%27` and parentheses as `%28`/`%29`.
- If Commons doesn't have it, WebFetch the company's own homepage and ask for the header logo's image URL.
- Save into `images/logos/<name>.svg` or `.png`.
- **Before wiring it in, render it small** (see `site-qa`'s `reference/site_qa.py` screenshot helper, or a quick standalone HTML page + headless-browser screenshot) at the actual badge size (~28px tall) on both a light and dark background. A logo that's a complex lockup (emblem + wordmark + subtext, like Sazerac's) will turn into an illegible blob at that size — crop it down to just the wordmark with PIL first, the way `sazerac-word.png` was made from `sazerac.png`. A logo that's white-only needs the `on-dark` chip variant; nearly everything else should sit on the default light `.logo-chip` background regardless of what section it's in.
- No real company involved (an independent concept project) → skip the logo row and use a `work-org` label instead, like the LO entry does ("Independent Concept").

**5. Add the HTML card.** Inside `<section class="section work-section" id="work">`,
add a new block following this exact shape (copy an existing one and edit):

```html
<div class="work-feature reveal" data-project="SLUG" role="button" tabindex="0">
  <div class="work-feature-media">
    <img src="images/work/SLUG-1.jpg" alt="..." loading="lazy" />
    <span class="work-feature-view">View case →</span>
  </div>
  <div class="work-feature-body">
    <span class="work-feature-index mono">0N</span>
    <div class="work-feature-logos">
      <img class="logo-chip" src="images/logos/....svg" alt="..." />
    </div>
    <h3 class="work-feature-title">Project Title</h3>
    <div class="work-achievement">
      <span class="work-achievement-num">STAT</span>
      <span class="work-achievement-label">what it means, in plain language</span>
    </div>
    <p class="work-desc">One or two sentences on what was built/delivered.</p>
  </div>
</div>
```

Renumber every `work-feature-index` in the section sequentially afterward —
don't leave gaps or duplicates. The `:nth-child(even)` CSS rule automatically
flips the image to the right on alternating rows, so just append in order.

**6. Add the matching JS entry.** In the `<script>` block, find the `projects`
object inside the "Selected Work lightbox" IIFE and add a matching key:

```js
SLUG: {
  title: "Project Title — Context",
  images: ["images/work/SLUG-1.jpg", "images/work/SLUG-2.jpg"],
  achievements: [
    "First real, quantified achievement bullet",
    "Second one",
    "Third one"
  ]
}
```

**7. Verify it, don't assume it.** Run the `site-qa` skill (or at minimum its
click-test) against the new card before calling this done — confirm the card
opens the right lightbox, the achievement bullets render, and the images
actually loaded (`naturalWidth > 0`). This project has a real history of
silent image-path typos; don't skip this step.

**8. Confirm before publishing.** Per this project's standing habit, walk the
user through what was added and get a go-ahead before committing/pushing —
don't publish automatically just because a card was added successfully.
