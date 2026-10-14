"""Build the KDP print interior PDF and wraparound cover PDF.

Usage: python3 build.py
Outputs go to ./output/. Requires Playwright (Node) with Chromium and pypdf/pdfplumber.
"""
import html
import json
import os
import re
import subprocess
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "output"
BUILD = ROOT / ".build"

AUTHOR = os.environ.get("GUIDE_AUTHOR", "DAVID SREERAMA")
YEAR = os.environ.get("GUIDE_YEAR", "2026")

# KDP paperback, black ink on white paper: spine width = pages x 0.002252 in.
SPINE_PER_PAGE_IN = 0.002252
TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125

RENDER_JS = r"""
const { chromium } = require(process.env.PW_PATH || 'playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  await browser.close();
})();
"""


def render(html_path: Path, pdf_path: Path) -> None:
    js = BUILD / "render.js"
    js.write_text(RENDER_JS)
    env = dict(os.environ)
    env.setdefault("PW_PATH", "/opt/node-tools/node_modules/playwright")
    subprocess.run(["node", str(js), str(html_path), str(pdf_path)], check=True, env=env)


def assemble(toc: dict | None) -> str:
    parts = sorted(p for p in SRC.glob("*.html") if p.name[0].isdigit())
    body = "\n".join(p.read_text() for p in parts)
    body = body.replace("{{AUTHOR}}", html.escape(AUTHOR)).replace("{{YEAR}}", YEAR)
    if toc:
        def fill(m):
            key = html.unescape(m.group(1))
            return f'data-toc="{m.group(1)}">{toc.get(key, "")}<'
        body = re.sub(r'data-toc="([^"]+)"><', fill, body)
    css = (SRC / "style.css").read_text()
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>AP Biology Unit 1 Study Guide</title><style>{css}</style></head><body>{body}</body></html>"""


def find_pages(pdf_path: Path, keys: list[str]) -> dict:
    """Map each TOC key to the first page (after the contents page) whose text contains it."""
    found = {}
    with pdfplumber.open(pdf_path) as pdf:
        texts = [(pg.extract_text() or "") for pg in pdf.pages]
    start = 3  # skip title, copyright, contents
    for key in keys:  # entries are in reading order, so each search starts at the previous hit
        for i, t in enumerate(texts):
            if i < start:
                continue
            # Match at the start of a line so running heads and cross-references don't count.
            if re.search(r"(^|\n)" + r"\s+".join(map(re.escape, key.split())) + r"\s*(\n|$)", t):
                found[key] = i + 1
                start = i
                break
    return found


def build_interior() -> int:
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    keys = [html.unescape(k) for k in re.findall(r'data-toc="([^"]+)"', (SRC / "00-front.html").read_text())]

    first = BUILD / "pass1.html"
    first.write_text(assemble(None))
    render(first, BUILD / "pass1.pdf")
    toc = find_pages(BUILD / "pass1.pdf", keys)
    missing = [k for k in keys if k not in toc]
    if missing:
        raise SystemExit(f"TOC entries not found in PDF: {missing}")

    final = BUILD / "interior.html"
    final.write_text(assemble(toc))
    pdf = OUT / "AP-Biology-Unit-1-Study-Guide-Interior.pdf"
    render(final, pdf)
    # Page numbers are filled into existing boxes, so layout cannot shift between passes.
    assert find_pages(pdf, keys) == toc, "TOC page numbers shifted between passes"
    with pdfplumber.open(pdf) as p:
        n = len(p.pages)
    print("TOC:", json.dumps(toc))
    return n


def build_cover(pages: int) -> None:
    spine = pages * SPINE_PER_PAGE_IN
    width = BLEED + TRIM_W + spine + TRIM_W + BLEED
    height = BLEED + TRIM_H + BLEED
    tpl = (SRC / "cover.html").read_text()
    out = (tpl.replace("{{W}}", f"{width:.4f}").replace("{{H}}", f"{height:.4f}")
              .replace("{{SPINE}}", f"{spine:.4f}").replace("{{BLEED}}", f"{BLEED}")
              .replace("{{TRIM_W}}", f"{TRIM_W}").replace("{{AUTHOR}}", html.escape(AUTHOR))
              .replace("{{SPINE_TEXT}}", "" if pages < 100 else "block"))
    p = BUILD / "cover.html"
    p.write_text(out)
    render(p, OUT / "AP-Biology-Unit-1-Study-Guide-Cover.pdf")
    print(f"Cover: {width:.3f} x {height:.3f} in, spine {spine:.3f} in for {pages} pages")


if __name__ == "__main__":
    n = build_interior()
    print("Interior pages:", n)
    build_cover(n)
