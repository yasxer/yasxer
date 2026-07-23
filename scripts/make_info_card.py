"""Hand-author a neofetch-style info card SVG (490 wide).

Each line fades and slides in on a short stagger so the panel looks like
it's printing next to the portrait. STATIC=1 emits a frozen frame for
local Quick Look previews.
"""
import os
from pathlib import Path

BG = "#0d1117"
BORDER = "#30363d"
FG = "#c9d1d9"
DIM = "#8b949e"
KEY = "#39d353"     # neofetch key color
AT = "#58a6ff"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

ROWS = [
    ("Role",       "Full-Stack & Mobile Developer"),
    ("Now",        "WorldSkills Shanghai 2026 - Skill 08 (Flutter)"),
    ("Founder",    "Shipix.app / ALGSERV"),
    ("Stack",      "Flutter - Laravel - Next.js - Supabase"),
    ("Learning",   "Docker - AI integration - Payments"),
    ("Open to",    "Freelance & remote work"),
    ("Web",        "yasserhs.me"),
    ("Location",   "Algiers, Algeria"),
    ("Uptime",     "shipping since 2022"),
]

W = 490
LINE_H = 24
PAD_X, PAD_TOP = 26, 46
STATIC = os.environ.get("STATIC") == "1"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def main() -> None:
    lines = []
    y = PAD_TOP + 18

    def add(content: str) -> None:
        nonlocal y
        i = len(lines)
        anim = "" if STATIC else f' class="ln" style="animation-delay:{0.15 + i * 0.12:.2f}s"'
        lines.append(f'<g{anim}><text x="{PAD_X}" y="{y}" class="row">{content}</text></g>')
        y += LINE_H

    add(f'<tspan fill="{KEY}" font-weight="600">yasser</tspan>'
        f'<tspan fill="{DIM}">@</tspan>'
        f'<tspan fill="{AT}" font-weight="600">github</tspan>')
    add(f'<tspan fill="{DIM}">{"-" * 30}</tspan>')
    for k, v in ROWS:
        add(f'<tspan fill="{KEY}" font-weight="600">{esc(k)}</tspan>'
            f'<tspan fill="{DIM}">: </tspan><tspan fill="{FG}">{esc(v)}</tspan>')

    # neofetch color palette strip
    colors = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39d353", "#c9d1d9", "#8b949e"]
    i = len(lines)
    anim = "" if STATIC else f' class="ln" style="animation-delay:{0.15 + i * 0.12:.2f}s"'
    sw = 26
    swatches = "".join(
        f'<rect x="{PAD_X + j * sw}" y="{y - 12}" width="{sw}" height="13" fill="{c}"/>'
        for j, c in enumerate(colors)
    )
    lines.append(f"<g{anim}>{swatches}</g>")
    y += LINE_H

    H = y + 10
    style = f"""
  .row {{ font: 400 13px {MONO}; }}
  .ttl {{ font: 600 12px {MONO}; fill: {FG}; }}"""
    if not STATIC:
        style += """
  .ln  { opacity: 0; animation: in .5s ease-out forwards; }
  @keyframes in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Info card">
<style>{style}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<circle cx="22" cy="20" r="5" fill="#ff5f56"/><circle cx="42" cy="20" r="5" fill="#ffbd2e"/><circle cx="62" cy="20" r="5" fill="#27c93f"/>
<text x="82" y="24" class="ttl">yasser@github: ~/whoami</text>
{''.join(lines)}
</svg>"""
    Path("info-card.svg").write_text(svg)
    print(f"info-card.svg · {W}x{H} · static={STATIC}")


if __name__ == "__main__":
    main()
