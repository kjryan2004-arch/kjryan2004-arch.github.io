# Drives the live site over Chrome DevTools Protocol and exercises every
# interactive element dynamically (no hardcoded project/skill names, so this
# stays valid as Selected Work grows). Prints PASS/FAIL per check and a
# final broken-image list. Exit code is 1 if anything failed.
#
# Requires: pip install websocket-client
# Usage: python regression_test.py "ws://localhost:9333/devtools/page/<id>"

import json
import sys
import websocket

if len(sys.argv) < 2:
    print("usage: regression_test.py <websocket-debugger-url>")
    sys.exit(1)

WS_URL = sys.argv[1]
ws = websocket.create_connection(WS_URL)
_id = 0
failures = []

def send(method, params=None):
    global _id
    _id += 1
    ws.send(json.dumps({"id": _id, "method": method, "params": params or {}}))
    while True:
        r = json.loads(ws.recv())
        if r.get("id") == _id:
            return r

def js(expr):
    r = send("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r["result"]:
        return {"__error__": r["result"]["exceptionDetails"]["text"]}
    return r["result"]["result"].get("value")

def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not condition else ""))
    if not condition:
        failures.append(label)

# ---- Work cards: click each, confirm the lightbox opens with a title ----
project_ids = js("Array.from(document.querySelectorAll('.work-feature')).map(e => e.dataset.project)")
for pid in project_ids:
    result = js(f"""
    (function(){{
      document.querySelector('.work-feature[data-project="{pid}"]').dispatchEvent(new MouseEvent('click', {{bubbles:true}}));
      var lb = document.getElementById('lightbox');
      var r = {{open: lb.classList.contains('open'), title: document.getElementById('lightbox-title').textContent}};
      document.getElementById('lightbox-close').click();
      return JSON.stringify(r);
    }})()
    """)
    data = json.loads(result) if isinstance(result, str) else result
    check(f"work-feature '{pid}' opens lightbox", data.get("open") and bool(data.get("title")), str(data))

# ---- Cross-links: [data-open-project] (e.g. Experience -> Selected Work) ----
cross_link_targets = js("Array.from(document.querySelectorAll('[data-open-project]')).map(e => e.dataset.openProject)")
for target in cross_link_targets:
    result = js(f"""
    (function(){{
      document.querySelector('[data-open-project="{target}"]').dispatchEvent(new MouseEvent('click', {{bubbles:true}}));
      var lb = document.getElementById('lightbox');
      var r = {{open: lb.classList.contains('open'), title: document.getElementById('lightbox-title').textContent}};
      document.getElementById('lightbox-close').click();
      return JSON.stringify(r);
    }})()
    """)
    data = json.loads(result) if isinstance(result, str) else result
    check(f"cross-link to '{target}' opens lightbox", data.get("open") and bool(data.get("title")), str(data))

# ---- Keyboard access: Enter on a work-feature (these are role=button divs) ----
if project_ids:
    result = js(f"""
    (function(){{
      var card = document.querySelector('.work-feature[data-project="{project_ids[0]}"]');
      card.focus();
      card.dispatchEvent(new KeyboardEvent('keydown', {{key:'Enter', bubbles:true}}));
      var lb = document.getElementById('lightbox');
      var r = {{open: lb.classList.contains('open')}};
      document.getElementById('lightbox-close').click();
      return JSON.stringify(r);
    }})()
    """)
    data = json.loads(result) if isinstance(result, str) else result
    check("keyboard Enter opens work-feature lightbox", data.get("open"), str(data))

# ---- Skills filter: click each tag, confirm toggle-on then toggle-off ----
skills = js("Array.from(document.querySelectorAll('#skill-tags .tag')).map(e => e.dataset.skill)")
for skill in skills:
    result = js(f"""
    (function(){{
      var tag = document.querySelector('[data-skill="{skill}"]');
      tag.dispatchEvent(new MouseEvent('click', {{bubbles:true}}));
      var activeAfterOn = tag.classList.contains('active');
      tag.dispatchEvent(new MouseEvent('click', {{bubbles:true}}));
      var activeAfterOff = tag.classList.contains('active');
      return JSON.stringify({{on: activeAfterOn, offCleared: !activeAfterOff}});
    }})()
    """)
    data = json.loads(result) if isinstance(result, str) else result
    check(f"skill tag '{skill}' toggles on/off", data.get("on") and data.get("offCleared"), str(data))

# ---- Every image on the page actually loaded ----
result = js("""
(function(){
  var imgs = Array.from(document.querySelectorAll('img'));
  var broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.src);
  return JSON.stringify({total: imgs.length, broken: broken});
})()
""")
data = json.loads(result) if isinstance(result, str) else result
check(f"all {data.get('total')} images loaded", len(data.get("broken", [])) == 0, str(data.get("broken")))

ws.close()

print()
if failures:
    print(f"{len(failures)} check(s) failed:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("All checks passed.")
