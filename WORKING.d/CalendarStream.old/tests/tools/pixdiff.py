"""Compare screenshots pixel by pixel, before and after a change (0.2.8-beta.19, R15), so only what changed is looked at:

    tests/tools/pixdiff.py BEFORE AFTER OUT [--tol 8] [--pad 24]

BEFORE and AFTER are two PNG files, or two folders of PNGs compared by name (shots.py makes such a folder). For each
pair it prints how much changed and where; for every changed area it writes OUT/<name>-<n>.png: that area before
(left) and after (right), the changed pixels outlined in magenta. Nothing changed: no files, and it says so.
Exit code: 0 nothing changed, 1 something changed, 2 a picture is missing on one side.

A pixel counts as changed when any color channel differs by more than --tol (0–255; the default ignores the
faint differences of font smoothing). Changes close together (within --pad pixels) are one area."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

TILE = 8


def regions(mask: Image.Image, pad: int) -> list[tuple[int, int, int, int]]:
    """The changed areas of a 1-bit mask as boxes (left, top, right, bottom): tiles with a changed pixel, grown by
    `pad` and merged where they touch."""
    w, h = mask.size
    cols, rows = (w + TILE - 1) // TILE, (h + TILE - 1) // TILE
    small = mask.resize((cols, rows), Image.Resampling.BOX).point(lambda v: 255 if v else 0)
    px = small.load()
    grow = max(1, pad // TILE)
    seen: set[tuple[int, int]] = set()
    boxes = []
    for y in range(rows):
        for x in range(cols):
            if not px[x, y] or (x, y) in seen:
                continue
            stack, l, t, r, b = [(x, y)], x, y, x, y
            seen.add((x, y))
            while stack:          # every changed tile within `grow` tiles belongs to the same area
                cx, cy = stack.pop()
                l, t, r, b = min(l, cx), min(t, cy), max(r, cx), max(b, cy)
                for ny in range(max(0, cy - grow), min(rows, cy + grow + 1)):
                    for nx in range(max(0, cx - grow), min(cols, cx + grow + 1)):
                        if px[nx, ny] and (nx, ny) not in seen:
                            seen.add((nx, ny))
                            stack.append((nx, ny))
            boxes.append((max(0, l * TILE - pad), max(0, t * TILE - pad),
                          min(w, (r + 1) * TILE + pad), min(h, (b + 1) * TILE + pad)))
    return boxes


def outline(img: Image.Image, mask: Image.Image) -> Image.Image:
    """The picture with its changed pixels' edges drawn in magenta."""
    out = img.convert("RGB")
    edge = ImageChops.subtract(_dilate(mask), mask)
    out.paste((255, 0, 255), mask=edge)
    return out


def _dilate(mask: Image.Image) -> Image.Image:
    return mask.filter(ImageFilter.MaxFilter(5))


def compare(before: Path, after: Path, out: Path, tol: int, pad: int) -> int:
    """Compare one pair; returns how many areas changed."""
    a, b = Image.open(before).convert("RGB"), Image.open(after).convert("RGB")
    w, h = max(a.width, b.width), max(a.height, b.height)
    note = ""
    if a.size != b.size:
        note = f" (size {a.width}×{a.height} → {b.width}×{b.height})"
        a, b = _pad(a, w, h), _pad(b, w, h)
    diff = ImageChops.difference(a, b).convert("RGB")
    mask = Image.merge("RGB", [c.point(lambda v: 255 if v > tol else 0) for c in diff.split()]).convert("L")
    mask = mask.point(lambda v: 255 if v else 0)
    changed = mask.histogram()[255]
    if not changed:
        print(f"{before.name}: unchanged{note}")
        return 0
    boxes = regions(mask, pad)
    print(f"{before.name}: {len(boxes)} changed area{'s' if len(boxes) != 1 else ''}, {changed} pixels "
          f"({100 * changed / (w * h):.2f}%){note}")
    oa, ob = outline(a, mask), outline(b, mask)
    for n, box in enumerate(boxes, 1):
        l, t, r, bt = box
        pa, pb = oa.crop(box), ob.crop(box)
        pair = Image.new("RGB", (pa.width * 2 + 12, pa.height), (128, 128, 128))
        pair.paste(pa, (0, 0))
        pair.paste(pb, (pa.width + 12, 0))
        ImageDraw.Draw(pair).line([(pa.width + 6, 0), (pa.width + 6, pa.height)], fill=(255, 0, 255), width=2)
        name = out / f"{before.stem}-{n}.png"
        pair.save(name)
        print(f"  {n}. x {l}–{r}, y {t}–{bt} → {name}")
    return len(boxes)


def _pad(img: Image.Image, w: int, h: int) -> Image.Image:
    """A picture grown to w × h, the new part in a color no page uses, so it counts as changed."""
    big = Image.new("RGB", (w, h), (255, 0, 255))
    big.paste(img, (0, 0))
    return big


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("before"); p.add_argument("after"); p.add_argument("out")
    p.add_argument("--tol", type=int, default=8); p.add_argument("--pad", type=int, default=24)
    o = p.parse_args()
    before, after, out = Path(o.before), Path(o.after), Path(o.out)
    out.mkdir(parents=True, exist_ok=True)
    if before.is_file():
        pairs, missing = [(before, after)], [] if after.is_file() else [after.name]
        pairs = pairs if not missing else []
    else:
        names_a = {f.name for f in before.glob("*.png")}
        names_b = {f.name for f in after.glob("*.png")}
        pairs = [(before / n, after / n) for n in sorted(names_a & names_b)]
        missing = sorted(names_a ^ names_b)
    total = sum(compare(a, b, out, o.tol, o.pad) for a, b in pairs)
    for name in missing:
        print(f"{name}: only on one side")
    print(f"{len(pairs)} compared, {total} changed area{'s' if total != 1 else ''}"
          + (f", {len(missing)} missing" if missing else ""))
    return 2 if missing else 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
