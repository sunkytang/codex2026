from __future__ import annotations


def ema(values: list[float], period: int) -> list[float]:
    if period <= 0:
        raise ValueError("EMA period must be positive")
    if not values:
        return []

    multiplier = 2 / (period + 1)
    result = [values[0]]
    for value in values[1:]:
        result.append((value - result[-1]) * multiplier + result[-1])
    return result


def rsi(values: list[float], period: int) -> list[float]:
    if period <= 0:
        raise ValueError("RSI period must be positive")
    if len(values) < period + 1:
        return []

    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(values, values[1:]):
        change = current - previous
        gains.append(max(change, 0.0))
        losses.append(max(-change, 0.0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    output = [_rsi_from_avgs(avg_gain, avg_loss)]

    for gain, loss in zip(gains[period:], losses[period:]):
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        output.append(_rsi_from_avgs(avg_gain, avg_loss))

    return output


def _rsi_from_avgs(avg_gain: float, avg_loss: float) -> float:
    if avg_loss == 0:
        return 100.0
    relative_strength = avg_gain / avg_loss
    return 100 - (100 / (1 + relative_strength))

