"""Export every drawn figure in the study guide as a high-resolution PNG for outside editing.

Writes <out>/NN_<label>.png plus <out>/FIGURE-LIST.md describing where each image is used.
Usage: python3 tools/export_figures.py <out_dir>
"""
import json, os, re, subprocess, sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
SKIP_FILES = {"107-labeling.html"}  # worksheets are generated from the lesson figures
JS = r"""
const { chromium } = require(process.env.PW_PATH || 'playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch(); const page = await b.newPage({ deviceScaleFactor: 3 });
  for (const j of jobs) {
    await page.setContent(`<html><head><style>body{margin:0;background:#fff;font-family:Inter,sans-serif} svg text{font-family:Inter,sans-serif}</style></head><body><div id="w" style="display:inline-block;padding:16px;background:#fff">${j.svg}</div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await (await page.$('#w')).screenshot({ path: j.out });
  }
  await b.close();
})();
"""
defs = (SRC / "defs.svg").read_text()
jobs, rows, n = [], [], 0
def slug(s): return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")[:60]
for f in sorted(p for p in SRC.glob("*.html") if p.name[0].isdigit() and p.name not in SKIP_FILES):
    soup = BeautifulSoup(f.read_text(), "html.parser")
    for svg in soup.find_all("svg"):
        if svg.find_parent(class_="frq-part"):
            continue  # blank graph grids for student answers
        art = svg.find_parent("div", class_="art")
        fig = svg.find_parent("figure")
        cap = fig.find("figcaption").get_text(" ", strip=True) if fig and fig.find("figcaption") else ""
        if art and art.get("data-ai") and not art["data-ai"].startswith("fig-"):
            label, desc = f"Organelle-{art['data-ai']}", art.get("data-alt", art["data-ai"])
        elif cap:
            m = re.match(r"(Figure [\w.\-]+)\s*(.*)", cap); label = m.group(1) if m else "Figure"; desc = m.group(2) if m else cap
        else:
            h = svg.find_previous(["h2", "h3"]); label, desc = "Diagram", h.get_text(" ", strip=True) if h else f.name
        if not svg.get("width"):
            svg["width"] = "640"  # in the book these scale to their container; give a print-quality size
        n += 1
        name = f"{n:02d}_{slug(label)}_{slug(desc.split('.')[0])}.png"
        jobs.append({"svg": defs + str(svg), "out": str(OUT / name)})
        rows.append((name, f.name, label, desc[:160]))
cover = (SRC / "cover.html").read_text()
m = re.search(r'(<svg viewBox="0 30 1000 970".*?</svg>)', cover, flags=re.S)
n += 1; name = f"{n:02d}_Cover-cell_Cutaway-animal-cell.png"
jobs.append({"svg": m.group(1).replace("<svg ", '<svg width="900" ', 1), "out": str(OUT / name)}); rows.append((name, "cover.html", "Cover", "Front-cover cutaway animal cell (no labels)"))
jf = OUT.parent / "export-jobs.json"; jf.write_text(json.dumps(jobs))
js = OUT.parent / "export.js"; js.write_text(JS)
env = dict(os.environ); env.setdefault("PW_PATH", "/opt/node-tools/node_modules/playwright")
subprocess.run(["node", str(js), str(jf)], check=True, env=env)
jf.unlink(); js.unlink()
lines = ["| File | Used in | Label | What it shows |", "|---|---|---|---|"] + [f"| `{a}` | {b} | {c} | {d} |" for a, b, c, d in rows]
(OUT / "FIGURE-LIST.md").write_text("\n".join(lines) + "\n")
print(n, "images exported")
