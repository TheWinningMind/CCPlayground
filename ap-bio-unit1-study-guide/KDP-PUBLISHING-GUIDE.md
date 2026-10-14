# Publishing on Amazon KDP: AP Biology Unit 1 Study Guide

## What's in this folder

| File | Use |
|---|---|
| `output/AP-Biology-Unit-1-Study-Guide-Interior.pdf` | Upload as the **manuscript** (paperback interior). 56 pages, 8.5" x 11", no bleed, black & white, fonts embedded. |
| `output/AP-Biology-Unit-1-Study-Guide-Cover.pdf` | Upload as the **cover** ("Upload a cover you already have"). Full wrap with 0.125" bleed. The spine is sized for 56 pages on white paper. |
| `src/` | Editable source (HTML/CSS) for every chapter and the cover. |
| `build.py` | Rebuilds both PDFs: `python3 build.py`. To set the author/publisher name, run `GUIDE_AUTHOR="Your Name" python3 build.py`. |

> **Before you upload:** the author name is set to **"The Winning Mind"**. If you want to publish under your own name or a different pen name, rebuild with `GUIDE_AUTHOR`. The cover's spine width depends on page count, so **always rebuild the cover after you edit the content**. `build.py` does this automatically.

## Paperback setup (KDP > Create > Paperback)

**Print options. Choose these exactly, or the files won't match:**
- Ink and paper: **Black & white interior with white paper**
- Trim size: **8.5 x 11 in**
- Bleed: **No bleed** (interior)
- Cover finish: **Matte** (glossy is also fine)
- ISBN: use KDP's **free ISBN** (KDP prints it with the barcode, so you don't add anything to the files). The barcode goes in the empty lower-right area of the back cover.

**Age and grade range:** Grade 9 to Grade 12.

## Listing details (copy and paste)

**Title:** AP Biology Unit 1: Chemistry of Life

**Subtitle:** The Comprehensive Study Guide with Lessons, Diagrams, 58 Practice Questions, Free-Response Practice, and Full Answer Explanations

**Author:** (match the name on the cover)

**Description:**

> Master the chemistry that the rest of AP Biology is built on.
>
> Unit 1, Chemistry of Life, introduces ideas you will use all year: why water's polarity makes life possible, how cells build and break down macromolecules, and how a molecule's structure determines its function. This guide explains each idea clearly and then gives you the practice you need to answer exam-style questions with confidence.
>
> **Inside you'll find:**
> - Focused lessons on all six Unit 1 topics: water and hydrogen bonding, elements of life, building and breaking macromolecules, carbohydrates, lipids, proteins, and nucleic acids
> - Annotated diagrams you can learn to draw from memory
> - Learning targets, misconception alerts, and exam tips for every topic
> - 58 original multiple-choice questions, each with a full explanation
> - Three free-response questions with point-by-point scoring guidelines
> - A guide to AP task verbs (identify, describe, explain, justify) and the claim–evidence–reasoning method
> - A master comparison of the four macromolecules, a one-page review sheet, a glossary, and a score tracker
>
> Ideal for students taking AP Biology, for summer preparation, and for review before unit tests and the AP Exam.
>
> *AP® is a registered trademark of the College Board, which is not affiliated with, and does not endorse, this product.*

**Keywords (7 slots):**
1. ap biology study guide
2. ap bio unit 1 chemistry of life
3. ap biology review book 2026 2027
4. biological macromolecules workbook
5. ap biology practice questions with answers
6. high school biology test prep
7. water properties proteins nucleic acids review

**Categories (suggested):**
- Books > Teen & Young Adult > Education & Reference > Study Aids
- Books > Education & Teaching > Studying & Workbooks > Test Preparation
- Books > Science & Math > Biological Sciences > Biology

**Price:** Most AP unit-level study guides sell for about **$9.99–$14.99**. Enter a price in KDP's pricing screen. It shows the printing cost and your royalty for this page count, so check the royalty before you publish.

## Things to know before publishing

1. **AI-generated content disclosure.** KDP asks whether the text, images, or translations are AI-generated. This content was drafted with AI assistance, so answer that question honestly. KDP requires the disclosure, and it isn't shown to customers.
2. **Trademark.** "AP" and "Advanced Placement" are College Board trademarks. Using them to describe what the book covers is common practice. The copyright page and back cover include the required non-affiliation disclaimer. Do **not** use the College Board logo, and don't call the questions "official."
3. **Check against the current CED.** The content follows the six standard Unit 1 topics (1.1–1.6). Before publishing, compare the topic list with the College Board's current *AP Biology Course and Exam Description*, and ideally have a biology teacher proofread the book.
4. **Order a proof copy** (KDP > "Request printed proofs") before you publish, so you can check print quality and margins.
5. **Kindle eBook (optional).** A fixed-layout PDF does not convert well to Kindle. If you also want an eBook, the next step would be a reflowable EPUB built from the same `src/` content.
