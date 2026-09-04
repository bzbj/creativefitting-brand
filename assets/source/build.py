#!/usr/bin/env python3
"""Compose square/circle adaptive marks from the real CreativeFitting artwork."""
from PIL import Image, ImageDraw
import os

HERE = os.path.dirname(os.path.abspath(__file__))
MASTER = Image.open(os.path.join(HERE, "wordmark.png")).convert("RGBA")  # 3132x356

# --- measured sub-regions (master px) ---
CRE = (0, 10, 1614, 282)      # "Creative"
FIT = (1664, 0, 3132, 356)    # "Fitting" (incl. inline bulb + g descender)
BULB = (2360, 0, 2640, 275)   # lightbulb glyph (with rays), padded

# --- brand colors ---
BLUE_A = (44, 160, 255)    # #2CA0FF bright
BLUE_B = (14, 99, 196)     # #0E63C4 deep
WHITE  = (255, 255, 255)
TINT   = (244, 248, 254)   # faint cool tint
SS = 3  # supersample factor

def crop(region):
    return MASTER.crop(region)

def white_silhouette(img):
    """Return a white version keeping the artwork's alpha (for reversed marks)."""
    a = img.split()[3]
    w = Image.new("RGBA", img.size, (255, 255, 255, 0))
    w.putalpha(a)
    solid = Image.new("RGBA", img.size, (255, 255, 255, 255))
    solid.putalpha(a)
    return solid

def lin_gradient(size, c0, c1, angle="diag"):
    # build small (smooth) then upscale — fast and visually identical
    n = 160
    g = Image.new("RGBA", (n, n))
    px = g.load()
    for y in range(n):
        for x in range(n):
            if angle == "diag":
                t = x / (n - 1) * 0.5 + y / (n - 1) * 0.5
            elif angle == "h":
                t = x / (n - 1)
            else:
                t = y / (n - 1)
            px[x, y] = (
                int(c0[0] + (c1[0] - c0[0]) * t),
                int(c0[1] + (c1[1] - c0[1]) * t),
                int(c0[2] + (c1[2] - c0[2]) * t),
                255,
            )
    return g.resize(size, Image.BILINEAR)

def frame_mask(size, shape, radius_frac=0.185):
    w, h = size
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    if shape == "circle":
        d.ellipse([0, 0, w - 1, h - 1], fill=255)
    else:
        r = int(min(w, h) * radius_frac)
        d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return m

def fit_into(img, box_w, box_h):
    """scale img to fit within box preserving aspect; return scaled img."""
    s = min(box_w / img.width, box_h / img.height)
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))), Image.LANCZOS)

def paste_center(canvas, img, cx, cy):
    canvas.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))

def make(shape="square", bg="light", layout="twoline", size=512):
    S = size * SS
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    # background
    if bg == "light":
        base = Image.new("RGBA", (S, S), WHITE + (255,))
    else:
        base = lin_gradient((S, S), BLUE_A, BLUE_B, "diag")
    mask = frame_mask((S, S), shape)
    canvas.paste(base, (0, 0), mask)
    if bg == "light":  # faint edge so the frame reads on white pages
        edge = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ed = ImageDraw.Draw(edge)
        w2 = max(2, int(S * 0.004))
        if shape == "circle":
            ed.ellipse([w2, w2, S - 1 - w2, S - 1 - w2], outline=(224, 233, 246, 255), width=w2)
        else:
            r = int(S * 0.185)
            ed.rounded_rectangle([w2, w2, S - 1 - w2, S - 1 - w2], radius=r,
                                 outline=(224, 233, 246, 255), width=w2)
        canvas.alpha_composite(edge)

    reverse = (bg != "light")
    cre = crop(CRE); fit = crop(FIT); bulb = crop(BULB)
    if reverse:
        cre, fit, bulb = white_silhouette(cre), white_silhouette(fit), white_silhouette(bulb)

    # bulb-only icon: less padding so the glyph fills ~1.5× more area
    if layout == "bulb":
        pad = 0.04 if shape == "square" else 0.08
    else:
        pad = 0.16 if shape == "square" else 0.205  # circle needs more inset
    inner = S * (1 - 2 * pad)
    cx = S / 2

    if layout == "twoline":
        gap = inner * 0.05
        sfac = min(inner / cre.width, inner / fit.width)
        cre_s = cre.resize((int(cre.width * sfac), int(cre.height * sfac)), Image.LANCZOS)
        fit_s = fit.resize((int(fit.width * sfac), int(fit.height * sfac)), Image.LANCZOS)
        total_h = cre_s.height + gap + fit_s.height
        top = (S - total_h) / 2
        paste_center(canvas, cre_s, cx, top + cre_s.height / 2)
        paste_center(canvas, fit_s, cx, top + cre_s.height + gap + fit_s.height / 2)

    elif layout == "emblem":  # bulb hero + two-line name
        gap = inner * 0.09
        bulb_h = inner * 0.36
        b2 = fit_into(bulb, inner, bulb_h)
        sfac = min(inner / cre.width, inner / fit.width) * 0.98
        cre_s = cre.resize((int(cre.width * sfac), int(cre.height * sfac)), Image.LANCZOS)
        fit_s = fit.resize((int(fit.width * sfac), int(fit.height * sfac)), Image.LANCZOS)
        name_gap = inner * 0.05
        total_h = b2.height + gap + cre_s.height + name_gap + fit_s.height
        top = (S - total_h) / 2
        y = top
        paste_center(canvas, b2, cx, y + b2.height / 2); y += b2.height + gap
        paste_center(canvas, cre_s, cx, y + cre_s.height / 2); y += cre_s.height + name_gap
        paste_center(canvas, fit_s, cx, y + fit_s.height / 2)

    elif layout == "bulb":  # bulb only
        b2 = fit_into(bulb, inner, inner)
        paste_center(canvas, b2, cx, S / 2)

    out = canvas.resize((size, size), Image.LANCZOS)
    return out

PNG_DIR = os.path.abspath(os.path.join(HERE, "..", "png"))
MARK_DIR = os.path.abspath(os.path.join(HERE, "..", "marks"))

def export_pngs():
    os.makedirs(PNG_DIR, exist_ok=True)
    layouts = ["twoline", "emblem", "bulb"]
    for lay in layouts:
        for sh in ["square", "circle"]:
            for bg in ["light", "blue"]:
                for size in (1024, 512):
                    img = make(sh, bg, lay, size)
                    name = f"{lay}-{sh}-{bg}-{size}.png"
                    img.save(os.path.join(PNG_DIR, name))
    # favicons — blue tile (white bulb on gradient) is legible at any size
    for px in (16, 32, 48, 64, 256):
        make("square", "blue", "bulb", px).save(os.path.join(PNG_DIR, f"favicon-{px}.png"))
    make("square", "blue", "bulb", 180).save(os.path.join(PNG_DIR, "favicon-180.png"))
    make("circle", "blue", "bulb", 512).save(os.path.join(PNG_DIR, "favicon-circle-512.png"))
    make("square", "blue", "bulb", 512).save(os.path.join(PNG_DIR, "apple-touch-512.png"))
    print("PNG exports written to", PNG_DIR)

def _defs_and_body():
    raw = open(os.path.join(HERE, "wordmark-raw.svg")).read()
    defs = raw[raw.index("<defs>") + len("<defs>"): raw.index("</defs>")]
    body = raw[raw.index("</defs>") + len("</defs>"): raw.rindex("</svg>")]
    return defs, body

def export_svgs():
    os.makedirs(MARK_DIR, exist_ok=True)
    defs, body = _defs_and_body()
    head = '<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
    # bulb.svg — crop viewBox straight onto the real bulb region
    bulb = f'''{head} width="34" height="36" viewBox="379.5 364.5 34 36" role="img" aria-label="CreativeFitting bulb">
<defs>{defs}</defs>{body}</svg>\n'''
    open(os.path.join(MARK_DIR, "bulb.svg"), "w").write(bulb)
    # two-line.svg — two nested viewports stacking Creative over Fitting
    tl = f'''{head} width="193.68" height="79.36" viewBox="0 0 193.68 79.36" role="img" aria-label="Creative Fitting">
<defs>{defs}<g id="art">{body}</g></defs>
<svg x="0" y="0" width="193.68" height="32.64" viewBox="96.36 367.56 193.68 32.64"><use xlink:href="#art"/></svg>
<svg x="8.76" y="36.64" width="176.16" height="42.72" viewBox="296.04 366.36 176.16 42.72"><use xlink:href="#art"/></svg>
</svg>\n'''
    open(os.path.join(MARK_DIR, "two-line.svg"), "w").write(tl)
    print("SVG marks written to", MARK_DIR)

if __name__ == "__main__":
    import sys
    if "export" in sys.argv:
        export_pngs()
    if "svg" in sys.argv:
        export_svgs()
    if "review" in sys.argv:
        combos = [
            ("twoline", "square", "light"), ("twoline", "circle", "light"),
            ("twoline", "square", "blue"),  ("twoline", "circle", "blue"),
            ("emblem", "square", "light"),  ("emblem", "circle", "light"),
            ("emblem", "square", "blue"),   ("bulb", "square", "light"),
            ("bulb", "circle", "blue"),
        ]
        cell = 360; cols = 5
        rows = (len(combos) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cell, rows * cell), (205, 208, 214))
        for i, (lay, sh, bg) in enumerate(combos):
            ic = make(sh, bg, lay, 320)
            base = Image.new("RGBA", ic.size, (205, 208, 214, 255)); base.alpha_composite(ic)
            r, c = divmod(i, cols)
            sheet.paste(base.convert("RGB"), (c * cell + 20, r * cell + 20))
        sheet.save(os.path.join(HERE, "_review.png"))
        print("wrote _review.png", sheet.size)
