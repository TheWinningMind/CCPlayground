"""Convert the author's Word library (../new-material) into HTML fragments for the workbook.

Usage:  python3 tools/convert.py
Needs pandoc, BeautifulSoup (bs4 + lxml) and Pillow. Writes src/gen/*.html and src/img/*.png.
The fragments are committed, so building the book does not need pandoc.

Each source file is converted with pandoc, then cleaned:
  * title-page boilerplate, editorial notes and LOTS/HOTS labels are removed;
  * multiple-choice questions become <div class="q"> blocks with an <ol class="choices">;
  * runs of underscores become ruled writing lines;
  * images are copied to src/img/ with stable names.
"""
from __future__ import annotations

import csv
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT.parent / "new-material"
ZIP = LIB / "07_Topic_2_6_Facilitated_Diffusion.zip"
WORK = ROOT / ".build" / "convert"
GEN = ROOT / "src" / "gen"
IMG = ROOT / "src" / "img"

TOPICS = [f"2.{i}" for i in range(1, 11)]
EXPECTED_MCQ = {"2.1": 70, "2.2": 40, "2.3": 40, "2.4": 40, "2.5": 45, "2.6": 35,
                "2.7": 60, "2.8": 30, "2.9": 35, "2.10": 35}

# Paragraphs that belong to the source files' title pages or editorial notes, not to the practice.
JUNK = [r"endorsed", r"affiliated", r"^DAVID SREERAMA", r"DAVID SREERAMA\s*[•|]", r"ORIGINAL (UNOFFICIAL )?AP-STYLE",
        r"Lower-Order Thinking", r"QUESTION BOOKLET", r"ANSWER KEY AND EXPLANATIONS", r"^AP BIOLOGY · UNIT 2",
        r"^CELL STRUCTURE", r"^Question booklet", r"scored answers", r"^Correct answer, scientific explanation",
        r"^Instructions:", r"^Select (the|one) (single )?best answer", r"^Choose the one best answer",
        r"^Assessment design and instructions", r"^Content boundary", r"^Editorial status", r"^Alignment and originality",
        r"^Curriculum (source|reference)", r"^Scope:", r"^Suggested use", r"^Student( name)?:", r"^Score:", r"^AP Biology \| Unit 2",
        r"^“What Am I\?”", r"^STUDENT QUESTION BOOKLET", r"^COMPLETE ANSWER KEY", r"^Use this key after",
        r"^How to use this key", r"^Each explanation identifies", r"^Analytic scoring suggestions", r"^Twelve collections",
        r"^Five topic-specific", r"^Four topic-specific", r"^Six topic-specific", r"^Eight topic-specific",
        r"^Original (independent|practice)", r"^An original, unofficial", r"^SCIENTIFIC VOCABULARY", r"^College Board learning objective",
        r"^\d+ original AP-style free-response", r"^Independent, original practice", r"apcentral\.collegeboard\.org"]
JUNK_RE = re.compile("|".join(JUNK), re.I)
KEEP_RE = re.compile(r"R\s*=\s*0\.0831|Ψ", re.I)  # instructions that carry data stay

Q_RE = re.compile(r"^\s*(\d{1,2})[.)]\s+\S")
CH_RE = re.compile(r"^\s*\(?([A-D])[).]\s+")


def text(el) -> str:
    return re.sub(r"\s+", " ", el.get_text(" ") if isinstance(el, Tag) else str(el)).strip()


def source(rel: str) -> Path:
    if rel.startswith("zip:"):
        dest = WORK / "zip"
        if not dest.exists():
            zipfile.ZipFile(ZIP).extractall(dest)
        return dest / rel[4:]
    return LIB / rel


def pandoc(path: Path, key: str) -> BeautifulSoup:
    media = WORK / "media" / key
    out = subprocess.run(["pandoc", str(path), "-t", "html", "--wrap=none", f"--extract-media={media}"],
                         check=True, capture_output=True, text=True).stdout
    return BeautifulSoup(f"<div id='root'>{out}</div>", "lxml")


# ---------------------------------------------------------------- generic cleaning
def clean(soup: BeautifulSoup, key: str) -> Tag:
    root = soup.find(id="root")
    for t in root.find_all(["colgroup"]):
        t.decompose()
    for t in root.find_all(["table", "td", "th", "col", "tr"]):
        for a in ("style", "class", "width"):
            t.attrs.pop(a, None)
    for t in root.find_all("blockquote"):
        t.unwrap()
    for t in root.find_all(["span", "u"]):
        if not t.attrs or t.get("class") in (["underline"], None):
            t.unwrap()
    # Images: copy to src/img with stable names.
    for i, im in enumerate(root.find_all("img"), 1):
        src = Path(im["src"])
        name = f"{key.replace('.', '-')}-{i}.png"
        try:
            pic = Image.open(src)
            pic = pic.convert("RGBA") if pic.mode in ("P", "LA", "RGBA") else pic.convert("RGB")
            if pic.width > 2000:
                pic = pic.resize((2000, round(pic.height * 2000 / pic.width)), Image.LANCZOS)
            pic.save(IMG / name, optimize=True)
        except Exception as e:  # unreadable vector formats etc.
            print("  ! image skipped", src, e)
            im.decompose()
            continue
        w = re.search(r"width:\s*([\d.]+)in", im.get("style", ""))
        im.attrs = {"src": f"img/{name}", "alt": im.get("alt", "")}
        if w:
            im["style"] = f"width:{min(float(w.group(1)), 6.5):.2f}in"
    # A caption paragraph that only repeats the image's alt text is dropped (alt stays for the eBook).
    for im in root.find_all("img"):
        p = im.find_parent("p")
        nxt = p.find_next_sibling() if p else None
        if nxt is not None and nxt.name == "p" and text(nxt) and text(nxt) == (im.get("alt") or "").strip():
            nxt["class"] = "cap"
    # Junk paragraphs and headings.
    for p in root.find_all(["p", "h1", "h2", "h3"]):
        tx = text(p)
        if tx and JUNK_RE.search(tx) and not KEEP_RE.search(tx):
            p.decompose()
    # Small "counts" tables on title pages (e.g. 7 TOPICS | 175 CLUES) and curriculum-basis tables.
    for tb in root.find_all("table"):
        tx = text(tb)
        if re.search(r"Curriculum basis|\d+ CLUES|PER TOPIC", tx):
            tb.decompose()
    drop_columns(root, {"level", "cognitive level", "cognitive demand", "question level"})
    # Remove thinking-skill labels wherever they appear in running text.
    for s in list(root.find_all(string=True)):
        new = re.sub(r"\s*[|•·;,]?\s*Cognitive (demand|level):\s*(Higher|Lower)-order\b", "", s)
        new = re.sub(r"\s*[|•·]\s*(LOTS|HOTS)\b", "", new)
        new = re.sub(r"\b(LOTS|HOTS)\s*[|•·]\s*", "", new)
        new = re.sub(r"^\s*(LOTS|HOTS)\s*$", "", new)
        if new != s:
            s.replace_with(new)
    writing_lines(root)
    for p in root.find_all("p"):
        if not text(p) and not p.find("img"):
            p.decompose()
    return root


def drop_columns(root: Tag, names: set[str]) -> None:
    for tb in root.find_all("table"):
        rows = tb.find_all("tr")
        if not rows:
            continue
        head = rows[0].find_all(["th", "td"])
        idx = [i for i, c in enumerate(head) if text(c).lower() in names]
        for r in rows:
            cells = r.find_all(["th", "td"])
            for i in sorted(idx, reverse=True):
                if i < len(cells):
                    cells[i].decompose()


def writing_lines(root: Tag) -> None:
    """Paragraphs made only of underscores become ruled lines; inline blanks become a short rule."""
    for p in root.find_all("p"):
        tx = text(p)
        if tx and re.fullmatch(r"[_\s]+", tx):
            p.name = "div"
            p.attrs = {"class": "wl"}
            p.clear()
    for s in list(root.find_all(string=re.compile(r"_{4,}"))):
        parts = re.split(r"(_{4,})", str(s))
        frag = []
        for part in parts:
            if re.fullmatch(r"_{4,}", part):
                span = BeautifulSoup("<span class='blank'></span>", "lxml").span
                frag.append(span)
            elif part:
                frag.append(NavigableString(part))
        for f in reversed(frag):
            s.insert_after(f)
        s.extract()
    # Merge runs of writing lines into one block with a count.
    for div in root.find_all("div", class_="wl"):
        if div.parent is None:
            continue
        n = 1
        nxt = div.find_next_sibling()
        while nxt is not None and nxt.name == "div" and nxt.get("class") == ["wl"]:
            n += 1
            gone, nxt = nxt, nxt.find_next_sibling()
            gone.decompose()
        div["data-n"] = str(n)


def demote(root: Tag, by: int = 2) -> None:
    for h in sorted(root.find_all(re.compile(r"^h[1-6]$")), key=lambda h: -int(h.name[1])):
        h.name = f"h{min(6, int(h.name[1]) + by)}"
        h.attrs.pop("id", None)


# ---------------------------------------------------------------- multiple choice
def split_br_choices(root: Tag) -> None:
    """'(A) ...<br>(B) ...' in one paragraph becomes one paragraph per choice."""
    for p in root.find_all("p"):
        if not p.find("br"):
            continue
        segs = re.split(r"<br\s*/?>", p.decode_contents())
        if sum(bool(CH_RE.match(BeautifulSoup(s, "lxml").get_text())) for s in segs) >= 2:
            for s in reversed(segs):
                if s.strip():
                    new = BeautifulSoup(f"<p>{s.strip()}</p>", "lxml").p
                    p.insert_after(new)
            p.decompose()


def strip_prefix(el: Tag, rx: re.Pattern) -> None:
    """Remove a leading number/letter label, including when it sits in its own <strong>."""
    for s in el.find_all(string=True):
        if not s.strip():
            continue
        s.replace_with(rx.sub("", s, count=1))
        break
    for st in el.find_all(["strong", "b"]):
        if not text(st):
            st.decompose()
        break


def structure_mcq(root: Tag, topic: str) -> Tag:
    split_br_choices(root)
    # Bold whole-paragraph stems: unwrap so the stem reads as normal text.
    for p in root.find_all("p"):
        kids = [k for k in p.children if not (isinstance(k, NavigableString) and not k.strip())]
        if len(kids) == 1 and isinstance(kids[0], Tag) and kids[0].name in ("strong", "b") and Q_RE.match(text(p)) and len(text(p)) > 8:
            kids[0].unwrap()
    out = BeautifulSoup("<div class='mcq'></div>", "lxml").div
    cur = None
    numbers = []
    for el in list(root.children):
        if isinstance(el, NavigableString):
            continue
        tx = text(el)
        if el.name == "p" and (m := Q_RE.match(tx)) and not CH_RE.match(tx):
            n = int(m.group(1))
            numbers.append(n)
            cur = BeautifulSoup(f"<div class='q'><div class='stem'><b class='qn'>{n}</b></div><ol class='choices'></ol></div>", "lxml").div
            strip_prefix(el, re.compile(r"^\s*\d{1,2}[.)]\s*"))
            el.name = "div"
            el["class"] = "st"
            cur.find("div", class_="stem").append(el)
            out.append(cur)
            continue
        if cur is not None and el.name == "p" and CH_RE.match(tx):
            strip_prefix(el, re.compile(r"^\s*\(?[A-D][).]\s*"))
            li = BeautifulSoup("<li></li>", "lxml").li
            for c in list(el.children):
                li.append(c)
            cur.find("ol").append(li)
            continue
        if cur is not None and not cur.find("ol").find("li"):
            cur.find("div", class_="stem").append(el)  # stem continues: table, image, extra paragraph
            continue
        cur = None
        if el.name == "p" and re.match(r"^(PART|SECTION)\s+[IVX]+\b", tx, re.I):
            el.name = "h4"
            el.string = re.sub(r"\s*\|\s*(LOWER|HIGHER)-ORDER THINKING SKILLS", "", tx, flags=re.I).replace(" | ", " · ")
        out.append(el)
    want = EXPECTED_MCQ[topic]
    if numbers != list(range(1, want + 1)):
        print(f"  ! {topic} MCQ numbering: got {len(numbers)} ({numbers[:3]}...{numbers[-3:]}), expected 1..{want}")
    bad = [q for q in out.find_all("div", class_="q") if len(q.find_all("li")) != 4]
    if bad:
        print(f"  ! {topic}: {len(bad)} questions without exactly 4 choices:",
              [text(q.find('b', class_='qn')) for q in bad][:10])
    return out


# ---------------------------------------------------------------- FRQs
FRQ_H = re.compile(r"^(?:FRQ\s*|Question\s*)?(\d+)\s*[.|—–:-]+\s*(?:(?:Long|Short)\s+FRQ\s*\d+\s*:\s*)?(.+)$", re.I)


def tidy_frq(root: Tag) -> None:
    """Give every FRQ a uniform title "FRQ n · Title" (h3.frq) and drop the file's front matter."""
    heads = [h for h in root.find_all(["h1", "h2"])]
    numbered = False
    for h in heads:
        tx = text(h)
        if (m := FRQ_H.match(tx)) and re.search(r"point", tx, re.I):
            h.string = f"FRQ {m.group(1)} · {m.group(2)}"
            h.name, h.attrs = "h3", {"class": "frq"}
            numbered = True
    if not numbered:  # Topic 2.1 style: "QUESTION 1 | LONG FRQ ... | 9 POINTS" paragraph, then an unnumbered title
        n = 0
        for h in root.find_all(["h1", "h2"]):
            prev = h.find_previous_sibling()
            m = re.match(r"QUESTION (\d+)\s*\|.*?(\d+) POINTS", text(prev) if prev else "", re.I)
            if m:
                h.string = f"FRQ {m.group(1)} · {text(h)} ({m.group(2)} points)"
                prev.decompose()
            elif h.name == "h1":
                n += 1
                pts = h.find_next(string=re.compile(r"\((\d+) points?\)"))
                extra = f" ({re.search(r'(\d+) points?', pts).group(1)} points)" if pts else ""
                h.string = f"FRQ {n} · {text(h)}{extra}"
            else:
                continue
            h.name, h.attrs = "h3", {"class": "frq"}
    first = root.find("h3", class_="frq")
    if first is not None:
        for el in list(first.find_previous_siblings()):
            el.decompose()


PART_RE = re.compile(r"^\(([a-h])\)")


def add_writing_space(root: Tag) -> None:
    """Give every lettered part ((a), (b), ...) ruled answer lines when the source left none.

    Topic 2.1's FRQs had one shared "planning space" table per question instead; it is replaced.
    """
    for p in root.find_all("p"):
        if re.match(r"RESPONSE PLANNING SPACE", text(p), re.I):
            nxt = p.find_next_sibling()
            if nxt is not None and nxt.name == "table" and not text(nxt):
                nxt.decompose()
            p.decompose()
    for p in root.find_all("p"):
        if not PART_RE.match(text(p)):
            continue
        nxt = p.find_next_sibling()
        if nxt is not None and nxt.name == "div" and "wl" in nxt.get("class", []):
            continue
        if nxt is not None and nxt.name == "p" and PART_RE.match(text(nxt)) is None and not text(nxt).startswith(("(", "Answer")):
            continue  # the part continues in another paragraph; lines go after that
        pts = re.search(r"(\d+)\s*points?", text(p), re.I)
        n = max(3, min(8, 2 * int(pts.group(1)))) if pts else 4
        p.insert_after(BeautifulSoup(f"<div class='wl' data-n='{n}'></div>", "lxml").div)


# ---------------------------------------------------------------- splitting multi-topic files
def split_by(root: Tag, pattern: str) -> dict[str, list[Tag]]:
    """Split top-level blocks at h1 headings matching pattern; group(1) gives the key."""
    groups, key = {}, None
    rx = re.compile(pattern, re.I)
    for el in list(root.children):
        if isinstance(el, NavigableString):
            continue
        if el.name == "h1" and (m := rx.search(text(el))):
            key = m.group(1)
            groups.setdefault(key, [])
            continue
        if key is not None:
            groups[key].append(el)
    return groups


def save(name: str, html: str) -> None:
    (GEN / f"{name}.html").write_text(html)


def frag(els) -> str:
    return "\n".join(str(e) for e in els)


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    rows = list(csv.reader(open(ROOT / "tools" / "sources.tsv"), delimiter="\t"))
    src = {(t, k): p for t, k, p in rows}
    for t in TOPICS:
        print("Topic", t)
        root = clean(pandoc(source(src[(t, "mcq_q")]), f"{t}_mcq_q"), f"{t}-mcq")
        mcq = structure_mcq(root, t)
        demote(mcq)
        save(f"{t}-mcq-q", str(mcq))
        for k, name in (("mcq_a", "mcq-a"), ("frq_a", "frq-a")):
            r = clean(pandoc(source(src[(t, k)]), f"{t}_{k}"), f"{t}-{name}")
            if k == "frq_a":
                tidy_frq(r)
            demote(r)
            save(f"{t}-{name}", r.decode_contents())
        r = clean(pandoc(source(src[(t, "frq_q")]), f"{t}_frq_q"), f"{t}-frq")
        tidy_frq(r)
        add_writing_space(r)
        demote(r)
        save(f"{t}-frq-q", r.decode_contents())
        r = clean(pandoc(source(src[(t, "id_q")]), f"{t}_id_q"), f"{t}-id")
        demote(r)
        save(f"{t}-id-q", r.decode_contents())

    print("Problems")
    for k, name in (("prob_q", "prob-q"), ("prob_a", "prob-a")):
        r = clean(pandoc(source(src[("all", k)]), f"all_{k}"), f"all-{name}")
        for nn, els in split_by(r, r"PROBLEM SET (\d+)").items():
            body = BeautifulSoup(f"<div>{frag(els)}</div>", "lxml").div
            demote(body, 1)  # h1 problem titles -> h2, set subtitle h2 -> h3
            for h in body.find_all("h2"):
                h.name, h["class"] = "h3", "prob"
            for h in body.find_all("h3", class_=False):
                h.name = "h4"
            if name == "prob-q":
                add_writing_space(body)
            save(f"set{nn}-{name}", body.decode_contents())
    print("Vocabulary")
    for k, name, pat in (("vocab_q", "vocab-q", r"Lesson (2\.\d+)"), ("vocab_a", "vocab-a", r"Lesson (2\.\d+)"),
                         ("id_a", "id-a", r"TOPIC (2\.\d+)")):
        r = clean(pandoc(source(src[("all", k)]), f"all_{k}"), f"all-{name}")
        for t, els in split_by(r, pat).items():
            body = BeautifulSoup(f"<div>{frag(els)}</div>", "lxml").div
            demote(body)
            save(f"{t}-{name}", body.decode_contents())
    print("Done:", len(list(GEN.glob('*.html'))), "fragments,", len(list(IMG.glob('*.png'))), "images")


if __name__ == "__main__":
    sys.exit(main())
