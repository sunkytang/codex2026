from __future__ import annotations

from dataclasses import dataclass

from .client import Candle
from .indicators import ema, rsi


@dataclass(frozen=True)
class Signal:
    side: str
    reason: str
    price: float


@dataclass(frozen=True)
class StrategyConfig:
    fast_ema: int
    slow_ema: int
    trend_fast_ema: int
    trend_slow_ema: int
    rsi_period: int
    long_rsi_min: float
    long_rsi_max: float
    short_rsi_min: float
    short_rsi_max: float


class EmaRsiStrategy:
    def __init__(self, config: StrategyConfig) -> None:
        self.config = config

    def evaluate(self, candles: list[Candle], trend_candles: list[Candle] | None = None) -> Signal:
        closes = [candle.close for candle in candles]
        if len(closes) < max(self.config.slow_ema, self.config.rsi_period) + 5:
            return Signal("FLAT", "not enough candles", closes[-1] if closes else 0.0)

        trend_side, trend_reason = self._trend_filter(trend_candles or candles)
        fast = ema(closes, self.config.fast_ema)
        slow = ema(closes, self.config.slow_ema)
        rsi_values = rsi(closes, self.config.rsi_period)
        price = closes[-1]
        current_rsi = rsi_values[-1]

        fast_crossed_up = fast[-2] <= slow[-2] and fast[-1] > slow[-1]
        fast_crossed_down = fast[-2] >= slow[-2] and fast[-1] < slow[-1]

        if (
            fast_crossed_up
            and self.config.long_rsi_min <= current_rsi <= self.config.long_rsi_max
        ):
            if trend_side != "LONG":
                return Signal("FLAT", f"long blocked by trend filter; {trend_reason}", price)
            return Signal(
                "LONG",
                f"EMA{self.config.fast_ema} crossed above EMA{self.config.slow_ema}; RSI={current_rsi:.1f}; {trend_reason}",
                price,
            )

        if (
            fast_crossed_down
            and self.config.short_rsi_min <= current_rsi <= self.config.short_rsi_max
        ):
            if trend_side != "SHORT":
                return Signal("FLAT", f"short blocked by trend filter; {trend_reason}", price)
            return Signal(
                "SHORT",
                f"EMA{self.config.fast_ema} crossed below EMA{self.config.slow_ema}; RSI={current_rsi:.1f}; {trend_reason}",
                price,
            )

        trend = "above" if fast[-1] > slow[-1] else "below"
        return Signal(
            "FLAT",
            f"no entry; fast EMA is {trend} slow EMA; RSI={current_rsi:.1f}",
            price,
        )

    def _trend_filter(self, candles: list[Candle]) -> tuple[str, str]:
        closes = [candle.close for candle in candles]
        required = max(self.config.trend_fast_ema, self.config.trend_slow_ema) + 2
        if len(closes) < required:
            return "FLAT", "trend filter has not enough candles"

        fast = ema(closes, self.config.trend_fast_ema)
        slow = ema(closes, self.config.trend_slow_ema)
        if fast[-1] > slow[-1] and closes[-1] > slow[-1]:
            return (
                "LONG",
                f"trend LONG: price above EMA{self.config.trend_slow_ema}",
            )
        if fast[-1] < slow[-1] and closes[-1] < slow[-1]:
            return (
                "SHORT",
                f"trend SHORT: price below EMA{self.config.trend_slow_ema}",
            )
        return "FLAT", f"trend neutral around EMA{self.config.trend_slow_ema}"
