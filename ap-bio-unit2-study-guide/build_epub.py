"""Build the Kindle eBook (reflowable EPUB 3) and the eBook cover JPG.

Usage: python3 build_epub.py   (run build.py first; the eBook cover is cut from the print cover PDF)
Reuses the chapter sources in src/. Diagrams are rasterized to PNG because Kindle's
support for inline SVG in reflowable books is unreliable.
"""
import html
import os
import re
import subprocess
import uuid
import zipfile
from pathlib import Path

import pypdfium2
from bs4 import BeautifulSoup, NavigableString

from build import AUTHOR, BLEED, BUILD, OUT, ROOT, SPINE_PER_PAGE_IN, SRC, TRIM_H, TRIM_W, YEAR, swap_ai_images

TITLE = "AP Biology Unit 2: Cell Structure and Function"
SUBTITLE = "The Comprehensive Study Guide"
LANG = "en"
EPUB = OUT / "AP-Biology-Unit-2-Study-Guide-Kindle.epub"
COVER_JPG = OUT / "AP-Biology-Unit-2-Study-Guide-Kindle-Cover.jpg"
WORK = BUILD / "epub"
AI_PREFIX = "images/ai-"

# Print-only wording that needs to change in a reflowable eBook.
REWORDS = [
    ("Write your answers in complete sentences on the lines provided or on separate paper.",
     "Write your answers in complete sentences on separate paper."),
    ("Construct</strong> an appropriately labeled graph of the data, including error bars.",
     "Construct</strong> an appropriately labeled graph of the data, including error bars, on graph paper."),
    ("Record each attempt. Redo any set",
     "Copy this table into a notebook and record each attempt. Redo any set"),
    ("Fill in each box from memory, then check your work against the lessons.",
     "Draw it on paper with six branches&mdash;SA:V Ratio, Increasing Surface Area, Heat Exchange, Benefits of Compartments, Endosymbiosis Steps, and Evidence&mdash;then check your work against the lessons."),
    ("Check each statement only when you can do it without notes.",
     "Check off each statement (in a notebook) only when you can do it without notes."),
]

SHOT_JS = r"""
const { chromium } = require(process.env.PW_PATH || 'playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 2 });
  for (const j of jobs) {
    await page.setContent(`<html><body style="margin:0;background:#fff;font-family:Inter,sans-serif">
      <div id="w" style="display:inline-block;padding:12px;background:#fff">${j.svg}</div></body></html>`);
    await page.evaluate(() => document.fonts.ready);
    await (await page.$('#w')).screenshot({ path: j.out });
  }
  await browser.close();
})();
"""

EBOOK_CSS = """
body { font-family: serif; line-height: 1.45; margin: 0 0.4em; }
h1 { font-family: sans-serif; font-size: 1.6em; line-height: 1.2; margin: 0.6em 0 0.5em; page-break-before: always; }
h2 { font-family: sans-serif; font-size: 1.25em; margin: 1.3em 0 0.4em; border-bottom: 1px solid #000; padding-bottom: 0.15em; page-break-after: avoid; }
h3 { font-family: sans-serif; font-size: 1.08em; margin: 1.1em 0 0.3em; page-break-after: avoid; }
h4 { font-family: sans-serif; font-size: 1em; margin: 0.9em 0 0.3em; }
p { margin: 0 0 0.6em; text-indent: 0; }
.eyebrow { font-family: sans-serif; font-size: 0.8em; letter-spacing: 0.12em; text-transform: uppercase; color: #555; margin: 0; }
.num { font-family: sans-serif; font-size: 2.6em; font-weight: bold; color: #999; margin: 0.3em 0 0; line-height: 1; }
.box { border: 1px solid #000; padding: 0.5em 0.7em; margin: 1em 0; }
.box.targets, .box.big { background-color: #eeeeee; }
.box.warn { border-left: 5px solid #000; }
.box.math { border-style: dashed; }
.label { font-family: sans-serif; font-size: 0.8em; font-weight: bold; letter-spacing: 0.1em; text-transform: uppercase; margin: 0 0 0.4em; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0 1em; font-size: 0.85em; }
th { background-color: #000; color: #fff; font-family: sans-serif; text-align: left; padding: 0.3em; }
td { border-bottom: 1px solid #999; padding: 0.3em; vertical-align: top; }
figure, .fig { margin: 1em 0; text-align: center; }
figure img, .fig img { max-width: 100%; height: auto; }
figcaption { font-family: sans-serif; font-size: 0.8em; text-align: left; margin-top: 0.3em; }
dl.vocab dt { font-family: sans-serif; font-weight: bold; margin-top: 0.5em; }
dl.vocab dd { margin: 0 0 0 1em; }
.q { margin: 0 0 1.1em; }
.q .stem { margin-bottom: 0.3em; }
.q p.ch { margin: 0 0 0.15em 1.2em; }
.qn { font-family: sans-serif; font-weight: bold; }
.ansref { font-family: sans-serif; font-size: 0.85em; }
.a { margin-bottom: 0.6em; }
.pts { font-family: sans-serif; font-size: 0.8em; color: #555; }
.frq-part { margin: 0.6em 0; }
.mm-box { border: 1px solid #000; padding: 0.4em 0.6em; margin: 0.6em 0; }
.mm-box h4 { margin: 0 0 0.3em; }
.mm-box ul { margin: 0; padding-left: 1.2em; }
.mm-hub { font-family: sans-serif; font-weight: bold; font-size: 1.2em; text-align: center; border: 2px solid #000; padding: 0.5em; margin: 0.8em 0; }
.mm-hub small { display: block; font-weight: normal; font-size: 0.75em; }
.mm-foot { font-family: sans-serif; font-weight: bold; text-align: center; margin: 0.8em 0; }
.wq { margin: 0 0 0.6em; }
.wai-key p { margin: 0 0 0.2em; }
.title-block { text-align: center; margin-top: 3em; }
.title-block .big { font-family: sans-serif; font-size: 2.4em; font-weight: bold; line-height: 1.1; margin: 0.3em 0; }
.title-block .sub { font-family: sans-serif; font-size: 1.15em; margin: 0.5em 0 1.5em; }
.title-block .author { font-family: sans-serif; font-weight: bold; letter-spacing: 0.08em; margin-top: 2em; }
.copyright p { font-size: 0.85em; }
.small { font-size: 0.85em; }
.center { text-align: center; }
.org { border: 1px solid #000; padding: 0.5em 0.7em; margin: 0.8em 0; }
.org .art { text-align: center; }
.org .art img { max-width: 70%; }
.where { font-family: sans-serif; font-size: 0.75em; letter-spacing: 0.08em; text-transform: uppercase; color: #555; margin: 0 0 0.3em; }
"""


def xhtml_page(title: str, body: str) -> str:
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            f'lang="{LANG}" xml:lang="{LANG}">\n<head><meta charset="utf-8"/><title>{html.escape(title)}</title>'
            f'<link rel="stylesheet" type="text/css" href="style.css"/></head>\n<body>\n{body}\n</body></html>\n')


def load_sections():
    raw = "\n".join(p.read_text() for p in sorted(SRC.glob("*.html")) if p.name[0].isdigit())
    raw = raw.replace("{{AUTHOR}}", html.escape(AUTHOR)).replace("{{YEAR}}", YEAR)
    raw = swap_ai_images(raw, src_for=lambda p: AI_PREFIX + p.name)
    for a, b in REWORDS:
        assert a in raw, f"reword target missing: {a[:50]}"
        raw = raw.replace(a, b)
    soup = BeautifulSoup(raw, "html.parser")
    return soup, soup.find_all("section", recursive=False)


def rasterize_figures(soup) -> list[str]:
    """Replace every inline SVG with a PNG <img>; return image file names."""
    img_dir = WORK / "OEBPS" / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    jobs, names = [], []
    defs = (SRC / "defs.svg").read_text()  # shared 3D gradients referenced by the figures
    for i, svg in enumerate(soup.find_all("svg"), 1):
        name = f"fig{i:02d}.png"
        jobs.append({"svg": defs + str(svg), "out": str(img_dir / name)})
        cap = svg.find_parent("figure")
        cap = cap.find("figcaption") if cap else None
        alt = cap.get_text(" ", strip=True) if cap else "Diagram"
        img = soup.new_tag("img", src=f"images/{name}", alt=alt)
        svg.replace_with(img)
        names.append(name)
    jobs_file = BUILD / "svg-jobs.json"
    jobs_file.write_text(__import__("json").dumps(jobs))
    js = BUILD / "shot.js"
    js.write_text(SHOT_JS)
    env = dict(os.environ)
    env.setdefault("PW_PATH", "/opt/node-tools/node_modules/playwright")
    subprocess.run(["node", str(js), str(jobs_file)], check=True, env=env)
    return names


def copy_ai_images(soup) -> list[str]:
    """Copy author-supplied AI images (already swapped into the HTML) into the eBook."""
    from build import IMAGES
    names = []
    for img in soup.find_all("img", src=re.compile("^" + re.escape(AI_PREFIX))):
        name = img["src"][len("images/"):]
        (WORK / "OEBPS" / "images" / name).write_bytes((IMAGES / name[len("ai-"):]).read_bytes())
        names.append(name)
    return names


def convert_quizzes(soup):
    """CSS counters are unreliable on Kindle: write question numbers and choice letters into the text."""
    for quiz in soup.select(".quiz"):
        for n, q in enumerate(quiz.select(".q"), 1):
            stem = q.select_one(".stem")
            num = soup.new_tag("span", attrs={"class": "qn"})
            num.string = f"{n}. "
            stem.insert(0, num)
            ol = q.select_one("ol.ch")
            for k, li in enumerate(ol.find_all("li", recursive=False)):
                p = soup.new_tag("p", attrs={"class": "ch"})
                letter = soup.new_tag("b")
                letter.string = f"({'ABCD'[k]}) "
                p.append(letter)
                for child in list(li.contents):
                    p.append(child.extract())
                ol.insert_before(p)
            ol.decompose()


def strip_print_only(soup):
    for sel in [".write", ".toc", ".dots", ".title-page .rule"]:
        for el in soup.select(sel):
            el.decompose()
    # The blank graphing grid in FRQ 1(c) is replaced by "on graph paper" wording.
    for fig in soup.select(".frq-part figure"):
        fig.decompose()
    for el in soup.select(".check"):
        el.decompose()
    # The blank "build your own" mind map is a print-only worksheet; its intro is reworded below.
    for el in soup.select(".mm-blank"):
        el.decompose()
    # Kindle reads top to bottom: put each mind map's center topic before its branches.
    for grid in soup.select(".mm-grid"):
        hub = grid.select_one(".mm-hub")
        if hub:
            grid.insert_before(hub.extract())
    for el in soup.select(".blank"):
        el.replace_with("__________")
    for el in soup.select("[style]"):
        del el["style"]


def link_quizzes_to_answers(soup):
    for h in soup.select("h2"):
        m = re.match(r"Check Your Understanding (2\.\d+)", h.get_text(strip=True))
        if m:
            quiz = h.find_next_sibling("div", class_="quiz")
            p = soup.new_tag("p", attrs={"class": "ansref"})
            a = soup.new_tag("a", href=f"answers-cyu.xhtml#ans-{m.group(1).replace('.', '-')}")
            a.string = f"Go to answers for Topic {m.group(1)}"
            p.append(a)
            quiz.insert_after(p)
    for h in soup.select("h2"):
        m = re.fullmatch(r"Topic (2\.\d+)", h.get_text(strip=True))
        if m:
            h["id"] = f"ans-{m.group(1).replace('.', '-')}"


def section_title(sec) -> str:
    h = sec.find("h1")
    return h.get_text(" ", strip=True) if h else ""


def build():
    import shutil
    shutil.rmtree(WORK, ignore_errors=True)
    (WORK / "META-INF").mkdir(parents=True)
    oebps = WORK / "OEBPS"
    oebps.mkdir()

    soup, sections = load_sections()
    strip_print_only(soup)
    images = rasterize_figures(soup)
    ai_images = copy_ai_images(soup)
    convert_quizzes(soup)
    link_quizzes_to_answers(soup)

    # Title page as text (Kindle shows the cover image separately).
    title_body = (f'<section class="title-block" epub:type="titlepage"><p class="eyebrow">AP&#174; Biology &#183; Unit 2</p>'
                  f'<p class="big">Cell Structure and Function</p><p class="sub">{SUBTITLE}<br/>Organelles, Membranes, '
                  f'Transport, and Compartmentalization</p><p class="author">{html.escape(AUTHOR)}</p></section>')

    chapters = [("title.xhtml", TITLE, title_body, None)]
    slug_for = {
        "Answers: Check Your Understanding": "answers-cyu",
        "Answers: Practice Test": "answers-test",
    }
    part_of = {
        "Cell Structure: Subcellular Components": "Part 1: The Lessons",
        "Science Practices and Unit 2 Math": "Part 2: Skills and Review",
        "Section I: Multiple Choice": "Part 3: Practice",
        "Answers: Check Your Understanding": "Part 4: Answers and Reference",
    }
    n = 0
    for sec in sections:
        if sec.attrs is None:  # removed by strip_print_only (e.g. the printed contents page)
            continue
        classes = sec.get("class") or []
        if "title-page" in classes:
            continue
        if "copyright" in classes:
            sec.name = "section"
            chapters.append(("copyright.xhtml", "Copyright", str(sec), None))
            continue
        title = section_title(sec)
        if not title:
            # Sections without their own heading (e.g. each mind map page) continue the previous chapter.
            fname_prev, title_prev, body_prev, part_prev = chapters[-1]
            chapters[-1] = (fname_prev, title_prev, body_prev + "\n" + str(sec), part_prev)
            continue
        n += 1
        fname = f"{slug_for.get(title, f'ch{n:02d}')}.xhtml"
        h1 = sec.find("h1")
        h1["id"] = "top"
        chapters.append((fname, title, str(sec), part_of.get(title)))

    # Validate XHTML well-formedness by round-tripping through lxml's XML parser.
    from lxml import etree
    for fname, title, body, _ in chapters:
        doc = xhtml_page(title, body)
        doc = re.sub(r"<(img|br|hr|meta|link)([^>]*?)(?<!/)>", r"<\1\2/>", doc)
        etree.fromstring(doc.encode("utf-8"))
        (oebps / fname).write_text(doc)

    (oebps / "style.css").write_text(EBOOK_CSS)

    # Navigation: EPUB 3 nav + NCX for older Kindle devices.
    nav_items, current_part, part_open = [], None, False
    toc_entries = [c for c in chapters if c[0] not in ("title.xhtml", "copyright.xhtml")]
    for fname, title, _, part in toc_entries:
        if part:
            if part_open:
                nav_items.append("</ol></li>")
            nav_items.append(f'<li><a href="{fname}">{html.escape(part)}</a><ol>')
            part_open = True
        nav_items.append(f'<li><a href="{fname}">{html.escape(title)}</a></li>')
    if part_open:
        nav_items.append("</ol></li>")
    first_lesson = next(c[0] for c in chapters if c[1] == "How to Use This Guide")
    nav = (f'<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{"".join(nav_items)}</ol></nav>'
           f'<nav epub:type="landmarks" hidden=""><ol>'
           f'<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>'
           f'<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>'
           f'<li><a epub:type="bodymatter" href="{first_lesson}">Start</a></li></ol></nav>')
    (oebps / "nav.xhtml").write_text(xhtml_page("Contents", nav))

    ncx_points = "".join(
        f'<navPoint id="np{i}" playOrder="{i}"><navLabel><text>{html.escape(t)}</text></navLabel>'
        f'<content src="{f}"/></navPoint>' for i, (f, t, _, _) in enumerate(toc_entries, 1))
    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'ap-bio-unit2-study-guide/' + AUTHOR)}"
    (oebps / "toc.ncx").write_text(
        f'<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
        f'<head><meta name="dtb:uid" content="{book_id}"/></head><docTitle><text>{html.escape(TITLE)}</text></docTitle>'
        f'<navMap>{ncx_points}</navMap></ncx>')

    # Cover: cut the front panel out of the print cover PDF.
    make_cover_jpg()
    (oebps / "images" / "cover.jpg").write_bytes(COVER_JPG.read_bytes())
    (oebps / "cover.xhtml").write_text(xhtml_page(
        "Cover", '<div class="center"><img src="images/cover.jpg" alt="Cover"/></div>'))

    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="css" href="style.css" media-type="text/css"/>',
        '<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
        '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>',
    ]
    manifest += [f'<item id="{f[:-6]}" href="{f}" media-type="application/xhtml+xml"/>' for f, *_ in chapters]
    manifest += [f'<item id="img-{i[:-4]}" href="images/{i}" media-type="image/png"/>' for i in images]
    manifest += [f'<item id="{i.rsplit(".", 1)[0]}" href="images/{i}" '
                 f'media-type="{"image/png" if i.endswith(".png") else "image/jpeg"}"/>' for i in ai_images]
    spine = ['<itemref idref="cover" linear="no"/>'] + [f'<itemref idref="{f[:-6]}"/>' for f, *_ in chapters]
    spine.insert(3, '<itemref idref="nav"/>')  # contents after title and copyright
    from datetime import datetime, timezone
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (oebps / "content.opf").write_text(f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANG}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{book_id}</dc:identifier>
    <dc:title>{html.escape(TITLE)}</dc:title>
    <dc:creator>{html.escape(AUTHOR)}</dc:creator>
    <dc:language>{LANG}</dc:language>
    <dc:rights>Copyright {YEAR} {html.escape(AUTHOR)}. All rights reserved.</dc:rights>
    <meta property="dcterms:modified">{modified}</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
    {chr(10).join('    ' + m for m in manifest).strip()}
  </manifest>
  <spine toc="ncx">
    {chr(10).join('    ' + s for s in spine).strip()}
  </spine>
</package>
""")
    (WORK / "META-INF" / "container.xml").write_text(
        '<?xml version="1.0" encoding="utf-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')

    EPUB.unlink(missing_ok=True)
    with zipfile.ZipFile(EPUB, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        for p in sorted(WORK.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(WORK).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    print(f"EPUB: {EPUB.relative_to(ROOT)} ({len(chapters)} chapters, {len(images)} figures)")


def make_cover_jpg():
    """KDP eBook cover: front panel of the print cover, 2560 px tall, RGB JPEG."""
    pdf = pypdfium2.PdfDocument(OUT / "AP-Biology-Unit-2-Study-Guide-Cover.pdf")
    page = pdf[0]
    w_in = page.get_width() / 72
    spine = w_in - 2 * BLEED - 2 * TRIM_W
    scale = 2560 / (TRIM_H * 72)
    img = page.render(scale=scale).to_pil().convert("RGB")
    px = img.width / w_in
    left = (BLEED + TRIM_W + spine) * px
    box = (round(left), round(BLEED * px), round(left + TRIM_W * px), round((BLEED + TRIM_H) * px))
    img.crop(box).save(COVER_JPG, "JPEG", quality=92)


if __name__ == "__main__":
    build()
