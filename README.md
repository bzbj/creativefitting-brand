# CreativeFitting — Brand Guidelines & Adaptive Marks

A mini brand-guideline page for the **existing** CreativeFitting logo, approved
**one-colour production variants**, a dotted-`i` alternate, and a set of
**square / circle adaptive marks** derived from the master artwork.

> Open **`index.html`** in a browser (or view the deployed page) for the full guideline.

## Why this exists
The primary wordmark is ~**8.75 : 1** — beautiful, but far too wide for an app icon, avatar,
or favicon, where it becomes tiny and flat. These adaptive marks reflow the **real logo
artwork** (same rounded letterforms, same blue gradient, same lightbulb) into shapes that
fill a square tile or a round avatar.

## Source & fidelity
All marks are built from the actual vector in
`CF-PR-2026/.kanna/uploads/CreativeFitting-Blue-logo.ai` — extracted to
`assets/source/wordmark.svg` (vector) and `wordmark.png` (transparent). **No letterforms were
re-typed.** `assets/source/build.py` composes every icon from that master (rerun to regenerate).

## The three adaptive concepts
| Mark | What | Best for |
|------|------|----------|
| **Two-line wordmark** | "Creative" over "Fitting" (bulb stays inline) | avatars, stamps, medium tiles |
| **Emblem** | Lightbulb hero + the name below | profile pictures, app splash, badges |
| **Bulb icon** | The lightbulb alone | favicon, app icon, tiny sizes |

Each comes in **square + circle** and **light (blue-on-white) + blue (white-on-gradient)**.

## Wordmark variants

| Asset | Colour / treatment | Intended use |
|------|---------------------|--------------|
| `wordmark-solid-blue.svg` | Solid `#1A85EC` | One-colour brand printing |
| `wordmark-solid-white.svg` | Solid `#FFFFFF` | Knockout on dark solid backgrounds |
| `wordmark-solid-black.svg` | Solid `#000000` | Monochrome reproduction |
| `wordmark-dotted-i.svg` | Original gradient + two restored dots | Legibility-led alternate wordmark |

The dotted-`i` alternate restores the dot above the `i` in **Creative** and the
first `i` in **Fitting**. The lightbulb, which occupies the second `i` position
in **Fitting**, is unchanged.

## File map
```
creativefitting-brand/
├─ index.html                     ← the guideline page (start here)
├─ README.md
└─ assets/
   ├─ source/
   │  ├─ wordmark.svg  wordmark.png   real logo, tight-cropped (vector + transparent PNG)
   │  ├─ build.py                     regenerates all adaptive marks from the master
   │  └─ build_wordmark_variants.py   regenerates the solid + dotted-i SVG variants
   ├─ wordmarks/
   │  ├─ wordmark-solid-{blue,white,black}.svg
   │  └─ wordmark-dotted-i.svg
   ├─ marks/
   │  ├─ two-line.svg                 vector, "Creative / Fitting" stacked
   │  └─ bulb.svg                     vector, lightbulb only
   └─ png/                            ready-to-use raster (transparent corners)
      ├─ {twoline,emblem,bulb}-{square,circle}-{light,blue}-{1024,512}.png
      ├─ favicon-256.png  favicon-64.png  favicon-circle-512.png
      └─ apple-touch-512.png
```

## Colour
| Token | Value | Use |
|-------|-------|-----|
| Brand Gradient | `#2091F7 → #116BCA` | the logo & primary surfaces (left→right) |
| Solid Blue | `#1A85EC` | approved one-colour logo; RGB 26/133/236 |
| Deep | `#0A63C4` | shadows, active states |
| Sky | `#B7DDFE` | tints, highlights |
| Ink | `#14181F` | text |
| Paper | `#FFFFFF` | backgrounds |

## Usage
- **Wide layouts** → the primary wordmark (`assets/source/wordmark.svg`).
- **One-colour print / fabrication** → an approved SVG from `assets/wordmarks/`.
- **Square / round slots** → a two-line or emblem mark from `assets/png/`.
- **≤ 32 px** → the bulb (`favicon-64.png` / `bulb.svg`).
- Reverse to white by placing the blue art on the brand gradient (the light/blue PNG pairs
  already provide both; in CSS, `filter: brightness(0) invert(1)` turns the wordmark white).

For process-print quoting, `#1A85EC` converts approximately to CMYK
`89 / 44 / 0 / 7`; use the printer's ICC profile and approve a physical proof
before production. The black variant should reproduce as `100% K` where a true
single-ink black plate is required.

Regenerate the wordmark SVG set with:

```bash
python3 assets/source/build_wordmark_variants.py
```

*Marks derived from the original CreativeFitting artwork · 2026.*
