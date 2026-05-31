from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from .client import BinanceFuturesPublicClient
from .executor import PaperExecutor
from .risk import RiskConfig, RiskManager
from .strategy import EmaRsiStrategy, StrategyConfig


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run_once(config: dict[str, Any], executor: PaperExecutor | None = None) -> str:
    if config["mode"] != "paper":
        raise RuntimeError("live trading is intentionally locked in this lab")

    client = BinanceFuturesPublicClient(config["base_url"])
    candles = client.klines(config["symbol"], config["interval"], int(config["lookback"]))
    trend_candles = client.klines(
        config["symbol"],
        config["trend_interval"],
        int(config["trend_lookback"]),
    )
    mark_price = client.mark_price(config["symbol"])

    strategy_config = StrategyConfig(**config["strategy"])
    signal = EmaRsiStrategy(strategy_config).evaluate(candles, trend_candles)

    risk_config = RiskConfig(
        balance_usdt=float(config["paper_balance_usdt"]),
        leverage=int(config["leverage"]),
        risk_per_trade_pct=float(config["risk_per_trade_pct"]),
        max_position_margin_pct=float(config["max_position_margin_pct"]),
        stop_loss_pct=float(config["stop_loss_pct"]),
        take_profit_pct=float(config["take_profit_pct"]),
    )
    risk = RiskManager(risk_config)
    paper = executor or PaperExecutor(float(config["paper_balance_usdt"]))

    status = paper.mark(mark_price)
    if signal.side in {"LONG", "SHORT"} and paper.position is None:
        plan = risk.plan(signal.side, signal.price)
        status = paper.maybe_open(plan)
        plan_text = (
            f"plan margin={plan.margin_usdt:.2f} notional={plan.notional_usdt:.2f} "
            f"max_loss={plan.max_loss_usdt:.2f}"
        )
    else:
        plan_text = "plan none"

    return (
        f"{config['symbol']} {config['interval']}/{config['trend_interval']} mark={mark_price:.2f} "
        f"signal={signal.side} reason=\"{signal.reason}\" {plan_text}; {status}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Binance futures paper trading lab")
    parser.add_argument("--config", default="config.example.json")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    executor = PaperExecutor(float(config["paper_balance_usdt"]))

    while True:
        print(run_once(config, executor), flush=True)
        if args.once:
            return
        time.sleep(int(config["poll_seconds"]))


if __name__ == "__main__":
    main()
