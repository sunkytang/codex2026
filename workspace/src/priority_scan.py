from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone, timedelta

from .pro_analysis import score_symbol


PRIORITY_SYMBOLS = ["HYPEUSDT", "TRUMPUSDT", "TURBOUSDT"]


def sub_scores(item: dict) -> tuple[int, int, int]:
    frames = item["frames"]
    f15 = frames["15m"]
    f1h = frames["1h"]
    trend = 0
    for frame in [f15, f1h]:
        if frame["trend"] == "strong_up":
            trend += 2
        elif frame["trend"] == "up":
            trend += 1
        elif frame["trend"] == "strong_down":
            trend -= 2
        elif frame["trend"] == "down":
            trend -= 1
    trend_score = max(0, min(4, trend + 2))

    price = float(item["price"])
    position_score = 1
    trigger = item.get("trigger", "")
    if item["symbol"] == "HYPEUSDT":
        if 61.50 <= price <= 61.80 or 62.45 <= price <= 62.75:
            position_score = 3
        elif 61.20 <= price <= 62.90:
            position_score = 2
    elif item["symbol"] == "TRUMPUSDT":
        if 1.90 <= price <= 1.925:
            position_score = 3
        elif 1.887 <= price <= 1.94:
            position_score = 2
    elif item["symbol"] == "TURBOUSDT":
        if 0.001060 <= price <= 0.0010715:
            position_score = 3
        elif 0.001048 <= price <= 0.00108:
            position_score = 2
    if trigger:
        position_score = max(position_score, 2)

    risk_score = 3
    funding = abs(float(item.get("funding_pct", 0)))
    quote_volume = float(item.get("quote_volume", 0))
    if funding > 0.03:
        risk_score -= 1
    if quote_volume < 10_000_000:
        risk_score -= 1
    risk_score = max(0, min(3, risk_score))
    return trend_score, position_score, risk_score


def action_line(item: dict) -> str:
    symbol = item["symbol"]
    price = float(item["price"])
    if symbol == "HYPEUSDT":
        if price >= 62.60:
            return "breakout_trigger_watch"
        if 61.50 <= price <= 61.80:
            return "pullback_trigger_watch"
        return "wait"
    if symbol == "TRUMPUSDT":
        if price >= 1.925:
            return "breakout_trigger_watch"
        if 1.90 <= price <= 1.91:
            return "support_reclaim_watch"
        return "wait"
    if symbol == "TURBOUSDT":
        if price >= 0.0010708:
            return "breakout_trigger_watch"
        if 0.001054 <= price <= 0.001060:
            return "pullback_trigger_watch"
        return "near_breakout_watch" if price >= 0.001067 else "wait"
    return "wait"


def scan_once() -> list[dict]:
    rows = []
    for symbol in PRIORITY_SYMBOLS:
        item = score_symbol(symbol)
        trend_score, position_score, risk_score = sub_scores(item)
        rows.append(
            {
                "symbol": symbol,
                "price": item["price"],
                "score": item["score"],
                "tpr": f"T{trend_score} P{position_score} R{risk_score}",
                "bias": item["side"],
                "setup": item["setup"],
                "trigger": item["trigger"],
                "invalidation": item["invalidation"],
                "action": action_line(item),
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Short high-frequency priority futures scanner.")
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--cycles", type=int, default=6)
    args = parser.parse_args()

    tz = timezone(timedelta(hours=8))
    for index in range(args.cycles):
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        print(json.dumps({"time_bjt": now, "rows": scan_once()}, ensure_ascii=False), flush=True)
        if index != args.cycles - 1:
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
