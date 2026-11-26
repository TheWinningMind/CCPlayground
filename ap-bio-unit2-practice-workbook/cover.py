"""Build the wraparound paperback cover for the Practice Workbook (called from build.py after the interior).

The back cover's "Look inside" thumbnails are rendered from the interior PDF in grayscale, the way the book prints.
"""
import html
import re

import pypdfium2

from build import AUTHOR, BLEED, BUILD, NAME, OUT, ROOT, SPINE_PER_PAGE_IN, SRC, TRIM_H, TRIM_W, page_texts, render

IMAGES = ROOT / "images"

# (caption, text at the start of a line on the page, page offset)
SAMPLE_PAGES = [
    ("Exam-style multiple choice", "Topic 2.3 Practice", 1),
    ("Free response with answer space", "Free-Response Questions Topic 2.2", 0),
    ("Every answer explained", "Topic 2.1 Answers", 4),
]


def render_samples() -> None:
    pdf_path = OUT / f"{NAME}-Interior.pdf"
    texts = page_texts(pdf_path)
    doc = pypdfium2.PdfDocument(pdf_path)
    for n, (_, needle, offset) in enumerate(SAMPLE_PAGES, 1):
        rx = re.compile(r"(^|\n)\s*" + r"\s+".join(map(re.escape, needle.split())))
        idx = next(i for i, t in enumerate(texts) if i >= 3 and rx.search(t)) + offset
        doc[idx].render(scale=200 / 72).to_pil().convert("L").convert("RGB").save(BUILD / f"sample-{n}.png")


def build_cover(pages: int) -> None:
    render_samples()
    spine = pages * SPINE_PER_PAGE_IN
    width = BLEED + TRIM_W + spine + TRIM_W + BLEED
    height = BLEED + TRIM_H + BLEED
    out = ((SRC / "cover.html").read_text()
           .replace("{{W}}", f"{width:.4f}").replace("{{H}}", f"{height:.4f}")
           .replace("{{SPINE}}", f"{spine:.4f}").replace("{{BLEED}}", f"{BLEED}").replace("{{TRIM_W}}", f"{TRIM_W}")
           .replace("{{AUTHOR}}", html.escape(AUTHOR))
           .replace("{{FONTS}}", (SRC / "fonts").resolve().as_uri())
           .replace("{{IMG}}", IMAGES.resolve().as_uri())
           .replace("{{SAMPLES}}", BUILD.resolve().as_uri()))
    p = BUILD / "cover.html"
    p.write_text(out)
    render(p, OUT / f"{NAME}-Cover.pdf")
    print(f"Cover: {width:.3f} x {height:.3f} in, spine {spine:.3f} in for {pages} pages")
