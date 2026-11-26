"""Repair the author's renumbered mind maps, whose taller title banners cover the top row of boxes.

The renumbered maps differ from the originals only in the title banner and the hub topic number.
This keeps each renumbered map, restores the original top strip (so the box headings reappear),
and writes the new title inside the original, shorter navy banner.
Usage: python3 tools/repair_mindmaps.py <original_dir> <renumbered_dir> <out_dir>
"""
import sys
from collections import Counter
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
TITLES = {  # out name: (original file, renumbered file, [banner line pairs per panel], keep renumbered as is)
    "mindmap-01": ("01_Topic_2_1_Subcellular_Components", "01_Topic_2_1_Cell_Structure_and_Function_Components", None),
    "mindmap-02": ("02_Topic_2_2_Cell_Structure_and_Function", "02_Topic_2_1_Cell_Structure_and_Function_Organelles",
                   [("AP Biology Unit 2  |  Topic 2.1", "Cell Structure and Function — Organelles and Processes")]),
    "mindmap-03": ("03_Topic_2_3_Cell_Size", "03_Topic_2_2_Cell_Size", [("AP Biology Unit 2  |  Topic 2.2", "Cell Size")]),
    "mindmap-04": ("04_Topic_2_4_Plasma_Membranes", "04_Topic_2_3_Plasma_Membrane", [("AP Biology Unit 2  |  Topic 2.3", "Plasma Membrane")]),
    "mindmap-05": ("05_Topic_2_5_Membrane_Permeability", "05_Topic_2_4_Membrane_Permeability", [("AP Biology Unit 2  |  Topic 2.4", "Membrane Permeability")]),
    "mindmap-06": ("06_Topic_2_6_Membrane_Transport", "06_Topic_2_5_Membrane_Transport", [("AP Biology Unit 2  |  Topic 2.5", "Membrane Transport")]),
    "mindmap-07": ("07_Topic_2_7_Facilitated_Diffusion", "07_Topic_2_6_Facilitated_Diffusion", [("AP Biology Unit 2  |  Topic 2.6", "Facilitated Diffusion")]),
    "mindmap-08": ("08_Topic_2_8_Tonicity_and_Osmoregulation", "08_Topic_2_7_Tonicity_and_Osmoregulation", [("AP Biology Unit 2  |  Topic 2.7", "Tonicity and Osmoregulation")]),
    "mindmap-09": ("09_Topic_2_9_Mechanisms_of_Transport", "09_Topic_2_8_Mechanisms_of_Transport", [("AP Biology Unit 2  |  Topic 2.8", "Mechanisms of Transport")]),
    "mindmap-10": ("10_Combined_Topics_2_10_and_2_11_Compartmentalization", "10_Topics_2_9_and_2_10_Compartmentalization",
                   [("AP Biology Unit 2  |  Topic 2.9", "Cell Compartmentalization"),
                    ("AP Biology Unit 2  |  Topic 2.10", "Origins of Cell Compartmentalization")]),
}

NEW_NAVY = (19, 56, 103)  # banner color used in the renumbered maps


def is_navy(p):
    """Banner blue: the originals use either dark navy or a brighter blue banner."""
    r, g, b = p[:3]
    return (r < 70 and g < 90 and 60 < b < 150 and b > r + 25) or (r < 120 and b > r + 60 and b > g + 30)

def navy_box(img, x0, x1, y1):
    """Bounding box of the solid navy banner: rows and columns that are mostly navy (ignores navy text)."""
    px = img.load()
    rows = [y for y in range(y1) if sum(is_navy(px[x, y]) for x in range(x0, x1, 3)) > 0.5 * (x1 - x0) / 3]
    ya, yb = min(rows), max(rows)
    cols = [x for x in range(x0, x1) if sum(is_navy(px[x, y]) for y in range(ya, yb + 1, 2)) > 0.6 * (yb - ya) / 2]
    return min(cols), ya, max(cols), yb

def write(draw, lines, box, color):
    x0, y0, x1, y1 = box
    for size in range(60, 8, -1):
        f = ImageFont.truetype(FONT, size)
        ws = [draw.textlength(l, font=f) for l in lines]
        if max(ws) <= x1 - x0 and size * 1.25 * len(lines) <= y1 - y0:
            break
    y = y0 + ((y1 - y0) - size * 1.25 * len(lines)) / 2 + size * 0.08
    for l, w in zip(lines, ws):
        draw.text((x0 + (x1 - x0 - w) / 2, y), l, font=f, fill=color); y += size * 1.25

def repair(orig, new, panels, out):
    O = Image.open(orig).convert("RGB"); N = Image.open(new).convert("RGB")
    if panels is None:
        N.save(out, optimize=True); return
    W, H = N.size; strip = int(H * (0.16 if W < H else 0.2))
    N.paste(O.crop((0, 0, W, strip)), (0, 0))          # original top strip: headings visible again
    d = ImageDraw.Draw(N)
    for i, lines in enumerate(panels):
        px0, px1 = (0, W) if len(panels) == 1 else ((0, W // 2) if i == 0 else (W // 2, W))
        bx = navy_box(O, px0, px1, strip)
        # repaint the whole original banner in the renumbered maps' navy so all ten match
        d.rounded_rectangle((bx[0], bx[1], bx[2], bx[3]), radius=max(8, (bx[3] - bx[1]) // 5), fill=NEW_NAVY)
        inner = (bx[0] + 14, bx[1] + 6, bx[2] - 14, bx[3] - 6)
        write(d, list(lines), (inner[0] + 12, inner[1] + 4, inner[2] - 12, inner[3] - 4), "white")
    N.save(out, optimize=True)

if __name__ == "__main__":
    od, nd, out = map(Path, sys.argv[1:4]); out.mkdir(parents=True, exist_ok=True)
    for name, (o, n, panels) in TITLES.items():
        repair(od / f"{o}.png", nd / f"{n}.png", panels, out / f"{name}.png"); print("repaired", name)
