from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass
from statistics import mean


BASE_URL = "https://fapi.binance.com"
FUTURES_SYMBOLS = ["BTCUSDT", "HYPEUSDT", "DOGEUSDT", "币安人生USDT"]


@dataclass(frozen=True)
class Frame:
    close: float
    ema9: float
    ema21: float
    ema50: float
    rsi14: float
    atr14: float
    high20: float
    low20: float
    trend: str


def get_json(path: str):
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def ema(values: list[float], period: int) -> list[float]:
    multiplier = 2 / (period + 1)
    result = [values[0]]
    for value in values[1:]:
        result.append((value - result[-1]) * multiplier + result[-1])
    return result


def rsi(values: list[float], period: int = 14) -> float:
    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(values, values[1:]):
        change = current - previous
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    def from_avgs(gain: float, loss: float) -> float:
        if loss == 0:
            return 100.0
        relative_strength = gain / loss
        return 100 - (100 / (1 + relative_strength))

    current = from_avgs(avg_gain, avg_loss)
    for gain, loss in zip(gains[period:], losses[period:]):
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        current = from_avgs(avg_gain, avg_loss)
    return current


def atr(rows: list[list], period: int = 14) -> float:
    ranges: list[float] = []
    previous_close = float(rows[0][4])
    for row in rows[1:]:
        high = float(row[2])
        low = float(row[3])
        close = float(row[4])
        ranges.append(max(high - low, abs(high - previous_close), abs(low - previous_close)))
        previous_close = close
    return mean(ranges[-period:])


def frame(rows: list[list]) -> Frame:
    closes = [float(row[4]) for row in rows]
    highs = [float(row[2]) for row in rows]
    lows = [float(row[3]) for row in rows]
    ema9 = ema(closes, 9)[-1]
    ema21 = ema(closes, 21)[-1]
    ema50 = ema(closes, 50)[-1]
    close = closes[-1]
    if close > ema9 > ema21 > ema50:
        trend = "strong_up"
    elif close > ema9 > ema21:
        trend = "up"
    elif close < ema9 < ema21 < ema50:
        trend = "strong_down"
    elif close < ema9 < ema21:
        trend = "down"
    else:
        trend = "mixed"
    return Frame(
        close=close,
        ema9=ema9,
        ema21=ema21,
        ema50=ema50,
        rsi14=rsi(closes),
        atr14=atr(rows),
        high20=max(highs[-20:]),
        low20=min(lows[-20:]),
        trend=trend,
    )


def score_symbol(symbol: str) -> dict:
    quoted = urllib.parse.quote(symbol, safe="")
    ticker = get_json(f"/fapi/v1/ticker/24hr?symbol={quoted}")
    premium = get_json(f"/fapi/v1/premiumIndex?symbol={quoted}")
    f15 = frame(get_json(f"/fapi/v1/klines?symbol={quoted}&interval=15m&limit=160"))
    f1h = frame(get_json(f"/fapi/v1/klines?symbol={quoted}&interval=1h&limit=160"))
    f4h = frame(get_json(f"/fapi/v1/klines?symbol={quoted}&interval=4h&limit=120"))

    trend_score = 0
    for current in [f15, f1h, f4h]:
        if current.trend == "strong_up":
            trend_score += 2
        elif current.trend == "up":
            trend_score += 1
        elif current.trend == "down":
            trend_score -= 1
        elif current.trend == "strong_down":
            trend_score -= 2

    rsi_score = 0
    if 45 <= f15.rsi14 <= 68:
        rsi_score += 1
    if 45 <= f1h.rsi14 <= 68:
        rsi_score += 1
    if f15.rsi14 > 75 or f1h.rsi14 > 75:
        rsi_score -= 1
    if f15.rsi14 < 30 or f1h.rsi14 < 30:
        rsi_score -= 1

    price = float(ticker["lastPrice"])
    breakout_distance = (f15.high20 - price) / price * 100
    pullback_distance = (price - f15.low20) / price * 100

    setup = "wait"
    side = "none"
    trigger = ""
    invalidation = ""
    if trend_score >= 3:
        side = "long"
        if 0 <= breakout_distance <= 0.4:
            setup = "breakout_watch"
            trigger = f"breakout_hold_above_{f15.high20:.6g}"
            invalidation = f"below_{f15.ema21:.6g}"
        elif 0.3 <= pullback_distance <= 1.5:
            setup = "pullback_watch"
            trigger = f"pullback_hold_{f15.ema21:.6g}_to_{f15.ema50:.6g}"
            invalidation = f"below_{f15.low20:.6g}"
    elif trend_score <= -3:
        side = "short"
        setup = "short_watch"
        trigger = f"retest_fail_near_{f15.ema21:.6g}"
        invalidation = f"above_{f15.high20:.6g}"

    total_score = max(0, min(10, 5 + trend_score + rsi_score))
    return {
        "symbol": symbol,
        "price": price,
        "change24h_pct": float(ticker["priceChangePercent"]),
        "quote_volume": float(ticker["quoteVolume"]),
        "funding_pct": float(premium["lastFundingRate"]) * 100,
        "score": total_score,
        "side": side,
        "setup": setup,
        "trigger": trigger,
        "invalidation": invalidation,
        "frames": {
            "15m": frame_to_dict(f15),
            "1h": frame_to_dict(f1h),
            "4h": frame_to_dict(f4h),
        },
    }


def frame_to_dict(value: Frame) -> dict:
    return {
        "close": round(value.close, 8),
        "trend": value.trend,
        "rsi14": round(value.rsi14, 1),
        "ema9": round(value.ema9, 8),
        "ema21": round(value.ema21, 8),
        "ema50": round(value.ema50, 8),
        "high20": round(value.high20, 8),
        "low20": round(value.low20, 8),
        "atr14": round(value.atr14, 8),
    }


def main() -> None:
    print(json.dumps([score_symbol(symbol) for symbol in FUTURES_SYMBOLS], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
