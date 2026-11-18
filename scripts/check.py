#!/usr/bin/env python3
"""Validate data.json before every push. Exit 1 on any problem."""
import json, re, sys, pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "data.json"
errs = []
try:
    d = json.loads(p.read_text())
except Exception as e:
    sys.exit(f"FAIL data.json is not valid JSON: {e}")

for k in ["updated", "intro", "book", "song", "shipped", "links", "thisWeek", "next"]:
    if k not in d:
        errs.append(f"missing key: {k}")
for t in ["book", "song"]:
    for i in d.get(t, {}).get("items", []):
        if i.get("status") not in ("live", "wip", "next"):
            errs.append(f"{t}: bad status {i.get('status')!r} on {i.get('label')!r}")
        if "link" in i and not i["link"].startswith("https://"):
            errs.append(f"{t}: link not https: {i['link']}")

text = p.read_text()
# Julie-facing rules: no em/en dashes, no money, no private plans, no vendor names, no Claude links
banned = {
    "—": "em dash", "–": "en dash",
    r"\$\d": "dollar amount", r"\bstretch\b": "stretch goal", r"mega.?fan": "mega fans",
    r"\bPodMatch\b": "PodMatch (not approved)", r"SongTools|Members Media": "playlist vendor name",
    r"claude\.ai": "Claude artifact link", r"\bPRIVATE\b": "private file",
    r"\bbandwidth\b": "bandwidth note", r"5,000|1,000 mega": "private target",
}
for pat, why in banned.items():
    if re.search(pat, text, re.I):
        errs.append(f"banned content: {why}")

if errs:
    print("FAIL"); [print(" -", e) for e in errs]; sys.exit(1)
print(f"OK  updated={d['updated']}  book={len(d['book']['items'])}  song={len(d['song']['items'])}  shipped={len(d['shipped'])}")
