---
name: site-qa
description: Run an automated regression check on kjryan2004-arch.github.io (Kiefer Ryan's personal site) — clicks every interactive element in a real headless browser and verifies images, the skills filter, and the Selected Work lightbox all actually work. Use before publishing any change to index.html, after adding a new Selected Work entry (add-case-study), after a layout/CSS change, or whenever the user asks to "test the site," "make sure nothing broke," or "check it works" before it goes live. This is a verification step, not a content-authoring one — pair it with add-case-study or direct edits, don't use it standalone to make changes.
---

# Site QA: automated regression check

This is a static HTML/CSS/JS site with no test suite and no build step, so
"does it still work" can only be answered by actually driving a browser.
Screenshotting the rendered page is not enough — this project has a real
history of a card that *looked* fine but whose click handler was silently
broken. This skill clicks things and reads back what actually happened in the
DOM.

## Why a real browser instead of eyeballing the HTML

Every interactive feature on this site (the skills filter, the Selected Work
lightbox, the case-study cross-links) is vanilla JS wired up with
`querySelectorAll` and event listeners. A typo in a selector, a class name
that got renamed in the CSS but not the JS, or a `data-project` value that
doesn't match a key in the `projects` object all fail *silently* — no console
error a casual look would catch. The only reliable check is: open it, click
it, read the resulting DOM state back out.

## How this project drives a headless browser

No `chromium-cli` or Playwright is installed in this environment. What does
work, reliably: **headless Microsoft Edge + raw Chrome DevTools Protocol over
websockets.** `websocket-client` may need installing once (`pip install
websocket-client`).

```powershell
# Launch — the --remote-allow-origins flag is required, or the websocket
# handshake gets rejected with a 403. This is not optional.
Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" `
  -ArgumentList "--headless","--disable-gpu","--remote-debugging-port=9333", `
    "--remote-allow-origins=*","--window-size=1400,2400","http://localhost:8123/" `
  -PassThru | Select-Object -ExpandProperty Id
Start-Sleep -Seconds 2
$json = (Invoke-WebRequest -Uri "http://localhost:9333/json" -UseBasicParsing).Content | ConvertFrom-Json
($json | Where-Object { $_.url -eq "http://localhost:8123/" }).webSocketDebuggerUrl
```

That prints a `ws://localhost:9333/devtools/page/<id>` URL — pass it to
`reference/regression_test.py`.

The site needs to actually be served (relative image paths won't resolve from
`file://`): `python -m http.server 8123` from the repo root, in the
background, before launching the browser.

## Running it

```
python reference/regression_test.py "ws://localhost:9333/devtools/page/<id>"
```

This discovers and exercises, dynamically (no hardcoded project names, so it
stays valid as `add-case-study` adds more entries):
- Every `.work-feature` card — clicks it, confirms the lightbox opens with a
  matching title
- Every `[data-open-project]` cross-link (like the Kroger → Air Care case
  link) — same check
- Every `[data-skill]` tag — clicks it, confirms at least the clicked tag's
  own matching timeline entries got `.match`, then clicks again and confirms
  it clears
- Keyboard access — focuses a `.work-feature` and fires a synthetic `Enter`
  keydown, confirms the lightbox still opens (these are `role="button"` divs,
  not real `<button>` elements, so this isn't free)
- Every `<img>` on the page — confirms `naturalWidth > 0` after load; reports
  the `src` of anything broken

It prints a pass/fail line per check plus a final broken-image list. Fix
anything it flags before treating a change as done.

## Mobile check

Interactive checks above run at desktop width. Separately re-launch Edge at
`--window-size=390,844` and screenshot the sections that changed
(`Page.captureScreenshot` over the same CDP connection) — read the resulting
PNG back to actually look at it. Don't skip this for anything that touches
layout; this site has real CSS (`.work-feature`, `.about-photos`,
`.stats-layout`) that reflows completely at phone width via `@media`
breakpoints, and that reflow has broken silently before.

## Cleanup

Always kill the headless browser and stop the local server when done —
`Stop-Process` on the Edge process, and stop the `http.server` background
job. Delete any screenshot files written to the repo root/working
directory before finishing — they're scratch output, not site content, and
have been accidentally left behind (and caught in `git status`) before.
