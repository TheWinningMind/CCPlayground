# Publishing on Amazon KDP: AP Biology Unit 2 Practice Workbook

## What's in this folder

| File | Use |
|---|---|
| `output/AP-Biology-Unit-2-Practice-Workbook-Interior.pdf` | Upload as the **manuscript** (paperback interior). 303 pages, 8.5" x 11", no bleed, fonts embedded. |
| `output/AP-Biology-Unit-2-Practice-Workbook-Cover.pdf` | Upload as the **cover** ("Upload a cover you already have"). Full-color wraparound with 0.125" bleed; the spine (0.682") is sized for 303 pages on white paper. |
| `tools/convert.py` | Converts your Word files in `../new-material/` into the HTML pieces in `src/gen/`. Run it again only if you change those Word files (needs pandoc). |
| `tools/sources.tsv` | Which Word file supplies each part of each topic. |
| `build.py` | Rebuilds the interior and the cover: `python3 build.py`. The cover's spine width follows the page count automatically. |
| `src/` | Stylesheet, cover design, fonts (Inter and Lilita One, both SIL Open Font License), converted content, and images. |
| `images/` | The three cover cells (same art as the study guide cover). |

## What's in the book

- **Front matter:** title page, copyright, contents, and How to Use This Workbook (a table of everything inside, plus a routine for each topic).
- **Part 1, Topic Practice:** one chapter per topic (2.1–2.10, Fall 2025 numbering). Each has multiple-choice questions, free-response questions with write-in lines, a problem set with answer space and graphing grids, and vocabulary clues.
- **Part 2, Unit Review:** Problem Sets 11 and 12, which combine all ten topics.
- **Part 3, Answers and Explanations:** for each topic, the answer key with explanations, FRQ scoring guidelines, worked solutions, and vocabulary answers. A score log closes the book.

| Topic | MCQ | FRQ | Problems | Who Am I? | Identity |
|---|---|---|---|---|---|
| 2.1 Cell Structure and Function | 70 | 7 | 6 | 25 | 25 |
| 2.2 Cell Size | 40 | 5 | 6 | 25 | 25 |
| 2.3 Plasma Membrane | 40 | 5 | 6 | 25 | 25 |
| 2.4 Membrane Permeability | 40 | 5 | 6 | 25 | 25 |
| 2.5 Membrane Transport | 45 | 6 | 6 | 25 | 25 |
| 2.6 Facilitated Diffusion | 35 | 5 | 6 | 25 | 25 |
| 2.7 Tonicity and Osmoregulation | 60 | 8 | 6 | 25 | 25 |
| 2.8 Mechanisms of Transport | 30 | 4 | 6 | – | 25 |
| 2.9 Cell Compartmentalization | 35 | 4 | 6 | – | 25 |
| 2.10 Origins of Cell Compartmentalization | 35 | 5 | 6 | – | 25 |
| Unit review (Problem Sets 11–12) | – | – | 12 | – | – |
| **Total** | **430** | **54** | **72** | **175** | **250** |

## Paperback setup (KDP > Create > Paperback)

- Ink and paper: **Black & white interior with white paper.**
- Trim size: **8.5 x 11 in**. Bleed: **No bleed**. Cover finish: **Matte** suits a write-in workbook (less glare when it lies open on a desk); glossy is also fine.
- ISBN: KDP's **free ISBN**. The barcode goes in the empty lower-right area of the back cover.
- Age and grade range: Grade 9 to Grade 12.

## Listing details (copy and paste)

**Title:** AP Biology Unit 2 Practice Workbook: Cell Structure and Function

**Subtitle:** 430 Multiple-Choice Questions, 54 Free-Response Questions, 72 Data and Calculation Problems, and Full Answer Explanations

> Use a title that differs from the study guide's. KDP links a paperback to its Kindle edition by matching title and author, so two paperbacks with the same title could get the study guide's Kindle edition attached to the wrong book.

**Series:** add it to the same series as the Unit 1 book and the Unit 2 study guide (for example "AP Biology Comprehensive Study Guides"), so Amazon shows them together.

**Description:**

> Practice until AP Biology Unit 2 feels easy.
>
> Knowing the facts is only half of AP Biology. The other half is using them: reading data, explaining a result, calculating a ratio, and writing a clear free-response answer. This workbook gives you hundreds of chances to practice, organized topic by topic, with a full explanation for every question so you learn from every mistake.
>
> **Inside you'll find:**
> - 430 original multiple-choice questions, many built on data tables, graphs, and diagrams
> - 54 free-response questions with write-in lines and point-by-point scoring guidelines
> - 72 data and calculation problems (surface area-to-volume ratio, water potential, transport rates, and more) with worked solutions
> - 425 vocabulary clues: "Who Am I?" and identity challenges with answers
> - All ten Unit 2 topics in the current Fall 2025 numbering, plus two integrated review sets
> - Graphing grids, answer space, and a score log to track your progress
>
> Use it on its own or alongside *AP Biology Unit 2: Cell Structure and Function, The Comprehensive Study Guide*, which follows the same ten topics in the same order.
>
> *AP® is a registered trademark of the College Board, which is not affiliated with, and does not endorse, this product.*

**Keywords (7 slots):**
1. ap biology practice workbook
2. ap biology unit 2 practice questions
3. ap bio cell structure free response
4. water potential practice problems
5. ap biology multiple choice with answers
6. cell membrane transport worksheets
7. ap biology review 2026 2027

**Categories (suggested):**
- Books > Teen & Young Adult > Education & Reference > Study Aids
- Books > Education & Teaching > Studying & Workbooks > Workbooks
- Books > Science & Math > Biological Sciences > Cell Biology

**Price:** the printing cost for 303 black-and-white pages at 8.5 x 11 is about **$4.64** (US). At KDP's 60% royalty, $16.99 earns about $5.56 per copy, $18.99 about $6.76, and $19.99 about $7.36. KDP's pricing screen shows the exact figures.

## Things to know before publishing

1. **AI-generated content disclosure.** Answer **yes** for text (drafted with AI assistance) and **yes** for images (the cover cells are AI-generated). KDP requires the disclosure; it isn't shown to customers.
2. **Trademark.** The copyright page and back cover carry the College Board non-affiliation notice. Don't use the College Board logo or call the questions "official."
3. **Check the content.** The questions come from your Word library; the converter only reformatted them. It removed title pages, editorial notes, and the LOTS/HOTS labels, and added write-in lines to the Topic 2.1 free-response questions (the only set without them). A teacher's proofread of the answer keys is still worthwhile.
4. **Order a proof copy** to check the write-in lines, graphing grids, and figures in print.

## Kindle eBook

This book is built as a **paperback only**. A write-in workbook doesn't suit a reflowable eBook: the answer lines, graphing grids, and two-column answer keys would be lost, and the many figures would make the delivery fee high. The study guide already has a Kindle edition for eBook readers.
