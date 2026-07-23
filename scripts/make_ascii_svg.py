"""Self-typing monochrome ASCII banner SVG (370 wide).

Stand-in for the photo portrait: renders "YASSER" as figlet-style ASCII
that wipes in row by row, left to right, with a block cursor riding the
wipe edge (SMIL — plays once, then freezes). Swap in make_portrait pipeline
later when a photo is available.
"""
from pathlib import Path

import pyfiglet

BG = "#0d1117"
BORDER = "#30363d"
INK = "#c9d1d9"     # monochrome — one light-gray fill, no rainbow noise
DIM = "#8b949e"
GREEN = "#39d353"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

W = 370
PAD_X, PAD_TOP = 22, 46


def render(text: str) -> list[str]:
    for font in ("ansi_shadow", "big", "standard"):
        try:
            art = pyfiglet.figlet_format(text, font=font)
            break
        except pyfiglet.FontNotFound:
            continue
    rows = [r.rstrip() for r in art.splitlines()]
    while rows and not rows[0].strip():
        rows.pop(0)
    while rows and not rows[-1].strip():
        rows.pop()
    return rows


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    rows = render("YASSER") + [""] + render("HAOUES")
    maxlen = max(len(r) for r in rows)
    inner_w = W - 2 * PAD_X
    fs = round(inner_w / (maxlen * 0.602), 2)   # monospace char ~0.602em wide
    lh = round(fs * 1.08, 2)

    parts = []
    for i, row in enumerate(rows):
        if not row.strip():
            continue
        y = PAD_TOP + 14 + i * lh
        row_w = round(len(row) * fs * 0.602, 1)
        delay = round(0.2 + i * 0.14, 2)
        dur = 0.5
        cid = f"w{i}"
        parts.append(f"""
<clipPath id="{cid}"><rect x="{PAD_X}" y="{y - lh}" width="0" height="{lh + 4}">
  <animate attributeName="width" from="0" to="{row_w}" begin="{delay}s" dur="{dur}s" fill="freeze"/>
</rect></clipPath>
<text x="{PAD_X}" y="{y}" xml:space="preserve" clip-path="url(#{cid})"
      style="font:600 {fs}px {MONO};fill:{INK}">{esc(row)}</text>
<rect x="{PAD_X}" y="{y - lh + 3}" width="{round(fs*0.602,1)}" height="{lh}" fill="{GREEN}" opacity="0">
  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.02;0.98;1" begin="{delay}s" dur="{dur}s" fill="freeze"/>
  <animate attributeName="x" from="{PAD_X}" to="{PAD_X + row_w}" begin="{delay}s" dur="{dur}s" fill="freeze"/>
</rect>""")

    total_delay = 0.2 + len(rows) * 0.14 + 0.5
    caption_y = PAD_TOP + 14 + len(rows) * lh + 16
    H = int(caption_y + 20)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="ASCII banner">
<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<circle cx="22" cy="20" r="5" fill="#ff5f56"/><circle cx="42" cy="20" r="5" fill="#ffbd2e"/><circle cx="62" cy="20" r="5" fill="#27c93f"/>
<text x="82" y="24" style="font:600 12px {MONO};fill:{INK}">yasser@github: ~/portrait</text>
{''.join(parts)}
<text x="{PAD_X}" y="{caption_y}" style="font:400 11px {MONO};fill:{DIM}" opacity="0">DZ · full-stack &amp; mobile<animate attributeName="opacity" from="0" to="1" begin="{total_delay}s" dur="0.4s" fill="freeze"/></text>
</svg>"""
    Path("yasser-ascii.svg").write_text(svg)
    print(f"yasser-ascii.svg · {W}x{H} · {len(rows)} rows · fs={fs}")


if __name__ == "__main__":
    main()
