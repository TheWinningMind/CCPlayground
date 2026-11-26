"""Build the KDP print interior PDF (and, with build_cover, the wraparound cover) for the Practice Workbook.

Usage:  python3 build.py
Reads the converted fragments in src/gen/ (made by tools/convert.py from the author's Word files)
and writes output/AP-Biology-Unit-2-Practice-Workbook-Interior.pdf.
Requires Playwright (Node) with Chromium, pdfplumber and BeautifulSoup.
"""
import html
import json
import os
import re
import subprocess
from pathlib import Path

import pdfplumber
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
GEN = SRC / "gen"
OUT = ROOT / "output"
BUILD = ROOT / ".build"
NAME = "AP-Biology-Unit-2-Practice-Workbook"

AUTHOR = os.environ.get("GUIDE_AUTHOR", "DAVID SREERAMA")
YEAR = os.environ.get("GUIDE_YEAR", "2026")

SPINE_PER_PAGE_IN = 0.002252  # KDP black ink on white paper
TRIM_W, TRIM_H, BLEED = 8.5, 11.0, 0.125

TOPICS = [
    ("2.1", "Cell Structure and Function"),
    ("2.2", "Cell Size"),
    ("2.3", "Plasma Membrane"),
    ("2.4", "Membrane Permeability"),
    ("2.5", "Membrane Transport"),
    ("2.6", "Facilitated Diffusion"),
    ("2.7", "Tonicity and Osmoregulation"),
    ("2.8", "Mechanisms of Transport"),
    ("2.9", "Cell Compartmentalization"),
    ("2.10", "Origins of Cell Compartmentalization"),
]

RENDER_JS = r"""
const { chromium } = require(process.env.PW_PATH || 'playwright');
(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + src, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true, timeout: 0 });
  await browser.close();
})();
"""


def render(html_path: Path, pdf_path: Path) -> None:
    js = BUILD / "render.js"
    js.write_text(RENDER_JS)
    env = dict(os.environ)
    env.setdefault("PW_PATH", "/opt/node-tools/node_modules/playwright")
    subprocess.run(["node", str(js), str(html_path), str(pdf_path)], check=True, env=env)


def gen(name: str) -> str:
    p = GEN / f"{name}.html"
    return p.read_text() if p.exists() else ""


def count(name: str, pattern: str) -> int:
    return len(re.findall(pattern, gen(name)))


def stats(t: str) -> dict:
    set_no = f"{int(t.split('.')[1]):02d}"
    return {
        "mcq": count(f"{t}-mcq-q", r'class="q"'),
        "frq": count(f"{t}-frq-q", r'class="frq"'),
        "frq_pts": sum(int(x) for x in re.findall(r'class="frq">[^<]*?[\[(](\d+) points?[\])]', gen(f"{t}-frq-q"))),
        "prob": count(f"set{set_no}-prob-q", r'class="prob"'),
        "wai": count(f"{t}-vocab-q", r"<strong>\d{2}\.</strong>"),
        "id": count(f"{t}-id-q", r"<strong>\d{2}\.</strong>"),
        "set": set_no,
    }


# ---------------------------------------------------------------- page pieces
def polish(fragment: str) -> str:
    """Final touches on converted HTML: writing-line heights, short choices in two columns, long tables may split."""
    soup = BeautifulSoup(f"<div id='x'>{fragment}</div>", "lxml")
    root = soup.find(id="x")
    for d in root.find_all("div", class_="wl"):  # merge neighbouring line blocks into one answer space
        if d.parent is None:
            continue
        nxt = d.find_next_sibling()
        while nxt is not None and nxt.name == "div" and "wl" in nxt.get("class", []):
            d["data-n"] = str(int(d.get("data-n", "1")) + int(nxt.get("data-n", "1")))
            gone, nxt = nxt, nxt.find_next_sibling()
            gone.decompose()
    for d in root.find_all("div", class_="wl"):
        n = int(d.get("data-n", "1"))
        n = 2 if n == 1 else n  # a single underscore line in the source stands for a short answer
        d.clear()
        for _ in range(n):
            d.append(soup.new_tag("i"))
    for ol in root.find_all("ol", class_="choices"):
        lis = ol.find_all("li")
        if lis and max(len(li.get_text(" ").strip()) for li in lis) <= 34 and not ol.find(["img", "table"]):
            ol["class"] = ["choices", "short"]
    for p in root.find_all("p"):  # answer-key lines such as "Question 04 | Correct answer: B" stand out
        if re.match(r"^\s*(Question\s+\d+\s*\||Q\d+\s*[—–-])", p.get_text(" ")) and not p.find("strong"):
            p["class"] = p.get("class", []) + ["akey"]
    for tb in root.find_all("table"):
        if len(tb.find_all("tr")) > 14:
            tb["class"] = "long"
    return root.decode_contents()


TRIMS: dict[str, int] = {}  # problem title -> writing lines to remove so it does not spill onto an empty page


def problem_blocks(fragment: str) -> str:
    """Wrap each problem (its h3.prob title and everything up to the next one) in <section class="pblock">.

    Lines listed in TRIMS are taken from the problem's last answer spaces (each keeps at least two lines).
    """
    soup = BeautifulSoup(f"<div id='x'>{fragment}</div>", "lxml")
    root = soup.find(id="x")
    block = None
    for el in list(root.children):
        if getattr(el, "name", None) == "h3" and "prob" in el.get("class", []):
            block = soup.new_tag("section", attrs={"class": "pblock"})
            el.insert_before(block)
        if block is not None and el is not block:
            block.append(el.extract())
    for blk in root.find_all("section", class_="pblock"):
        cut = TRIMS.get(re.sub(r"\s+", " ", blk.find("h3").get_text(" ")).strip(), 0)
        for wl in reversed(blk.find_all("div", class_="wl")):
            while cut and len(wl.find_all("i")) > 2:
                wl.find_all("i")[-1].decompose()
                cut -= 1
    return root.decode_contents()


def opener(t: str, title: str, s: dict) -> str:
    items = [(s["mcq"], "multiple-choice questions"), (s["frq"], f"free-response questions ({s['frq_pts']} points)"),
             (s["prob"], f"problems in Problem Set {s['set']}"), (s["wai"], "&ldquo;Who Am I?&rdquo; clues"),
             (s["id"], "identity-challenge clues")]
    counts = "".join(f"<div><b>{n}</b>{label}</div>" for n, label in items if n)
    return f"""<section class="opener">
  <div class="tline">Topic {t} Practice</div>
  <div class="num">{t}</div>
  <h1>{title}</h1>
  <div class="counts">{counts}</div>
  <div class="box targets howto"><div class="label">Suggested order</div>
    <ol><li>Answer the multiple-choice questions in one sitting, then mark them with the key in Part 3.</li>
    <li>Write full answers to the free-response questions before you look at the scoring guidelines.</li>
    <li>Work the problem set with a calculator, showing every step and unit.</li>
    <li>Finish with the vocabulary clues as a quick retrieval check.</li></ol></div>
</section>"""


def topic_chapter(t: str, title: str) -> str:
    s = stats(t)
    out = [opener(t, title, s)]
    out.append(f'<h2 class="part-head">Multiple-Choice Questions<span class="cnt">Topic {t} &middot; {s["mcq"]} questions</span></h2>')
    out.append(polish(gen(f"{t}-mcq-q")))
    out.append(f'<h2 class="part-head">Free-Response Questions<span class="cnt">Topic {t} &middot; {s["frq"]} questions &middot; {s["frq_pts"]} points</span></h2>')
    out.append(f'<div class="frqs">{polish(gen(f"{t}-frq-q"))}</div>')
    out.append(f'<h2 class="part-head">Problem Set {s["set"]}<span class="cnt">Topic {t} &middot; {s["prob"]} problems</span></h2>')
    out.append(f'<div class="probs">{problem_blocks(polish(gen(f"set{s["set"]}-prob-q")))}</div>')
    if s["wai"]:
        out.append(f'<h2 class="part-head">Vocabulary: Who Am I?<span class="cnt">Topic {t} &middot; {s["wai"]} clues</span></h2>')
        out.append(f'<div class="vocab">{polish(gen(f"{t}-vocab-q"))}</div>')
    out.append(f'<h2 class="part-head">Vocabulary: Identity Challenge<span class="cnt">Topic {t} &middot; {s["id"]} clues</span></h2>')
    out.append(f'<div class="vocab">{polish(gen(f"{t}-id-q"))}</div>')
    return "\n".join(out)


def review_chapter() -> str:
    out = ["""<section class="opener">
  <div class="tline">Unit 2 Review Problems</div>
  <div class="num">2.R</div>
  <h1>Integrated Unit 2 Problems</h1>
  <p>These two problem sets combine ideas from all ten topics, the way real AP free-response questions do. Use them after you finish the topic chapters, or as a timed review before a unit test.</p>
</section>"""]
    for nn in ("11", "12"):
        out.append(f'<h2 class="part-head">Problem Set {nn}<span class="cnt">Topics 2.1&ndash;2.10 &middot; {count(f"set{nn}-prob-q", chr(99)+"lass=.prob.")} problems</span></h2>')
        out.append(f'<div class="probs">{problem_blocks(polish(gen(f"set{nn}-prob-q")))}</div>')
    return "\n".join(out)


def answers_chapter(t: str, title: str) -> str:
    s = stats(t)
    out = [f'<section class="answers"><h1 class="ans-head"><span class="tline">Topic {t} Answers</span><br>{title}</h1>',
           f'<h2>Multiple-Choice Answers and Explanations</h2><div class="cols2">{polish(gen(f"{t}-mcq-a"))}</div>',
           f'<h2 class="part-head">Free-Response Scoring Guidelines</h2>{polish(gen(f"{t}-frq-a"))}',
           f'<h2 class="part-head">Problem Set {s["set"]}: Worked Solutions</h2><div class="probs">{polish(gen(f"set{s["set"]}-prob-a"))}</div>']
    vocab = []
    if s["wai"]:
        vocab.append(f'<h3>Who Am I?</h3><div class="cols2">{polish(gen(f"{t}-vocab-a"))}</div>')
    vocab.append(f'<h3>Identity Challenge</h3><div class="cols2">{polish(gen(f"{t}-id-a"))}</div>')
    out.append('<h2 class="part-head">Vocabulary Answers</h2>' + "".join(vocab))
    out.append("</section>")
    return "\n".join(out)


def review_answers() -> str:
    out = ['<section class="answers"><h1 class="ans-head"><span class="tline">Unit 2 Review Answers</span><br>Integrated Unit 2 Problems</h1>']
    for nn in ("11", "12"):
        out.append(f'<h2 class="part-head">Problem Set {nn}: Worked Solutions</h2><div class="probs">{polish(gen(f"set{nn}-prob-a"))}</div>')
    out.append("</section>")
    return "\n".join(out)


def front() -> str:
    tot = {k: sum(stats(t)[k] for t, _ in TOPICS) for k in ("mcq", "frq", "frq_pts", "wai", "id")}
    tot["prob"] = sum(count(f"set{n:02d}-prob-q", r'class="prob"') for n in range(1, 13))
    rows = "".join(
        f"<tr><td>{t}&nbsp; {title}</td><td>{s['mcq']}</td><td>{s['frq']}</td><td>{s['prob']}</td><td>{s['wai'] or '&ndash;'}</td><td>{s['id']}</td></tr>"
        for t, title in TOPICS for s in [stats(t)])
    rows += f"<tr><td>Unit 2 Review (Problem Sets 11&ndash;12)</td><td>&ndash;</td><td>&ndash;</td><td>{tot['prob'] - sum(stats(t)['prob'] for t, _ in TOPICS)}</td><td>&ndash;</td><td>&ndash;</td></tr>"
    rows += f"<tr><td><b>Total</b></td><td><b>{tot['mcq']}</b></td><td><b>{tot['frq']}</b></td><td><b>{tot['prob']}</b></td><td><b>{tot['wai']}</b></td><td><b>{tot['id']}</b></td></tr>"
    toc = ['<li><span>How to Use This Workbook</span><span class="dots"></span><span class="pg" data-toc="How to Use This Workbook"></span></li>',
           '<li class="part"><span>Part 1 &middot; Topic Practice</span></li>']
    toc += [f'<li class="sub"><span>Topic {t} &nbsp;{title}</span><span class="dots"></span><span class="pg" data-toc="Topic {t} Practice"></span></li>' for t, title in TOPICS]
    toc += ['<li class="part"><span>Part 2 &middot; Unit Review</span></li>',
            '<li class="sub"><span>Integrated Unit 2 Problems</span><span class="dots"></span><span class="pg" data-toc="Unit 2 Review Problems"></span></li>',
            '<li class="part"><span>Part 3 &middot; Answers and Explanations</span></li>']
    toc += [f'<li class="sub"><span>Topic {t} &nbsp;{title}</span><span class="dots"></span><span class="pg" data-toc="Topic {t} Answers"></span></li>' for t, title in TOPICS]
    toc += ['<li class="sub"><span>Integrated Unit 2 Problems</span><span class="dots"></span><span class="pg" data-toc="Unit 2 Review Answers"></span></li>',
            '<li><span>Score Log</span><span class="dots"></span><span class="pg" data-toc="Score Log"></span></li>']
    return f"""
<section class="title-page">
  <div>
    <div class="kicker">AP&reg; Biology</div>
    <div class="big">Unit 2<br>Practice<br>Workbook</div>
    <div class="sub">Cell Structure and Function</div>
    <div class="rule"></div>
    <div class="feat">{tot['mcq']} multiple-choice questions with explanations<br>
      {tot['frq']} free-response questions with scoring guidelines<br>
      {tot['prob']} data and calculation problems with worked solutions<br>
      {tot['wai'] + tot['id']} vocabulary clues with answers</div>
  </div>
  <div class="author">{html.escape(AUTHOR)}</div>
</section>
<section class="copyright">
  <p><strong>AP&reg; Biology Unit 2: Cell Structure and Function &mdash; Practice Workbook</strong></p>
  <p>Copyright &copy; {YEAR} {html.escape(AUTHOR)}. All rights reserved.</p>
  <p>No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means&mdash;electronic, mechanical, photocopying, recording, or otherwise&mdash;without the prior written permission of the publisher, except for brief quotations in reviews.</p>
  <p><strong>Trademark notice.</strong> AP&reg; and Advanced Placement&reg; are registered trademarks of the College Board, which is not affiliated with, and does not endorse, this product. All questions in this workbook are original and were written to reflect the style and content of the AP Biology course; they are not official AP Exam questions.</p>
  <p><strong>Data and figures.</strong> Experimental data in this workbook are hypothetical and were created for practice. Diagrams are simplified instructional models and are not to scale.</p>
  <p><strong>Disclaimer.</strong> This workbook is a supplementary study aid aligned to the AP Biology Course and Exam Description effective Fall 2025. Always check the current Course and Exam Description published by the College Board. While every effort has been made to ensure accuracy, the author and publisher assume no responsibility for errors or omissions.</p>
  <p>First edition</p>
</section>
<section class="toc"><h1>Contents</h1><ol>{''.join(toc)}</ol></section>
<section class="howto-page">
  <h1>How to Use This Workbook</h1>
  <p>This workbook is the practice companion to <em>AP&reg; Biology Unit 2: Cell Structure and Function &mdash; The Comprehensive Study Guide</em>. It follows the same ten topics in the same order (Course and Exam Description effective Fall 2025), so you can study a topic in the guide and then practice it here. It also works on its own.</p>
  <h2>What&rsquo;s inside</h2>
  <table><thead><tr><th>Topic</th><th>MCQ</th><th>FRQ</th><th>Problems</th><th>Who Am I?</th><th>Identity</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>A simple routine for each topic</h2>
  <ol class="steps">
    <li><strong>Multiple choice.</strong> Answer every question before checking any. Circle your choice and mark the ones you guessed. Then check your work with the explanations in Part 3, including the ones you got right by guessing.</li>
    <li><strong>Free response.</strong> Write complete sentences on the lines provided. Use the task verb: <em>describe</em>, <em>explain</em>, <em>calculate</em>, <em>predict</em>, or <em>justify</em>. Score yourself with the point-by-point guidelines, then rewrite any part that earned no points.</li>
    <li><strong>Problems.</strong> Show the equation, the substituted values, and the answer with units. The worked solutions show every step, so compare your method as well as your final number.</li>
    <li><strong>Vocabulary.</strong> Fill in the clues from memory. Any term you miss is a term to review in your notes or the study guide.</li>
    <li><strong>Track your progress</strong> in the Score Log at the back of the book.</li>
  </ol>
  <div class="box tip"><div class="label">Exam tip</div><p>On the AP Exam, a correct answer with no reasoning usually earns little credit. When you check your free-response answers, look for the key idea each point requires, not the exact wording.</p></div>
</section>
"""


def score_log() -> str:
    rows = "".join(
        f"<tr><td>{t}&nbsp; {title}</td><td>&nbsp;/ {s['mcq']}</td><td>&nbsp;/ {s['frq_pts']}</td><td>&nbsp;/ {s['prob']}</td><td>&nbsp;/ {s['wai'] + s['id']}</td><td></td></tr>"
        for t, title in TOPICS for s in [stats(t)])
    return f"""<section class="score"><h1 class="ans-head">Score Log</h1>
<p>Record your scores after checking each section. Fill in the last column with the date you will review your weakest areas again.</p>
<table class="log"><thead><tr><th>Topic</th><th>MCQ correct</th><th>FRQ points</th><th>Problems solved</th><th>Vocabulary</th><th>Review again on</th></tr></thead><tbody>{rows}</tbody></table>
</section>"""


def assemble(toc: dict | None) -> str:
    body = [front()]
    body.append('<div class="partpage">' + "".join(topic_chapter(t, title) for t, title in TOPICS) + "</div>")
    body.append(review_chapter())
    body += [answers_chapter(t, title) for t, title in TOPICS]
    body.append(review_answers())
    body.append(score_log())
    html_body = "\n".join(body)
    base = SRC.resolve().as_uri()
    html_body = html_body.replace('src="img/', f'src="{base}/img/')
    if toc:
        def fill(m):
            return f'data-toc="{m.group(1)}">{toc.get(html.unescape(m.group(1)), "")}<'
        html_body = re.sub(r'data-toc="([^"]+)"><', fill, html_body)
    css = (SRC / "style.css").read_text().replace('url("fonts/', f'url("{base}/fonts/')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>AP Biology Unit 2 Practice Workbook</title><style>{css}</style></head><body>{html_body}</body></html>"""




def page_texts(pdf_path: Path) -> list[str]:
    import pypdfium2
    doc = pypdfium2.PdfDocument(pdf_path)
    return [pg.get_textpage().get_text_range().replace("\r\n", "\n") for pg in doc]


def find_pages(pdf_path: Path, keys: list[str]) -> dict:
    texts, found, start = page_texts(pdf_path), {}, 3
    for key in keys:
        rx = re.compile(r"(^|\n)\s*" + r"\s+".join(map(re.escape, key.split())) + r"(?=\s|$)")
        for i in range(start, len(texts)):
            if rx.search(texts[i]):
                found[key] = i + 1
                start = i
                break
    return found


def orphan_problems(pdf_path: Path) -> list[str]:
    """Problems whose last writing lines spill onto a page that has no text of its own."""
    texts, out = page_texts(pdf_path), []
    for i, t in enumerate(texts):
        body = "".join(l for l in t.split("\n") if l.strip() and not l.strip().isdigit()
                       and "PRACTICE WORKBOOK" not in l and "AP® BIOLOGY" not in l)
        if body or i == 0:
            continue
        for j in range(i - 1, max(i - 4, 0), -1):
            hits = re.findall(r"Problem \d+ \|[^\n]*", texts[j])
            if hits:
                out.append(re.sub(r"\s+", " ", hits[-1]).strip())
                break
    return out


def build_interior() -> int:
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    keys = [html.unescape(k) for k in re.findall(r'data-toc="([^"]+)"', front())]
    first = BUILD / "pass1.html"
    for attempt in range(6):
        first.write_text(assemble(None))
        render(first, BUILD / "pass1.pdf")
        spill = orphan_problems(BUILD / "pass1.pdf")
        if not spill:
            break
        for pid in spill:
            TRIMS[pid] = TRIMS.get(pid, 0) + 3
        print("Trimming writing lines to avoid near-empty pages:", spill)
    toc = find_pages(BUILD / "pass1.pdf", keys)
    missing = [k for k in keys if k not in toc]
    if missing:
        raise SystemExit(f"TOC entries not found in PDF: {missing}")
    final = BUILD / "interior.html"
    final.write_text(assemble(toc))
    pdf = OUT / f"{NAME}-Interior.pdf"
    render(final, pdf)
    assert find_pages(pdf, keys) == toc, "TOC page numbers shifted between passes"
    n = len(page_texts(pdf))
    print("TOC:", json.dumps(toc))
    return n


if __name__ == "__main__":
    n = build_interior()
    print("Interior pages:", n)
    if (SRC / "cover.html").exists():
        from cover import build_cover
        build_cover(n)
