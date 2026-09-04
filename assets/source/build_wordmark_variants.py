#!/usr/bin/env python3
"""Build self-contained CreativeFitting wordmark SVG variants.

The master is preserved verbatim. Solid variants replace every artwork
gradient fill with one approved colour; the dotted-i alternate adds two dots
whose diameter matches the existing i stems and whose tops align with the
nearby t ascenders.
"""

from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
MASTER = HERE / "wordmark.svg"
OUTPUT_DIR = HERE.parent / "wordmarks"

SOLID_COLOURS = {
    "blue": "#1A85EC",
    "white": "#FFFFFF",
    "black": "#000000",
}

GRADIENT_FILL = re.compile(r'fill="url\(#linear-pattern-\d+\)"')
GRADIENT_DEFINITION = re.compile(
    r"<linearGradient\b.*?</linearGradient>\s*", re.DOTALL
)
SVG_OPEN = re.compile(r"(<svg\b[^>]*>)", re.DOTALL)


def add_title(svg: str, title: str) -> str:
    """Insert an accessible title directly inside the root SVG element."""
    return SVG_OPEN.sub(rf"\1\n<title>{title}</title>", svg, count=1)


def build_solid(master: str, name: str, colour: str) -> str:
    """Replace every painted gradient path with a single process-safe fill."""
    variant, count = GRADIENT_FILL.subn(f'fill="{colour}"', master)
    if count != 21:
        raise RuntimeError(f"Expected 21 painted paths; found {count}")
    variant, definition_count = GRADIENT_DEFINITION.subn("", variant)
    if definition_count != 21:
        raise RuntimeError(
            f"Expected to remove 21 gradient definitions; found {definition_count}"
        )
    variant = add_title(variant, f"CreativeFitting solid {name} wordmark")
    return variant.replace(
        "</svg>",
        f'<!-- Approved one-colour production variant: {colour}. -->\n</svg>',
    )


def build_dotted_i(master: str) -> str:
    """Restore the two conventional i dots while retaining the bulb glyph."""
    dots = """
<!-- Alternate: restored dots above the i in Creative and the first i in Fitting. -->
<g id="restored-i-dots" aria-label="Two restored i dots">
  <circle cx="232.785156" cy="373.164063" r="2.019531" fill="url(#linear-pattern-9)"/>
  <circle cx="329.085938" cy="372.984375" r="2.019531" fill="url(#linear-pattern-10)"/>
</g>
"""
    variant = add_title(master, "CreativeFitting wordmark with restored i dots")
    return variant.replace("</svg>", f"{dots}</svg>")


def main() -> None:
    master = MASTER.read_text(encoding="utf-8")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, colour in SOLID_COLOURS.items():
        output = OUTPUT_DIR / f"wordmark-solid-{name}.svg"
        output.write_text(build_solid(master, name, colour), encoding="utf-8")

    dotted = OUTPUT_DIR / "wordmark-dotted-i.svg"
    dotted.write_text(build_dotted_i(master), encoding="utf-8")

    print(f"Wrote {len(SOLID_COLOURS) + 1} variants to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
