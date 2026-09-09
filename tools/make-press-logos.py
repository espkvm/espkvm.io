#!/usr/bin/env python3
"""Build the logo files the press page hands out, from assets/icon.svg.

There is no rasteriser on this machine and the mark is nothing but rectangles on
a 64x64 grid, so it is drawn here: parse the rects out of the SVG, fill them into
a buffer at 2x and average it down (which is all the anti-aliasing a rounded
corner needs), and write the PNG with zlib and struct.

    python3 tools/make-press-logos.py

Writes assets/press/*.png and assets/press/espkvm-logo-on-light.svg. Everything
it writes is committed - a writer downloads these, so they cannot be generated
at build time.
"""

import os
import re
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "icon.svg")
OUT = os.path.join(ROOT, "assets", "press")

DARK = (0x0E, 0x11, 0x16)
LIGHT = (0xE6, 0xED, 0xF3)
GRID = 64.0
RADIUS = 12.0


def rects():
    svg = open(SRC, encoding="utf-8").read()
    out = []
    for m in re.finditer(r'<rect([^>]*)/>', svg):
        attrs = dict(re.findall(r'(\w+)="([^"]+)"', m.group(1)))
        if "x" not in attrs:  # the background square
            continue
        out.append(tuple(float(attrs[k]) for k in ("x", "y", "width", "height")))
    return out


def render(size, background, glyph, ss=2):
    """RGBA pixels, size x size. background=None leaves it transparent."""
    n = size * ss
    scale = n / GRID
    r = RADIUS * scale
    # Coverage buffer per channel is overkill; two masks are enough.
    bg = bytearray(n * n)
    fg = bytearray(n * n)
    if background is not None:
        for y in range(n):
            for x in range(n):
                # inside the rounded square?
                cx = min(max(x + 0.5, r), n - r)
                cy = min(max(y + 0.5, r), n - r)
                dx = x + 0.5 - cx
                dy = y + 0.5 - cy
                if dx * dx + dy * dy <= r * r:
                    bg[y * n + x] = 1
    for (gx, gy, gw, gh) in rects():
        x0, x1 = int(round(gx * scale)), int(round((gx + gw) * scale))
        y0, y1 = int(round(gy * scale)), int(round((gy + gh) * scale))
        for y in range(y0, y1):
            row = y * n
            for x in range(x0, x1):
                fg[row + x] = 1

    # Average the supersampled masks down into RGBA.
    px = bytearray(size * size * 4)
    area = ss * ss
    for y in range(size):
        for x in range(size):
            b = f = 0
            for sy in range(ss):
                base = (y * ss + sy) * n + x * ss
                for sx in range(ss):
                    b += bg[base + sx]
                    f += fg[base + sx]
            bc = b / area
            fc = f / area
            # The glyphs sit on the square, so alpha is whichever covers more.
            a = max(bc, fc)
            if a == 0:
                continue
            # Mix the glyph over the background by its own coverage.
            col = tuple(
                (glyph[i] * fc + (background[i] if background else glyph[i]) * (bc - min(bc, fc)))
                / max(fc + (bc - min(bc, fc)), 1e-6)
                for i in range(3)
            )
            o = (y * size + x) * 4
            px[o] = int(round(col[0]))
            px[o + 1] = int(round(col[1]))
            px[o + 2] = int(round(col[2]))
            px[o + 3] = int(round(a * 255))
    return bytes(px)


def write_png(path, size, px):
    raw = bytearray()
    stride = size * 4
    for y in range(size):
        raw.append(0)
        raw += px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n" +
           chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)) +
           chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
           chunk(b"IEND", b""))
    open(path, "wb").write(png)
    print("  %-46s %6d bytes" % (os.path.relpath(path, ROOT), len(png)))


def hexstr(c):
    return "#%02x%02x%02x" % c


def write_svg(path, background, glyph):
    """The same mark as vector. background=None leaves it transparent."""
    body = "\n".join(
        '    <rect x="%g" y="%g" width="%g" height="%g"/>' % r for r in rects())
    square = ('  <rect width="64" height="64" rx="12" fill="%s"/>\n' % hexstr(background)
              if background else "")
    open(path, "w", encoding="utf-8").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" '
        'height="64" role="img" aria-label="ESP-KVM">\n'
        "  <title>ESP-KVM</title>\n"
        '%s  <g fill="%s">\n%s\n  </g>\n</svg>\n' % (square, hexstr(glyph), body))
    print("  %s" % os.path.relpath(path, ROOT))


BLACK = (0x00, 0x00, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)

# name, background (None = transparent), glyph colour, PNG sizes.
# Between them these cover every background a page can have: the two squares for
# a layout that wants a badge, the four transparent ones for a layout that wants
# the mark to sit on its own colour, and black/white for one-colour printing.
VARIANTS = [
    ("espkvm-logo",            DARK,  LIGHT, (256, 512, 1024)),
    ("espkvm-logo-inverse",    LIGHT, DARK,  (512,)),
    ("espkvm-logo-on-light",   None,  DARK,  (512,)),
    ("espkvm-logo-on-dark",    None,  LIGHT, (512,)),
    ("espkvm-logo-black",      None,  BLACK, (512,)),
    ("espkvm-logo-white",      None,  WHITE, (512,)),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, bg, fg, sizes in VARIANTS:
        write_svg(os.path.join(OUT, name + ".svg"), bg, fg)
        for size in sizes:
            suffix = "-%d" % size if len(sizes) > 1 or size != 512 else "-512"
            write_png(os.path.join(OUT, "%s%s.png" % (name, suffix)),
                      size, render(size, bg, fg))


if __name__ == "__main__":
    main()
