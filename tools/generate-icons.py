"""Erzeugt die PWA-Icons (Neon-Tetromino) mit Pillow.

    python3 tools/generate-icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "icons"
OUT.mkdir(exist_ok=True)

MAGENTA = (255, 45, 245)
CYAN = (0, 246, 255)
BG = (5, 1, 13, 255)
RENDER = 1024


def glow_at(color, size, cx, cy, spread=0.75, strength=0.55):
    """Weicher, radialer Neon-Schein an einer Position."""
    radius = int(size * spread)
    small = ImageOps.invert(
        Image.radial_gradient("L").resize((radius * 2, radius * 2), Image.Resampling.BICUBIC)
    )
    small = small.point(lambda v: int(v * strength))
    mask = Image.new("L", (size, size), 0)
    mask.paste(small, (cx - radius, cy - radius))
    layer = Image.new("RGBA", (size, size), color + (0,))
    layer.putalpha(mask)
    return layer


def tetromino(size, factor=1.0):
    """T-Stein aus vier Leuchtkacheln, zentriert."""
    mark = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(mark)
    block = size * 0.175 * factor
    gap = size * 0.018 * factor
    width = 3 * block + 2 * gap
    height = 2 * block + gap
    ox = (size - width) / 2
    oy = (size - height) / 2
    radius = block * 0.16
    stroke = max(2, int(block * 0.045))

    cells = [
        (0, 0, MAGENTA), (1, 0, MAGENTA), (2, 0, MAGENTA), (1, 1, CYAN)
    ]
    for cx, cy, color in cells:
        x0 = ox + cx * (block + gap)
        y0 = oy + cy * (block + gap)
        box = (x0, y0, x0 + block, y0 + block)
        d.rounded_rectangle(box, radius=radius, fill=color + (255,),
                            outline=(255, 255, 255, 230), width=stroke)
        inset = block * 0.16
        d.rounded_rectangle(
            (x0 + inset, y0 + inset, x0 + block - inset, y0 + block - inset),
            radius=radius * 0.7, fill=(255, 255, 255, 45)
        )
    return mark


def render(maskable=False):
    s = RENDER
    img = Image.new("RGBA", (s, s), BG)
    img = Image.alpha_composite(img, glow_at(MAGENTA, s, 0, 0, spread=0.9, strength=0.5))
    img = Image.alpha_composite(img, glow_at(CYAN, s, s, s, spread=0.9, strength=0.5))

    grid = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(grid)
    step = s // 12
    for i in range(0, s + 1, step):
        d.line([(i, 0), (i, s)], fill=(0, 246, 255, 16), width=2)
        d.line([(0, i), (s, i)], fill=(255, 45, 245, 14), width=2)
    img = Image.alpha_composite(img, grid)

    mark = tetromino(s, factor=0.72 if maskable else 1.0)
    halo = mark.filter(ImageFilter.GaussianBlur(s * 0.028))
    halo.putalpha(halo.getchannel("A").point(lambda v: int(v * 0.95)))
    img = Image.alpha_composite(img, halo)
    img = Image.alpha_composite(img, mark)
    return img


def save(img, name, size):
    img.resize((size, size), Image.Resampling.LANCZOS).convert("RGB").save(
        OUT / name, "PNG", optimize=True
    )
    print(f"{name}: {size}x{size}")


base = render()
save(base, "icon-512.png", 512)
save(base, "icon-192.png", 192)
save(base, "apple-touch-icon.png", 180)
save(render(maskable=True), "icon-maskable-512.png", 512)
