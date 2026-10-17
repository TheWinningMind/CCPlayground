# Publishing on Amazon KDP: AP Biology Unit 2 Study Guide

## What's in this folder

| File | Use |
|---|---|
| `output/AP-Biology-Unit-2-Study-Guide-Interior.pdf` | Upload as the **manuscript** (paperback interior). 85 pages, 8.5" x 11", no bleed, fonts embedded. |
| `output/AP-Biology-Unit-2-Study-Guide-Cover.pdf` | Upload as the **cover** ("Upload a cover you already have"). Full-color wraparound with 0.125" bleed. The spine is sized for 85 pages on white paper. |
| `output/AP-Biology-Unit-2-Study-Guide-Kindle.epub` | Upload as the **Kindle eBook manuscript**. Reflowable EPUB 3, with diagrams in full color. |
| `output/AP-Biology-Unit-2-Study-Guide-Kindle-Cover.jpg` | Upload as the **Kindle eBook cover** (front panel of the print cover, 2560 px tall). |
| `AI-IMAGE-PROMPTS.md` | Prompts and file names for optional AI-generated 3D images (the cover cell and the 14 organelle cards). |
| `images/` | Put AI-generated images here. Any slot without an image keeps the built-in 3D illustration. |
| `src/` | Editable source (HTML/CSS) for every chapter and the cover. The cover title font, Lilita One, is bundled in `src/fonts/` under the SIL Open Font License, which allows commercial use. `src/defs.svg` holds the shared 3D shading used by all illustrations. |
| `build.py` | Rebuilds both PDFs: `python3 build.py`. To set the author/publisher name: `GUIDE_AUTHOR="Your Name" python3 build.py`. |
| `build_epub.py` | Rebuilds the eBook and its cover: `python3 build_epub.py` (run `build.py` first). |

> **Before you upload:** the author name is set to **"DAVID SREERAMA"**, the same as the Unit 1 book. The spine width depends on the page count, so **always rebuild after you edit content or add images**. `build.py` resizes the cover automatically.

## What's in the book

- **Front matter:** title page, copyright and trademark notice, contents, How to Use This Guide (with a four-week study plan), and Unit 2 at a Glance.
- **Part 1, The Lessons:** all eleven Unit 2 topics (2.1–2.11), each with learning targets, step-by-step explanations, misconception alerts, exam tips, key terms, and a Check Your Understanding set. Also included:
  - A labeled 3D animal cell, plant cell, and prokaryotic cell
  - A **3D Organelle Gallery** with 14 cards (structure, function, and which cells have it)
  - Worked examples for SA:V ratios and water potential
  - Diagrams of the secretory pathway, the fluid mosaic membrane, transport mechanisms, the Na⁺/K⁺ pump cycle, tonicity, endocytosis, and endosymbiosis
  - Three one-page mind maps, plus a blank one to fill in
- **Part 2, Skills and Review:** task verbs, the Unit 2 calculation toolkit, experimental design, master comparison tables, and a one-page review sheet.
- **Part 3, Practice:** 25-question multiple-choice test, three free-response questions (9 + 4 + 4 points), and 100 "Who Am I?" vocabulary clues.
- **Part 4, Answers and Reference:** explanations for all 83 multiple-choice questions, FRQ scoring guidelines, the Who Am I? key, a glossary, a score tracker, and a learning-target checklist.

## Paperback setup (KDP > Create > Paperback)

**Print options:**
- Ink and paper: **Black & white interior with white paper.** The interior art was drawn with strong light and dark contrast, so it prints clearly in grayscale. *Optional:* choose **Standard color** if you want the 3D illustrations printed in color. The PDF does not change, but the printing cost per copy is much higher, so check the royalty on KDP's pricing screen.
- Trim size: **8.5 x 11 in**
- Bleed: **No bleed** (interior)
- Cover finish: **Glossy** (it makes the bright cover colors stand out; matte is also fine)
- ISBN: use KDP's **free ISBN**. KDP prints the barcode in the empty lower-right area of the back cover.

**Age and grade range:** Grade 9 to Grade 12.

## Listing details (copy and paste)

**Title:** AP Biology Unit 2: Cell Structure and Function

**Subtitle:** The Comprehensive Illustrated Study Guide with 3D Organelle Gallery, Step-by-Step Lessons, 180+ Practice Questions, Free-Response Practice, and Full Answer Explanations

**Series (optional):** add this book and the Unit 1 book to a KDP series, such as "AP Biology Comprehensive Study Guides," so Amazon links them.

**Description:**

> See the cell from the inside out, and master AP Biology Unit 2.
>
> Unit 2 is where biology becomes cellular. This guide shows you what every organelle does, why cells stay small, how the fluid mosaic membrane controls what enters and leaves, how water moves by osmosis, and how compartments and endosymbiosis shaped the eukaryotic cell. Each idea is explained step by step, followed by the practice you need to answer exam-style questions with confidence.
>
> **Inside you'll find:**
> - Clear lessons on all eleven Unit 2 topics, from subcellular components to the origins of compartmentalization
> - A 3D Organelle Gallery and labeled 3D cutaways of animal, plant, and bacterial cells
> - Step-by-step worked examples for surface area-to-volume ratio and water potential
> - Diagrams of the secretory pathway, fluid mosaic model, passive and active transport, the sodium–potassium pump, tonicity, endocytosis, and endosymbiosis
> - Learning targets, misconception alerts, and exam tips for every topic
> - 83 original multiple-choice questions, each with a full explanation
> - 100 "Who Am I?" vocabulary questions with a complete answer key
> - Three free-response questions with point-by-point scoring guidelines
> - Three one-page mind maps, master comparison tables, a one-page review sheet, a glossary, and a score tracker
>
> Ideal for students taking AP Biology, for summer preparation, and for review before unit tests and the AP Exam.
>
> *AP® is a registered trademark of the College Board, which is not affiliated with, and does not endorse, this product.*

**Keywords (7 slots):**
1. ap biology study guide unit 2
2. ap bio cell structure and function
3. cell membrane transport review
4. organelles workbook high school
5. ap biology practice questions with answers
6. water potential osmosis practice
7. ap biology review book 2026 2027

**Categories (suggested):**
- Books > Teen & Young Adult > Education & Reference > Study Aids
- Books > Education & Teaching > Studying & Workbooks > Test Preparation
- Books > Science & Math > Biological Sciences > Cell Biology

**Price:** AP unit-level study guides usually sell for about **$9.99–$14.99**. Enter a price in KDP's pricing screen; it shows the printing cost and your royalty for this page count.

## Things to know before publishing

1. **AI-generated content disclosure.** KDP asks whether the text, images, or translations are AI-generated. The text was drafted with AI assistance, so answer that honestly. If you add AI-generated images from `AI-IMAGE-PROMPTS.md`, also answer **yes** for images. KDP requires the disclosure, and it isn't shown to customers.
2. **Trademark.** "AP" and "Advanced Placement" are College Board trademarks. Using them to describe what the book covers is common practice. The copyright page and back cover include the non-affiliation disclaimer. Do **not** use the College Board logo, and don't call the questions "official."
3. **Check against the current CED.** The content follows the eleven standard Unit 2 topics (2.1–2.11). Before publishing, compare them with the College Board's current *AP Biology Course and Exam Description*, and ideally have a biology teacher proofread the book.
4. **Order a proof copy** (KDP > "Request printed proofs") to check print quality, especially how the 3D illustrations look in grayscale.

## Kindle eBook setup (KDP > Create > Kindle eBook)

Use the **same title, subtitle, author, description, keywords, and categories** as the paperback so KDP links the two formats.

- **Manuscript:** `AP-Biology-Unit-2-Study-Guide-Kindle.epub`
- **Cover:** `AP-Biology-Unit-2-Study-Guide-Kindle-Cover.jpg`
- **ISBN:** not required. Leave it blank.
- **Preview:** use KDP's online Kindle Previewer. Check the diagrams, the Organelle Gallery, and the clickable table of contents on both phone and tablet views. Diagrams are in full color in the eBook.
- **Price:** the 70% royalty applies to list prices from **$2.99 to $9.99** (US). Study guides often sell for **$4.99–$7.99** as eBooks.

**How the eBook differs from the paperback:** text reflows to fit the screen, diagrams are color images, and each Check Your Understanding set links to its answers. Write-in lines, the blank graph grid, and the blank mind map are replaced with instructions to use paper. The Score Tracker asks readers to copy the table into a notebook.
