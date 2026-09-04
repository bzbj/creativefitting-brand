#!/usr/bin/env python3
"""Generate a BOLD lightbulb icon (vector) + favicon set, replacing the thin one."""
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MARKS = os.path.join(ROOT, "assets", "marks")
PNG = os.path.join(ROOT, "assets", "png")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- bold bulb geometry (native viewBox 0 0 100 100), bbox ~ x[8,92] y[6,76], center (50,41) ---
BULB = '''<g fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">
  <path d="M37 63 C 28 55 26 38 38 30 C 46 24.5 54 24.5 62 30 C 74 38 72 55 63 63 Z"/>
  <path d="M41 63 L41 71 Q41 76 46 76 L54 76 Q59 76 59 71 L59 63"/>
  <path d="M43 69.5 H57"/>
  <path d="M50 15 V6"/><path d="M75 24 L81 18"/><path d="M25 24 L19 18"/>
  <path d="M83 45 H92"/><path d="M17 45 H8"/>
</g>'''

GRADS = ('<linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#2CA0FF"/><stop offset="1" stop-color="#0E63C4"/></linearGradient>'
         '<linearGradient id="blue" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="#2091F7"/><stop offset="1" stop-color="#116BCA"/></linearGradient>')

def bulb_group(stroke, sw, s, cy=52):
    tx = 50 - 50 * s
    ty = cy - 41 * s
    return f'<g transform="translate({tx:.3f},{ty:.3f}) scale({s})">{BULB.format(stroke=stroke, sw=sw)}</g>'

def icon_svg(shape, bg, size=None):
    dim = f' width="{size}" height="{size}"' if size else ''
    if shape == "square":
        s, sw = 0.84, 10
        frame_fill = ('<rect width="100" height="100" rx="22" fill="url(#tile)"/>' if bg == "blue"
                      else '<rect width="100" height="100" rx="22" fill="#fff"/>'
                           '<rect x="1.5" y="1.5" width="97" height="97" rx="20.5" fill="none" stroke="#E0E9F6" stroke-width="1.5"/>')
    else:
        s, sw = 0.78, 11
        frame_fill = ('<circle cx="50" cy="50" r="50" fill="url(#tile)"/>' if bg == "blue"
                      else '<circle cx="50" cy="50" r="50" fill="#fff"/>'
                           '<circle cx="50" cy="50" r="49" fill="none" stroke="#E0E9F6" stroke-width="1.5"/>')
    stroke = "#fff" if bg == "blue" else "url(#blue)"
    return (f'<svg xmlns="http://www.w3.org/2000/svg"{dim} viewBox="0 0 100 100" role="img" aria-label="CreativeFitting">'
            f'<defs>{GRADS}</defs>{frame_fill}{bulb_group(stroke, sw, s)}</svg>')

def plain_bulb_svg():
    # transparent, blue gradient bulb, tight viewBox
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="88" height="76" viewBox="6 4 88 76" '
            f'role="img" aria-label="lightbulb"><defs>{GRADS}</defs>'
            f'{BULB.format(stroke="url(#blue)", sw=8)}</svg>')

def render(svg_text, out_png, px):
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, dir=HERE) as f:
        f.write(svg_text); tmp = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=1", f"--window-size={px},{px}",
                    "--default-background-color=00000000", f"--screenshot={out_png}",
                    f"file://{tmp}"], stderr=subprocess.DEVNULL)
    os.remove(tmp)

if __name__ == "__main__":
    os.makedirs(MARKS, exist_ok=True); os.makedirs(PNG, exist_ok=True)
    # vector marks
    open(os.path.join(MARKS, "bulb-bold.svg"), "w").write(plain_bulb_svg())
    for shape in ("square", "circle"):
        for bg in ("light", "blue"):
            open(os.path.join(MARKS, f"icon-bulb-{shape}-{bg}.svg"), "w").write(icon_svg(shape, bg))
    # primary favicon = blue square tile
    fav = icon_svg("square", "blue")
    open(os.path.join(ROOT, "favicon.svg"), "w").write(fav)

    # favicon PNGs (build each SVG sized to its target so it scales to fill)
    for px in (16, 32, 48, 64, 180, 192, 512):
        render(icon_svg("square", "blue", px), os.path.join(PNG, f"favicon-{px}.png"), px)
    render(icon_svg("square", "blue", 512), os.path.join(PNG, "apple-touch-512.png"), 512)
    render(icon_svg("square", "blue", 256), os.path.join(PNG, "favicon-256.png"), 256)  # overwrite old thin
    render(icon_svg("circle", "blue", 512), os.path.join(PNG, "favicon-circle-512.png"), 512)
    # replace the thin adaptive "bulb" row PNGs with bold ones
    for shape in ("square", "circle"):
        for bg in ("light", "blue"):
            for px in (1024, 512):
                render(icon_svg(shape, bg, px), os.path.join(PNG, f"bulb-{shape}-{bg}-{px}.png"), px)
    print("bold bulb icons + favicons written")
