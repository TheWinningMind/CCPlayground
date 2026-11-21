"""Generate the Who Am I? chapter and its answer key from who_am_i_data.py.

Usage: python3 make_who_am_i.py   (then run build.py)
"""
from pathlib import Path

from who_am_i_data import SECTIONS

SRC = Path(__file__).resolve().parent / "src"

# Plain-text spellings in the data file, shown with proper symbols in the book.
PRETTY = [
    ("6s squared", "6<i>s</i><sup>2</sup>"), ("s cubed", "<i>s</i><sup>3</sup>"),
    ("4 pi r squared", "4&pi;<i>r</i><sup>2</sup>"), ("(4/3) pi r cubed", "(4/3)&pi;<i>r</i><sup>3</sup>"),
    ("Psi-S = -iCRT", "&Psi;<sub>S</sub> = &minus;<i>iCRT</i>"), ("(Psi)", "(&Psi;)"),
    ("(O2)", "(O<sub>2</sub>)"), ("(CO2)", "(CO<sub>2</sub>)"), ("from CO2", "from CO<sub>2</sub>"),
    ("Na+/K+", "Na<sup>+</sup>/K<sup>+</sup>"), ("3 Na+", "3 Na<sup>+</sup>"), ("2 K+", "2 K<sup>+</sup>"),
    ("(K+)", "(K<sup>+</sup>)"), ("H+ ", "H<sup>+</sup> "), ("-70", "&minus;70"),
    ("0.0831 liter-bars per mole-kelvin", "0.0831 L&middot;bar/mol&middot;K"),
    ("'", "&rsquo;"), ("1 to 5", "1&ndash;5"), ("10 to 100", "10&ndash;100"),
]


def pretty(s: str) -> str:
    for a, b in PRETTY:
        s = s.replace(a, b)
    return s


def main():
    q, a, n = [], [], 0
    for letter, title, items in SECTIONS:
        assert len(items) == 25, (letter, len(items))
        q.append(f'  <h2 class="wai-sec">Section {letter} &middot; {pretty(title)}</h2>')
        a.append(f"    <h4>Section {letter}</h4>")
        for clue, answer in items:
            n += 1
            q.append(f'  <p class="wq"><b class="n">{n}.</b> {pretty(clue)} <span class="blank"></span></p>')
            a.append(f"    <p><b>{n}.</b> {pretty(answer)}</p>")
    intro = """<section class="opener">
  <div class="eyebrow">Part 3 &middot; Extra Practice</div>
  <h1 style="margin-top:0.2in">Who Am I? Vocabulary Challenge</h1>
  <p class="wai-intro">Precise vocabulary earns points on the AP Biology Exam. Each of the 200 clues below describes a structure, process, molecule, or idea from Unit 2. Write the term that best fits each clue. Answers are in Part 4.</p>
  <div class="box tip"><div class="label">How to Use This Section</div><p>Work one section at a time. Mark any clue you had to guess, then reread that part of the lessons before checking the answers. Return to the marked clues a few days later.</p></div>
"""
    (SRC / "065-who-am-i.html").write_text(intro + "\n".join(q) + "\n</section>\n")
    key = """<section class="section-start answers">
  <h1>Answers: Who Am I?</h1>
  <p class="small">Accept reasonable equivalents, such as &ldquo;Golgi body&rdquo; for Golgi complex or &ldquo;ER&rdquo; with the correct type.</p>
  <div class="wai-key">
"""
    (SRC / "075-who-am-i-answers.html").write_text(key + "\n".join(a) + "\n  </div>\n</section>\n")
    print(f"Who Am I?: {n} clues")


if __name__ == "__main__":
    main()
