from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .client import BinanceFuturesPublicClient, Candle
from .risk import RiskConfig, RiskManager
from .strategy import EmaRsiStrategy, StrategyConfig


@dataclass
class BacktestPosition:
    side: str
    entry_price: float
    quantity: float
    stop_loss: float
    take_profit: float
    entry_time: int


@dataclass
class BacktestTrade:
    side: str
    entry_price: float
    exit_price: float
    pnl: float
    reason: str


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_backtest(config: dict[str, Any], limit: int) -> str:
    client = BinanceFuturesPublicClient(config["base_url"])
    candles = client.klines(config["symbol"], config["interval"], limit)
    trend_candles = client.klines(config["symbol"], config["trend_interval"], limit)
    strategy = EmaRsiStrategy(StrategyConfig(**config["strategy"]))

    balance = float(config["paper_balance_usdt"])
    starting_balance = balance
    peak_balance = balance
    max_drawdown = 0.0
    position: BacktestPosition | None = None
    trades: list[BacktestTrade] = []

    warmup = max(
        int(config["strategy"]["slow_ema"]),
        int(config["strategy"]["rsi_period"]),
    ) + 5

    for index in range(warmup, len(candles)):
        candle = candles[index]

        if position is not None:
            exit_price, reason = check_exit(position, candle)
            if exit_price is not None:
                pnl = calculate_pnl(position, exit_price)
                balance += pnl
                peak_balance = max(peak_balance, balance)
                drawdown = peak_balance - balance
                max_drawdown = max(max_drawdown, drawdown)
                trades.append(
                    BacktestTrade(position.side, position.entry_price, exit_price, pnl, reason)
                )
                position = None
                continue

        if position is None:
            candle_time = candles[index].open_time
            available_trend_candles = [
                trend_candle for trend_candle in trend_candles if trend_candle.open_time <= candle_time
            ]
            signal = strategy.evaluate(candles[: index + 1], available_trend_candles)
            if signal.side in {"LONG", "SHORT"}:
                risk = RiskManager(
                    RiskConfig(
                        balance_usdt=balance,
                        leverage=int(config["leverage"]),
                        risk_per_trade_pct=float(config["risk_per_trade_pct"]),
                        max_position_margin_pct=float(config["max_position_margin_pct"]),
                        stop_loss_pct=float(config["stop_loss_pct"]),
                        take_profit_pct=float(config["take_profit_pct"]),
                    )
                )
                plan = risk.plan(signal.side, signal.price)
                position = BacktestPosition(
                    side=plan.side,
                    entry_price=plan.entry_price,
                    quantity=plan.quantity,
                    stop_loss=plan.stop_loss,
                    take_profit=plan.take_profit,
                    entry_time=candle.open_time,
                )

    wins = [trade for trade in trades if trade.pnl > 0]
    losses = [trade for trade in trades if trade.pnl <= 0]
    total_pnl = balance - starting_balance
    win_rate = (len(wins) / len(trades) * 100) if trades else 0.0
    avg_win = sum(trade.pnl for trade in wins) / len(wins) if wins else 0.0
    avg_loss = sum(trade.pnl for trade in losses) / len(losses) if losses else 0.0

    return "\n".join(
        [
            f"symbol={config['symbol']} interval={config['interval']} trend_interval={config['trend_interval']} candles={len(candles)}",
            f"trades={len(trades)} wins={len(wins)} losses={len(losses)} win_rate={win_rate:.1f}%",
            f"start_balance={starting_balance:.2f} end_balance={balance:.2f} total_pnl={total_pnl:.2f} USDT",
            f"avg_win={avg_win:.2f} avg_loss={avg_loss:.2f} max_drawdown={max_drawdown:.2f} USDT",
            "last_5_trades=" + format_last_trades(trades[-5:]),
        ]
    )


def check_exit(position: BacktestPosition, candle: Candle) -> tuple[float | None, str]:
    if position.side == "LONG":
        if candle.low <= position.stop_loss:
            return position.stop_loss, "stop_loss"
        if candle.high >= position.take_profit:
            return position.take_profit, "take_profit"
    else:
        if candle.high >= position.stop_loss:
            return position.stop_loss, "stop_loss"
        if candle.low <= position.take_profit:
            return position.take_profit, "take_profit"
    return None, ""


def calculate_pnl(position: BacktestPosition, exit_price: float) -> float:
    if position.side == "LONG":
        return (exit_price - position.entry_price) * position.quantity
    return (position.entry_price - exit_price) * position.quantity


def format_last_trades(trades: list[BacktestTrade]) -> str:
    if not trades:
        return "none"
    return "; ".join(
        f"{trade.side} {trade.reason} pnl={trade.pnl:.2f}" for trade in trades
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest the Binance futures lab strategy")
    parser.add_argument("--config", default="config.example.json")
    parser.add_argument("--limit", type=int, default=1000)
    args = parser.parse_args()

    config = load_config(Path(args.config))
    print(run_backtest(config, args.limit))


if __name__ == "__main__":
    main()
