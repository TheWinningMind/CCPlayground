# Images for editing in ChatGPT

These are the images used in the AP Biology Unit 2 study guide, so you can make student-friendly versions in ChatGPT (or another image tool) and send them back.

## Folders

- **`1-book-figures/`**: all 32 images currently in the book, at print resolution. `FIGURE-LIST.md` says where each one is used and what it shows.
- **`2-mind-maps-to-renumber/`**: your 10 mind maps. Their headings use the old 11-topic numbers and need renumbering (see the table below).

## Rules that keep the book accurate

1. **Keep the file name exactly the same** when you save an edited image (for example, `20_Figure-2-6_The-fluid-mosaic-model.png`). That's how I match it to its place in the book.
2. **Keep every label, with the same spelling and pointing at the same structure.** Labeled figures are referenced by the lesson text and the labeling worksheets. You can restyle labels, but don't drop, add, or move them to other structures.
3. **Keep the science the same:** the same organelles, arrows, directions (high → low, in/out), numbers, and ion counts (for example, 3 Na⁺ out, 2 K⁺ in).
4. **Keep the shape** (landscape or portrait, about the same proportions) so the page layout still works.
5. **White or very light background, high contrast.** The paperback prints in black and white, so check that the image still reads in grayscale.
6. **Large output:** at least 2,000 px wide (3,000 px is better) as PNG.
7. Don't add text that isn't in the original (no titles, watermarks, or ChatGPT captions). The book adds captions itself.

## A prompt that works well

> Redraw this biology diagram for high-school AP Biology students. Make it cleaner, more colorful, and easier to understand, in a friendly 3D illustration style with soft shading. Keep **every label exactly as written** and pointing at the same structure, keep all arrows and numbers, keep the same layout and aspect ratio, use a plain white background, and do not add any new text. Output a high-resolution PNG.

For the organelle cards (`04`–`17`, no labels), add: *"Show only the single organelle, centered, with no text."*

## Mind maps: new numbering

| File | Old heading | New heading |
|---|---|---|
| 01 | Topic 2.1: Cell Structure: Subcellular Components | Topic 2.1, Part A: Subcellular Components |
| 02 | Topic 2.2: Cell Structure and Function | Topic 2.1, Part B: Cell Structure and Function |
| 03 | Topic 2.3: Cell Size | Topic 2.2: Cell Size |
| 04 | Topic 2.4: Plasma Membranes | Topic 2.3: Plasma Membrane |
| 05 | Topic 2.5: Membrane Permeability | Topic 2.4: Membrane Permeability |
| 06 | Topic 2.6: Membrane Transport | Topic 2.5: Membrane Transport |
| 07 | Topic 2.7: Facilitated Diffusion | Topic 2.6: Facilitated Diffusion |
| 08 | Topic 2.8: Tonicity and Osmoregulation | Topic 2.7: Tonicity and Osmoregulation |
| 09 | Topic 2.9: Mechanisms of Transport | Topic 2.8: Mechanisms of Transport |
| 10 | Topics 2.10 and 2.11 (side by side) | Topic 2.9: Cell Compartmentalization and Topic 2.10: Origins of Cell Compartmentalization |

Change **both** places each topic number appears: the title banner at the top and the central bubble. Also check the small text for any other old topic numbers. Ask for at least 2,500 × 3,500 px (portrait) so the small print is sharp on paper.

## Sending them back

Zip the edited images (keeping the file names) and upload the zip to `new-material/` on the `claude/happy-hopper-8rl1se` branch, the same way as before. You can send just the ones you changed; any image you don't send stays as it is. I'll check each one for accuracy before it goes into the book.
