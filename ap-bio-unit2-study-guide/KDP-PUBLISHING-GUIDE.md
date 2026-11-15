# Publishing on Amazon KDP: AP Biology Unit 2 Study Guide

This is a **new book**, separate from Unit 1. You create it in KDP as a new title (KDP > Create > Paperback, and again for Kindle eBook). Nothing about your Unit 1 listing changes, and Unit 1 does not need to be re-uploaded.

## What's in this folder

| File | Use |
|---|---|
| `output/AP-Biology-Unit-2-Study-Guide-Interior.pdf` | Upload as the **manuscript** (paperback interior). 109 pages, 8.5" x 11", no bleed, black & white, fonts embedded. |
| `output/AP-Biology-Unit-2-Study-Guide-Cover.pdf` | Upload as the **cover** ("Upload a cover you already have"). Full-color wrap with 0.125" bleed. The spine is sized for 109 pages on white paper and carries the title and author name. |
| `output/AP-Biology-Unit-2-Study-Guide-Kindle.epub` | Upload as the **Kindle eBook manuscript**. Reflowable EPUB 3, validated with EPUBCheck (0 errors, 0 warnings). |
| `output/AP-Biology-Unit-2-Study-Guide-Kindle-Cover.jpg` | Upload as the **Kindle eBook cover** (1978 x 2560 px JPG). |
| `src/` | Editable source (HTML/CSS) for every chapter and the cover. |
| `who_am_i_data.py` | The 200 Who Am I? clues and answers. Edit here, then run `python3 make_who_am_i.py`. |
| `build.py` | Rebuilds both print PDFs: `python3 build.py`. To change the author name: `GUIDE_AUTHOR="Your Name" python3 build.py`. |
| `build_epub.py` | Rebuilds the eBook and its cover: `python3 build_epub.py` (run `build.py` first). |

> **Before you upload:** the author name is set to **"DAVID SREERAMA"**. The cover's spine width depends on page count, so **always rebuild the cover after you edit the content**. `build.py` does this automatically.

## What's different from Unit 1

- **More content:** all 11 Unit 2 topics; 101 multiple-choice questions (66 in the lessons plus a 35-question practice test) and 200 Who Am I? clues; four free-response questions; five mind maps; new Label the Cell diagrams, a Math Toolkit, and a Lab Focus chapter.
- **Cover:** full-color gradient design with a cell illustration, colored badges, and the author name at 30 pt (Unit 1 used 13 pt).
- **Spine text:** the book is thick enough (over 100 pages) for KDP to allow text on the spine, so the spine shows the title and your name.

## Paperback setup (KDP > Create > Paperback)

**Print options. Choose these exactly, or the files won't match:**
- Ink and paper: **Black & white interior with white paper**. (The cover prints in full color no matter which interior you choose. Only the inside pages are black and white, which keeps the printing cost low.)
- Trim size: **8.5 x 11 in**
- Bleed: **No bleed** (interior)
- Cover finish: **Glossy** is recommended for this colorful cover (matte also works but makes colors a little softer).
- ISBN: use KDP's **free ISBN**. It is different from Unit 1's ISBN, because every book gets its own. KDP prints the barcode in the empty lower-right area of the back cover.

**Age and grade range:** Grade 9 to Grade 12.

**Note on color:** screens show colors brighter than ink can print. The bright pinks, yellows, and cyans on the cover will look slightly softer on the printed book. This is normal; order a proof copy to see the real result.

## Listing details (copy and paste)

**Title:** AP Biology Unit 2: Cell Structure and Function

**Subtitle:** The Comprehensive Study Guide with Lessons, Mind Maps, Diagram Practice, 300+ Practice Questions, Free-Response Practice, and Full Answer Explanations

**Series (optional but recommended):** Create a series called "AP Biology Comprehensive Study Guides" and add Unit 1 as #1 and this book as #2. Amazon then links the books together on their product pages. (KDP > Bookshelf > "..." next to the book > Link to a series.)

**Author:** (match the name on the cover)

**Description:**

> See inside the cell, and master the unit that the rest of AP Biology is built on.
>
> Unit 2, Cell Structure and Function, takes you from molecules to living cells: the organelles that build, ship, and power, the membranes that decide what gets in and out, and the surprising origins of mitochondria and chloroplasts. This guide explains every idea clearly and then gives you the practice you need, including the calculations and lab analysis the AP Exam loves to test.
>
> **Inside you'll find:**
> - Focused lessons on all eleven Unit 2 topics: subcellular components, cell structure and function, cell size, plasma membranes, membrane permeability, membrane transport, facilitated diffusion, tonicity and osmoregulation, mechanisms of transport, compartmentalization, and endosymbiosis
> - Annotated diagrams, five one-page mind maps, and label-the-cell diagram practice
> - The Unit 2 Math Toolkit: surface area-to-volume ratios and water potential, with worked examples and practice problems
> - Lab Focus: diffusion and osmosis experiments to graph and analyze
> - Learning targets, misconception alerts, and exam tips for every topic
> - 101 original multiple-choice questions, each with a full explanation
> - 200 "Who Am I?" vocabulary questions with a complete answer key
> - Four free-response questions with point-by-point scoring guidelines
> - Master comparison tables, a one-page review sheet, a glossary, and a score tracker
>
> Ideal for students taking AP Biology, for summer preparation, and for review before unit tests and the AP Exam.
>
> *AP® is a registered trademark of the College Board, which is not affiliated with, and does not endorse, this product.*

**Keywords (7 slots):**
1. ap biology study guide
2. ap bio unit 2 cell structure and function
3. ap biology review book 2026 2027
4. cell membrane transport workbook
5. ap biology practice questions with answers
6. high school biology test prep
7. organelles osmosis water potential review

**Categories (suggested):**
- Books > Teen & Young Adult > Education & Reference > Study Aids
- Books > Education & Teaching > Studying & Workbooks > Test Preparation
- Books > Science & Math > Biological Sciences > Biology > Cell Biology

**Price:** this book is longer than Unit 1, so KDP's printing cost will be higher. Enter a price on KDP's pricing screen and check the royalty it shows before publishing. Most AP unit-level study guides of this length sell for about **$12.99–$16.99**.

## Things to know before publishing

1. **AI-generated content disclosure.** KDP asks whether the text, images, or translations are AI-generated. This content was drafted with AI assistance, so answer that question honestly. KDP requires the disclosure, and it isn't shown to customers.
2. **Trademark.** "AP" and "Advanced Placement" are College Board trademarks. The copyright page and back cover include the non-affiliation disclaimer. Do **not** use the College Board logo, and don't call the questions "official."
3. **Check against the current CED.** The content follows the eleven standard Unit 2 topics (2.1–2.11). Before publishing, compare the topic list with the College Board's current *AP Biology Course and Exam Description*, and ideally have a biology teacher proofread the book.
4. **Order a proof copy** (KDP > "Request printed proofs") before you publish, so you can check the cover colors, print quality, and margins.

## Kindle eBook setup (KDP > Create > Kindle eBook)

Use the **same title, subtitle, author, description, keywords, and categories** as the paperback. KDP then links the two formats on one product page.

- **Manuscript:** upload `AP-Biology-Unit-2-Study-Guide-Kindle.epub`.
- **Cover:** "Upload a cover you already have" and choose `AP-Biology-Unit-2-Study-Guide-Kindle-Cover.jpg`.
- **ISBN:** not required for Kindle eBooks. Leave it blank.
- **AI-generated content:** answer the same way as for the paperback.
- **Preview:** use KDP's online **Kindle Previewer** after you upload. Check the diagrams, tables, and the clickable table of contents on both a phone and a tablet view.
- **Price and royalty:** KDP's 70% royalty applies to list prices from **$2.99 to $9.99** (in the US). Study guides often sell for **$4.99–$7.99** as eBooks.

**How the eBook differs from the paperback:** text reflows to fit any screen, diagrams are images, and each Check Your Understanding set ends with a link to its answers. Write-in lines, blank graph grids, the blank mind map, and the label-the-cell answer lines are replaced with instructions to use a notebook or graph paper.
