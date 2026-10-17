# AI-Generated 3D Images: Prompts and How to Add Them

The book already includes 3D-shaded illustrations of every organelle, so it is complete without any AI images. To use AI-generated 3D renders instead, generate them with the prompts below and put them in the `images/` folder. The build swaps them in automatically.

## How it works (step by step)

1. Open your image generator (Midjourney, ChatGPT/DALL·E, Gemini/Imagen, Adobe Firefly, Leonardo, and so on).
2. Paste the **shared style** text, then the prompt for one image.
3. Pick the best result. Check it for scientific accuracy using the "Must show" column (AI images often get the details wrong).
4. Save it as a PNG or JPG using the **exact file name** in the table, for example `images/mitochondrion.png`.
5. Rebuild the book:
   ```
   python3 build.py         # print interior + cover PDFs
   python3 build_epub.py    # Kindle eBook + eBook cover
   ```
   Any slot that has no image keeps the built-in illustration, so you can add images one at a time.
6. Delete or rename an image file to go back to the built-in illustration.

> **Why only these slots?** The labeled teaching diagrams (the labeled animal and plant cells, the membrane, the transport mechanisms, the Na⁺/K⁺ pump, osmosis, and endosymbiosis) stay as vector drawings. AI generators can't reliably place accurate labels, and wrong labels would cost students points. The slots below are the unlabeled "hero" pictures: the cover cell and the 14 cards in the 3D Organelle Gallery.

## Image specifications

| Slot | Aspect ratio | Minimum size | Background |
|---|---|---|---|
| `cover-cell` | about 1.4 : 1 (landscape) | 2400 × 1700 px | Solid deep royal blue `#1d2a8f`, so it blends into the cover |
| All organelle cards | 4 : 3 (landscape) | 1200 × 900 px | Soft white-to-light-gray gradient |

- **Print interior is black and white.** The paperback interior is set up for KDP's black-and-white printing (the cheapest option), so color images print in grayscale there. Choose images with strong light and dark contrast. Images stay in full color in the Kindle eBook and on the cover. If you want a color paperback interior, choose KDP's "Standard color" or "Premium color" ink when setting up the book. Nothing in the files needs to change, but the printing cost per copy is much higher.
- No text, labels, letters, or watermarks in any image.
- For Midjourney, add `--ar 4:3` (cards) or `--ar 7:5` (cover) to the end of the prompt.

## Shared style (paste before every prompt)

```
Highly detailed 3D render, scientific educational illustration, glossy semi-translucent materials, soft studio lighting with gentle rim light, subtle ambient occlusion, vibrant saturated colors, clean and accurate biology, centered subject, no text, no labels, no watermark.
```

## Prompts

| File name | Prompt | Must show (check accuracy) |
|---|---|---|
| `cover-cell` | A 3D cutaway of a eukaryotic animal cell, shown as a rounded slab viewed from above at a 30° angle, a quarter of the cell cut open to reveal the interior; a large purple nucleus with nucleolus, blue folded rough endoplasmic reticulum dotted with ribosomes, teal stacked Golgi apparatus with budding vesicles, orange capsule-shaped mitochondria with visible cristae, small green lysosomes, yellow vesicles, pink glossy cell membrane rim; isolated on a solid deep royal blue background (#1d2a8f). | No cell wall, no chloroplasts, no large central vacuole (it is an *animal* cell) |
| `nucleus` | A 3D sphere-shaped cell nucleus with a wedge cut away, showing a double nuclear envelope studded with nuclear pores, coiled purple chromatin inside, and a dense magenta nucleolus. | Double membrane, pores, nucleolus |
| `ribosome` | A 3D ribosome with a large purple subunit sitting on a smaller orange subunit, a thin yellow mRNA strand threaded between them, and a short chain of beads (polypeptide) emerging from the top. | Two unequal subunits, no membrane |
| `rough-er` | A 3D stack of flattened, gently curved blue membrane sheets (cisternae) connected at the edges, the surfaces dotted with many small dark ribosomes. | Flattened sacs, ribosomes on the outside |
| `smooth-er` | A 3D network of interconnected smooth, glossy blue membrane tubes branching like pipes, with no ribosomes on the surface. | Tubules, **no** ribosomes |
| `golgi` | A 3D Golgi apparatus: four or five curved, flattened teal membrane sacs stacked like pancakes, with small round yellow vesicles budding from the edges. | Separate stacked sacs, vesicles |
| `mitochondrion` | A 3D mitochondrion, a capsule-shaped orange organelle with the top half cut away, revealing a smooth outer membrane, a highly folded inner membrane forming cristae, and a pale matrix inside. | Two membranes, folded cristae |
| `chloroplast` | A 3D chloroplast, a lens-shaped green organelle cut open lengthwise, showing a double outer membrane, pale stroma, and several stacks of coin-like thylakoids (grana) connected by thin membranes. | Double membrane, grana stacks, stroma |
| `lysosome` | A 3D glossy green spherical vesicle cut open to show small enzyme molecules inside, suggesting an acidic digestive compartment. | Single membrane, enzymes inside |
| `central-vacuole` | A 3D plant cell cut open, rectangular with a green cellulose cell wall, a very large clear blue central vacuole filling most of the cell, a thin layer of cytoplasm pressed against the wall, the nucleus pushed to one side. | Vacuole fills most of the cell |
| `peroxisome` | A 3D pink spherical organelle with a single membrane, slightly translucent, showing a dark crystalline core inside. | Single membrane, crystalline core |
| `cytoskeleton` | Three 3D protein fibers side by side: a thick hollow blue microtubule tube, a thin twisted double strand of red bead-like actin (microfilament), and a medium rope-like orange intermediate filament. | Microtubule hollow; actin twisted beads |
| `centrosome` | A 3D pair of centrioles at right angles to each other, each a short cylinder made of nine triplets of microtubules arranged in a ring. | Two cylinders at 90°, 9 triplets |
| `plasma-membrane` | A 3D cross-section of a cell membrane: a phospholipid bilayer of pink round heads and yellow wavy tails, a large blue transmembrane protein channel spanning it, small orange cholesterol molecules between the tails, and green branched carbohydrate chains on top. | Heads out, tails in; carbohydrates on the outside only |
| `cell-wall` | A 3D block of a plant cell wall showing crisscrossing layers of green cellulose microfibrils, with a thin pink plasma membrane beneath it. | Wall *outside* the membrane |

## Before you publish

- **Accuracy:** compare every AI image with the built-in illustration and the "Must show" column. Regenerate anything that adds wrong structures (for example, chloroplasts in an animal cell, or ribosomes on smooth ER).
- **KDP disclosure:** KDP asks whether your book contains AI-generated images. If you add any, answer **yes** for images. The disclosure isn't shown to customers.
- **Rights:** check that your image generator's terms allow commercial use in a book you sell. Most paid plans do; some free tiers don't.
