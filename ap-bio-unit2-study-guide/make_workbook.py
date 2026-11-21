"""Generate the Free-Response Problem Workbook chapter and its answer key from the author's files.

Usage: python3 make_workbook.py
Reads  ../new-material/Unit2_All_72_Problems.docx and Unit2_All_72_Worked_Solutions.docx
Writes src/1045-problem-workbook.html and src/1145-answers-workbook.html
The generated HTML is committed, so the book builds without this step; rerun it only if the
author's source files change. Editorial corrections are listed in FIXES and FORMAT below.
"""
import html
import re
from pathlib import Path

import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent
NEW = ROOT.parent / "new-material"
SRC = ROOT / "src"

# (set, problem, part, point index) -> replacement scoring point (editorial review).
FIXES = {
    (6, 1, "c", 2): "At the highest concentration Line B levels off near 9 units, about half of Line A's 16, "
                    "consistent with roughly half as many carriers.",
}
# Table cells written with the precision the problem's data imply.
FORMAT = {
    (3, 4): {"0.5": "0.50"},
    (7, 1): {"0.1": "0.10", "0.2": "0.20", "0.3": "0.30", "0.4": "0.40", "0.5": "0.50",
             "5": "5.00", "5.2": "5.20", "5.0": "5.00", "4.8": "4.80", "4.6": "4.60"},
}
PART = re.compile(r"^\(([a-e])\)\s+(.*?)\s+\[(\d+) points?\]$")
LINES = {1: 2, 2: 3, 3: 4}  # answer lines by point value


def walk(fn):
    d = docx.Document(fn)
    for el in d.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, d)
            yield "p", p.style.name, p.text.strip(), bool(el.findall(".//" + qn("w:drawing")))
        elif tag == "tbl":
            yield "t", None, [[c.text.strip() for c in r.cells] for r in Table(el, d).rows], False


def parse_problems(fn):
    sets, prob = [], None
    for kind, style, txt, img in walk(fn):
        if kind == "t":
            prob["tables"].append(txt)
            continue
        if style == "Heading 1" and txt.startswith("PROBLEM SET"):
            m = re.match(r"PROBLEM SET (\d+) • TOPIC (.*)", txt)
            sets.append({"n": int(m.group(1)), "topic": m.group(2), "title": None, "problems": []})
            prob = None
            continue
        if style == "Heading 2" and sets and sets[-1]["title"] is None:
            sets[-1]["title"] = txt
            continue
        if style == "Heading 1" and txt.startswith("Problem"):
            m = re.match(r"Problem (\d+)\s*\|\s*(.*)", txt)
            prob = {"n": int(m.group(1)), "title": m.group(2).strip(), "meta": None, "text": [], "tables": [], "parts": []}
            sets[-1]["problems"].append(prob)
            continue
        # Figures in the source are simple flow sketches that repeat the text; the data tables carry the information.
        if prob is None or img or not txt or set(txt) <= set("_ ") or txt.startswith("Figure M"):
            continue
        if prob["meta"] is None and "POINTS" in txt:
            prob["meta"] = txt
            continue
        m = PART.match(txt)
        if m:
            prob["parts"].append({"l": m.group(1), "q": m.group(2), "pts": int(m.group(3))})
            continue
        prob["text"].append(txt)
    return sets


def parse_solutions(fn):
    sets, prob, part = [], None, None
    for kind, style, txt, img in walk(fn):
        if kind == "t" or not txt:
            continue
        if style == "Heading 1" and txt.startswith("PROBLEM SET"):
            sets.append([])
            prob = None
            continue
        if style == "Heading 1" and txt.startswith("Problem"):
            prob = []
            sets[-1].append(prob)
            part = None
            continue
        if prob is None:
            continue
        m = PART.match(txt)
        if m:
            part = {"l": m.group(1), "points": [], "calc": []}
            prob.append(part)
        elif style == "List Bullet" and part is not None:
            part["points"].append(re.sub(r"^Point \d+:\s*", "", txt))
        elif txt.startswith("Worked calculation:") and part is not None:
            part["calc"].append(txt.split(":", 1)[1].strip())
    return sets


def e(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"Ψ([spP])", lambda m: f"&Psi;<sub>{m.group(1).upper() if m.group(1) != 'p' else 'P'}</sub>", s)
    s = s.replace("Ψ", "&Psi;").replace("−", "&minus;").replace("×", "&times;").replace("÷", "&divide;")
    s = re.sub(r"SA/V", "SA:V", s)
    return s


def skills(meta: str) -> tuple[str, int, str]:
    kind = "Long" if meta.startswith("EXTENDED") else "Short"
    pts = int(re.search(r"(\d+) POINTS", meta).group(1))
    sk = re.search(r"Skill emphasis:\s*(.*)$", meta).group(1).strip()
    return kind, pts, sk


def table_html(rows, fmt):
    head = "".join(f"<th>{e(c)}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{e(fmt.get(c, c))}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f'<table class="plain wb-data"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def graph(points=None, sem=None, blank=False):
    """SVG axes for Problem 70: x = intensity 1-4, y = 0-30."""
    X0, Y0, W, H = 70, 260, 440, 230
    x = lambda v: X0 + (v - 0.5) * W / 4
    y = lambda v: Y0 - v * H / 30
    g = ['<svg viewBox="0 0 540 310" width="440" xmlns="http://www.w3.org/2000/svg">']
    if blank:
        g.append('<g stroke="#bbb" stroke-width="0.8">'
                 + "".join(f'<path d="M{X0},{Y0 - i * H / 30:.1f}h{W}"/>' for i in range(1, 31))
                 + "".join(f'<path d="M{X0 + i * W / 20:.1f},{Y0 - H}v{H}"/>' for i in range(1, 21)) + "</g>")
        g.append(f'<path d="M{X0},{Y0 - H}v{H}h{W}" stroke="#111" stroke-width="2" fill="none"/>')
    else:
        g.append('<g stroke="#ddd" stroke-width="0.8">'
                 + "".join(f'<path d="M{X0},{y(v):.1f}h{W}"/>' for v in range(5, 31, 5)) + "</g>")
        g.append(f'<path d="M{X0},{Y0 - H}v{H}h{W}" stroke="#111" stroke-width="1.6" fill="none"/>')
        g.append("".join(f'<text x="{X0 - 8}" y="{y(v) + 4:.1f}" font-size="12" text-anchor="end">{v}</text>'
                         for v in range(0, 31, 5)))
        g.append("".join(f'<text x="{x(v):.1f}" y="{Y0 + 18}" font-size="12" text-anchor="middle">{v}</text>'
                         for v in range(1, 5)))
        g.append(f'<text x="{X0 + W / 2}" y="{Y0 + 40}" font-size="13" font-weight="700" text-anchor="middle">Treatment intensity (a.u.)</text>')
        g.append(f'<text transform="translate(20,{Y0 - H / 2}) rotate(-90)" font-size="13" font-weight="700" text-anchor="middle">Mean response (a.u.)</text>')
        path = " ".join(f"{'M' if i == 0 else 'L'}{x(a):.1f},{y(b):.1f}" for i, (a, b) in enumerate(points))
        g.append(f'<path d="{path}" stroke="#111" stroke-width="2" fill="none"/>')
        for (a, b), s in zip(points, sem):
            g.append(f'<path d="M{x(a):.1f},{y(b - s):.1f}V{y(b + s):.1f}M{x(a) - 7:.1f},{y(b - s):.1f}h14M{x(a) - 7:.1f},{y(b + s):.1f}h14" stroke="#111" stroke-width="1.5"/>')
            g.append(f'<circle cx="{x(a):.1f}" cy="{y(b):.1f}" r="5" fill="#111"/>')
    g.append("</svg>")
    return "".join(g)


def main():
    P = parse_problems(NEW / "Unit2_All_72_Problems.docx")
    S = parse_solutions(NEW / "Unit2_All_72_Worked_Solutions.docx")
    assert len(P) == len(S) == 12
    out, ans, n, total = [], [], 0, 0
    out.append("""<section class="section-start">
  <div class="eyebrow">Part 3 &middot; Practice</div>
  <h1>Free-Response Problem Workbook</h1>
  <p>These 72 data-based problems are the kind of reasoning the AP free-response section rewards: read a table, calculate, explain a mechanism, predict an outcome, and design or critique an experiment. There are twelve sets of six problems. Sets 1&ndash;10 follow Topics 2.1&ndash;2.10 in order, and Sets 11 and 12 mix every topic, the way the exam does. Each set has two <strong>long problems</strong> (9 points) and four <strong>short problems</strong> (4 points), for 408 points in all.</p>
  <p>Work each set right after you finish its topic, or save Sets 11 and 12 for the week before the exam. Write on the lines provided, then score yourself with the point-by-point answers in Part 4. Every scoring point is worth 1 point, so you can see exactly what an answer needs to earn credit. The science practice codes (for example, 4.B or 6.E) tell you which AP skill each problem exercises.</p>
  <div class="box math">
    <div class="label">Formulas You Will Need</div>
    <p><strong>Cube:</strong> SA = 6<i>s</i><sup>2</sup>, V = <i>s</i><sup>3</sup> &nbsp;&middot;&nbsp; <strong>Sphere:</strong> SA = 4&pi;<i>r</i><sup>2</sup>, V = <sup>4</sup>&frasl;<sub>3</sub>&pi;<i>r</i><sup>3</sup>, so SA:V = 3&thinsp;&divide;&thinsp;<i>r</i> &nbsp;&middot;&nbsp; <strong>Rectangular solid:</strong> SA = 2(<i>lw</i> + <i>lh</i> + <i>wh</i>)</p>
    <p><strong>Water potential:</strong> &Psi; = &Psi;<sub>P</sub> + &Psi;<sub>S</sub> &nbsp;&middot;&nbsp; &Psi;<sub>S</sub> = &minus;<i>iCRT</i>, with <i>R</i> = 0.0831 L&middot;bar&middot;mol<sup>&minus;1</sup>&middot;K<sup>&minus;1</sup> and <i>T</i> in kelvins (&deg;C + 273)</p>
    <p><strong>Percent change</strong> = (final &minus; initial) &divide; initial &times; 100</p>
  </div>
  <p class="small"><em>All data are illustrative values written for practice, not results from published studies.</em></p>
""")
    ans.append("""<section class="section-start answers">
  <h1>Answers: Free-Response Problem Workbook</h1>
  <p>Each numbered point below earns 1 point. An answer earns the point if it says the same thing in different words; it does not need to match the wording exactly. For calculations, show the setup and include units.</p>
""")
    for ps, ss in zip(P, S):
        topic = f"Topic {ps['topic']}" if "–" not in ps["topic"] else "All Topics"
        out.append(f'  <h2 class="avoid">Set {ps["n"]} &middot; {topic} &middot; {e(ps["title"])}</h2>')
        ans.append(f'  <h2 class="avoid">Set {ps["n"]} &middot; {e(ps["title"])}</h2>')
        assert len(ps["problems"]) == len(ss) == 6
        for pp, sp in zip(ps["problems"], ss):
            n += 1
            kind, pts, sk = skills(pp["meta"])
            assert [a["l"] for a in pp["parts"]] == [a["l"] for a in sp]
            assert sum(a["pts"] for a in pp["parts"]) == pts
            total += pts
            out.append(f'  <div class="wb-prob"><h3>Problem {n} &middot; {e(pp["title"])}</h3>')
            out.append(f'  <div class="wb-meta">{kind} response &middot; {pts} points &middot; Science practices {e(sk)}</div>')
            for t in pp["text"]:
                out.append(f"  <p>{e(t)}</p>")
            for t in pp["tables"]:
                out.append("  " + table_html(t, FORMAT.get((ps["n"], pp["n"]), {})))
            out.append("  </div>")
            ans.append(f'  <div class="wb-ans"><h3>Problem {n} &middot; {e(pp["title"])} <span class="pts">{pts} pts</span></h3>')
            for qa, sa in zip(pp["parts"], sp):
                assert qa["pts"] == len(sa["points"]), (ps["n"], pp["n"], qa["l"])
                plural = "s" if qa["pts"] > 1 else ""
                q = e(qa["q"])
                if (ps["n"], pp["n"], qa["l"]) == (12, 4, "a"):
                    q = q.replace("on the supplied blank axes", "on the blank axes below")
                    out.append(f'  <div class="frq-part avoid"><strong>({qa["l"]})</strong> {q} <span class="pts">[{qa["pts"]} pt{plural}]</span>'
                               f'<figure style="margin:6pt 0">{graph(blank=True)}</figure></div>')
                else:
                    out.append(f'  <div class="frq-part"><strong>({qa["l"]})</strong> {q} <span class="pts">[{qa["pts"]} pt{plural}]</span></div>')
                    out.append("  " + '<div class="write"></div>' * LINES[qa["pts"]])
                items = []
                for i, pt in enumerate(sa["points"]):
                    pt = FIXES.get((ps["n"], pp["n"], qa["l"], i), pt)
                    items.append(f'<span class="wb-pt">{i + 1}</span>&thinsp;{e(pt)}')
                calc = "".join(f' <em>Worked calculation:</em> {e(c)}' for c in sa["calc"])
                ans.append(f'  <div class="a"><b class="k">({qa["l"]})</b> {" ".join(items)}{calc}</div>')
            if (ps["n"], pp["n"]) == (12, 4):
                ans.append(f'  <figure>{graph(points=[(1, 12), (2, 19), (3, 23), (4, 24)], sem=[1, 2, 2, 2])}'
                           '<figcaption><b>Model graph for Problem 70.</b> Means with &plusmn;1 SEM error bars; both axes labeled with units.</figcaption></figure>')
            ans.append("  </div>")
    assert n == 72 and total == 408, (n, total)
    out.append("</section>\n")
    ans.append("</section>\n")
    (SRC / "1045-problem-workbook.html").write_text("\n".join(out))
    (SRC / "1145-answers-workbook.html").write_text("\n".join(ans))
    print(f"{n} problems, {total} points")


if __name__ == "__main__":
    main()
