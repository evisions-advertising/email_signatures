#!/usr/bin/env python3
"""Generate index.html (signature preview page with copy buttons) from signatures/.

Usage: python scripts/generate_preview.py
Run from the repository root. Deterministic: same input -> same output.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIGNATURES = ROOT / "signatures"
OUT = ROOT / "index.html"

HEAD = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Email Signature Preview</title><style>
body{font-family:Arial,sans-serif;background:#f4f4f4;margin:20px;}
h1{color:#F37021;} h2{color:#202020;border-bottom:3px solid #F37021;padding-bottom:4px;margin-top:36px;}
.grid{display:flex;flex-wrap:wrap;gap:16px;}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:14px;width:380px;box-shadow:0 1px 3px rgba(0,0,0,.08);display:flex;flex-direction:column;gap:12px;}
.copybtn{align-self:flex-start;background:#F37021;color:#fff;border:none;border-radius:6px;padding:8px 16px;font-size:13px;font-weight:bold;cursor:pointer;font-family:Arial,sans-serif;}
.copybtn:hover{background:#d95f15;} .copybtn.done{background:#3aa655;}
</style>
<script>
function copySig(btn){
  var sig = btn.closest('.card').querySelector('.sig');
  var range = document.createRange();
  range.selectNodeContents(sig);
  var sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
  var ok = false;
  try { ok = document.execCommand('copy'); } catch(e) {}
  sel.removeAllRanges();
  if (ok) {
    var orig = btn.textContent;
    btn.textContent = 'Copied! Paste into Gmail (Ctrl+V)';
    btn.classList.add('done');
    setTimeout(function(){ btn.textContent = orig; btn.classList.remove('done'); }, 2500);
  } else {
    btn.textContent = 'Copy failed - please select and copy manually';
  }
}
</script>
</head><body>"""


def main():
    teams = sorted(d for d in SIGNATURES.iterdir() if d.is_dir())
    cards_by_team = []
    total = 0
    for team in teams:
        files = sorted(team.glob("*.html"))
        if not files:
            continue
        cards = []
        for f in files:
            html = f.read_text(encoding="utf-8")
            m = re.search(r"<body>(.*)</body>", html, re.S)
            inner = m.group(1) if m else "<em>ERROR: could not extract</em>"
            cards.append(
                "<div class='card'><div class='sig'>%s</div>"
                "<button class='copybtn' onclick='copySig(this)'>Copy signature</button></div>" % inner
            )
            total += 1
        cards_by_team.append((team.name, cards))

    parts = [HEAD, "<h1>Email Signatures (%d)</h1>" % total]
    for name, cards in cards_by_team:
        parts.append("<h2>%s (%d)</h2><div class='grid'>" % (name, len(cards)))
        parts.extend(cards)
        parts.append("</div>")
    parts.append("</body></html>")

    OUT.write_text("\n".join(parts), encoding="utf-8", newline="\n")
    print("index.html generated: %d signatures" % total)


if __name__ == "__main__":
    main()
