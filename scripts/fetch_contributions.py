"""Fetch the public contribution calendar — no token, no GraphQL.

GitHub serves the calendar as public HTML at
https://github.com/users/<username>/contributions
(the same fragment the profile page itself uses).
Writes data/contributions.json with raw days + derived stats.
"""
import datetime
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "yasxer"
URL = f"https://github.com/users/{USER}/contributions"


def main() -> None:
    html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    # Tooltip text ("3 contributions on July 4th.") keyed by the cell it targets.
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        tip = tips.get(td.get("id"), "")
        m = re.match(r"([\d,]+) contribution", tip)
        count = int(m.group(1).replace(",", "")) if m else 0
        days.append({"date": date, "count": count, "level": int(td.get("data-level", 0))})

    days.sort(key=lambda d: d["date"])
    total = sum(d["count"] for d in days)

    # Longest streak
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    # Current streak (today being empty doesn't break it yet)
    tail = days[:-1] if days and days[-1]["count"] == 0 else days
    current = 0
    for d in reversed(tail):
        if d["count"] > 0:
            current += 1
        else:
            break

    best = max(days, key=lambda d: d["count"]) if days else None

    out = {
        "user": USER,
        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "days": days,
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/contributions.json").write_text(json.dumps(out, indent=2))
    print(f"{total} contributions / {len(days)} days · longest streak {longest} · current {current}")


if __name__ == "__main__":
    main()
