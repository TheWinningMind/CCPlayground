"""Generate the diagram-labeling worksheets (src/107-labeling.html) and their answer key
(src/116-labeling-answers.html) from the labeled figures in the lessons.

Usage: python3 make_labeling.py src   (rerun after editing a labeled figure)
"""
import html, re, sys
from pathlib import Path
from lxml import etree
SRC = Path(sys.argv[1])
NS = "http://www.w3.org/2000/svg"
KEEP = {"Extracellular fluid", "Cytoplasm"}  # orientation labels stay visible

def figures(fname):
    return re.findall(r"<svg[^>]*>.*?</svg>", (SRC / fname).read_text(), flags=re.S)

def text_of(t):
    return " ".join("".join(t.itertext()).split())

def stack(texts):
    """Split a run of texts into labels; vertically stacked lines (same x, <= 18 units apart) form one label."""
    out = []
    for t in texts:
        prev = out[-1][-1] if out else None
        if prev is not None and t.get("x") == prev.get("x") and 0 < float(t.get("y")) - float(prev.get("y")) <= 18:
            out[-1].append(t)
        else:
            out.append([t])
    return out


def convert(svg_src, start):
    svg_src = svg_src.replace("&nbsp;", "&#160;")
    root = etree.fromstring(svg_src.encode())
    groups = [g for g in root.iter(f"{{{NS}}}g") if g.get("fill") == "#111" and g.get("font-weight") == "700"]
    g = groups[0]
    labels, buf = [], []
    for el in list(g):
        tag = etree.QName(el).localname
        if tag == "text":
            buf.append(el)
        elif tag == "line" and buf:
            labels.extend(stack(buf)); buf = []
    labels.extend(stack(buf))
    answers, n = [], start
    for lab in labels:
        name = " ".join(text_of(t) for t in lab)
        if name in KEEP:
            continue
        first = lab[0]
        x, y = float(first.get("x")), float(first.get("y"))
        anchor = first.get("text-anchor") or g.get("text-anchor")
        cx = x if anchor == "middle" else x + 13
        for t in lab:
            g.remove(t)
        badge = etree.SubElement(g, f"{{{NS}}}g")
        etree.SubElement(badge, f"{{{NS}}}circle", cx=f"{cx}", cy=f"{y - 5}", r="12", fill="#111")
        num = etree.SubElement(badge, f"{{{NS}}}text", x=f"{cx}", y=f"{y}", fill="#fff")
        num.set("text-anchor", "middle"); num.set("font-size", "13"); num.set("font-weight", "800")
        num.text = str(n)
        answers.append((n, html.escape(name))); n += 1
    out = etree.tostring(root, encoding="unicode")
    out = re.sub(r'\sxmlns:ns\d="[^"]*"', "", out)
    return out, answers

SHEETS = [
    ("Animal Cell", "01-subcellular.html", 1, "Label the structures of the animal cell."),
    ("Plant Cell", "01-subcellular.html", 2, "Label the structures of the plant cell."),
    ("Prokaryotic Cell", "01-subcellular.html", 0, "Label the structures of the bacterial cell."),
    ("Plasma Membrane", "04-membranes.html", 0, "Label the components of the fluid mosaic membrane."),
]
pages, keys = [], []
for i, (title, f, idx, task) in enumerate(SHEETS):
    svg, ans = convert(figures(f)[idx], 1)
    bank = sorted({a for _, a in ans})
    blanks = "\n".join(f'      <p class="wq"><b class="n">{n}.</b> <span class="blank"></span></p>' for n, _ in ans)
    cls = "opener" if i == 0 else "section-start"
    intro = ('''  <div class="eyebrow">Part 3 &middot; Extra Practice</div>
  <h1 style="margin-top:0.2in">Diagram Labeling Practice</h1>
  <p>On the AP exam you must recognize structures in diagrams you have never seen before. Without looking back at the lessons, write the name of each numbered structure. Use the word bank if you get stuck; a term may be used more than once. Answers are in Part 4.</p>
''' if i == 0 else "")
    pages.append(f'''<section class="{cls}">
{intro}  <h2>Worksheet {i + 1} &middot; {title}</h2>
  <p>{task}</p>
  <figure>{svg}</figure>
  <div class="box"><div class="label">Word Bank</div><p>{" &middot; ".join(bank)}</p></div>
  <div class="cols">
{blanks}
  </div>
</section>''')
    keys.append(f"    <h4>Worksheet {i + 1} &middot; {title}</h4>\n" + "\n".join(f"    <p><b>{n}.</b> {a}</p>" for n, a in ans))
(SRC / "107-labeling.html").write_text("\n\n".join(pages) + "\n")
(SRC / "116-labeling-answers.html").write_text(f'''<section class="section-start answers">
  <h1>Answers: Diagram Labeling</h1>
  <div class="wai-key">
{chr(10).join(keys)}
  </div>
</section>
''')
print([len(k.splitlines()) - 1 for k in keys])
