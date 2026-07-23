"""Render data/contributions.json as an animated terminal-style heatmap SVG.

53-week x 7-day calendar of rounded boxes, revealed with a diagonal
line-after-line slide-down (CSS keyframes that play once, then freeze).
Output: contrib-heatmap.svg (860 wide).
"""
import datetime
import json
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
#           none -> brightest (level 5 is a neon top end for the best day)

BG = "#0d1117"
BORDER = "#30363d"
FG = "#c9d1d9"
DIM = "#8b949e"
GREEN = "#39d353"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

CELL, GAP = 11, 3
STEP = CELL + GAP
W = 860

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def main() -> None:
    data = json.loads(Path("data/contributions.json").read_text())
    days = data["days"]
    best_date = data["best_day"]["date"] if data.get("best_day") else None

    first = datetime.date.fromisoformat(days[0]["date"])
    first_sunday = first - datetime.timedelta(days=(first.weekday() + 1) % 7)

    left, top = 34, 64          # room for day labels / title bar + month labels
    cells, month_labels = [], []
    seen_months = set()
    n_weeks = 0

    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        week = (date - first_sunday).days // 7
        dow = (date.weekday() + 1) % 7          # Sunday = 0
        n_weeks = max(n_weeks, week + 1)
        x, y = left + week * STEP, top + dow * STEP

        level = d["level"]
        if best_date and d["date"] == best_date and d["count"] > 0:
            level = 5                            # neon top end for the best day
        delay = round((week + dow) * 0.018, 3)   # diagonal stagger
        cells.append(
            f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
            f'fill="{PALETTE[level]}" style="animation-delay:{delay}s">'
            f'<title>{d["count"]} on {d["date"]}</title></rect>'
        )
        key = (date.year, date.month)
        if key not in seen_months and date.day <= 7:
            seen_months.add(key)
            month_labels.append(
                f'<text x="{x}" y="{top - 8}" class="lbl">{date.strftime("%b")}</text>'
            )

    grid_w = left + n_weeks * STEP
    footer_y = top + 7 * STEP + 24
    H = footer_y + 22

    day_labels = "".join(
        f'<text x="{left - 8}" y="{top + i * STEP + CELL - 2}" class="lbl" text-anchor="end">{t}</text>'
        for i, t in ((1, "Mon"), (3, "Wed"), (5, "Fri"))
    )
    legend_x = grid_w - 5 * (CELL + 3) - 84
    legend = (
        f'<text x="{legend_x - 34}" y="{footer_y + 9}" class="lbl">Less</text>'
        + "".join(
            f'<rect x="{legend_x + i * (CELL + 3)}" y="{footer_y}" width="{CELL}" height="{CELL}" '
            f'rx="2.5" fill="{PALETTE[i]}"/>'
            for i in range(5)
        )
        + f'<text x="{legend_x + 5 * (CELL + 3) + 6}" y="{footer_y + 9}" class="lbl">More</text>'
    )

    stats = (
        f'{data["total"]:,} contributions in the last year'
        f'   ·   longest streak {data["longest_streak"]}d'
        f'   ·   current {data["current_streak"]}d'
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Contribution heatmap">
<style>
  .lbl {{ font: 400 10px {MONO}; fill: {DIM}; }}
  .ttl {{ font: 600 12px {MONO}; fill: {FG}; }}
  .sub {{ font: 400 11px {MONO}; fill: {DIM}; }}
  .c   {{ opacity: 0; animation: drop .45s cubic-bezier(.2,.7,.3,1) forwards; }}
  @keyframes drop {{ from {{ opacity: 0; transform: translateY(-7px); }} to {{ opacity: 1; transform: none; }} }}
</style>
<rect width="{W}" height="{H}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<circle cx="22" cy="20" r="5" fill="#ff5f56"/><circle cx="42" cy="20" r="5" fill="#ffbd2e"/><circle cx="62" cy="20" r="5" fill="#27c93f"/>
<text x="82" y="24" class="ttl">yasser@github: ~/contributions</text>
{''.join(month_labels)}
{day_labels}
{''.join(cells)}
<text x="{left}" y="{footer_y + 9}" class="sub">{esc(stats)}</text>
{legend}
</svg>"""
    Path("contrib-heatmap.svg").write_text(svg)
    print(f"contrib-heatmap.svg · {n_weeks} weeks · {W}x{H}")


if __name__ == "__main__":
    main()
