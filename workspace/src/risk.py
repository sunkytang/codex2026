from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskConfig:
    balance_usdt: float
    leverage: int
    risk_per_trade_pct: float
    max_position_margin_pct: float
    stop_loss_pct: float
    take_profit_pct: float


@dataclass(frozen=True)
class OrderPlan:
    side: str
    entry_price: float
    quantity: float
    notional_usdt: float
    margin_usdt: float
    stop_loss: float
    take_profit: float
    max_loss_usdt: float


class RiskManager:
    def __init__(self, config: RiskConfig) -> None:
        self.config = config

    def plan(self, side: str, entry_price: float) -> OrderPlan:
        if side not in {"LONG", "SHORT"}:
            raise ValueError("side must be LONG or SHORT")
        if entry_price <= 0:
            raise ValueError("entry price must be positive")

        risk_budget = self.config.balance_usdt * self.config.risk_per_trade_pct / 100
        stop_distance = entry_price * self.config.stop_loss_pct / 100
        risk_quantity = risk_budget / stop_distance

        max_margin = self.config.balance_usdt * self.config.max_position_margin_pct / 100
        max_notional = max_margin * self.config.leverage
        max_quantity = max_notional / entry_price
        quantity = min(risk_quantity, max_quantity)

        notional = quantity * entry_price
        margin = notional / self.config.leverage

        if side == "LONG":
            stop_loss = entry_price * (1 - self.config.stop_loss_pct / 100)
            take_profit = entry_price * (1 + self.config.take_profit_pct / 100)
        else:
            stop_loss = entry_price * (1 + self.config.stop_loss_pct / 100)
            take_profit = entry_price * (1 - self.config.take_profit_pct / 100)

        max_loss = abs(entry_price - stop_loss) * quantity
        return OrderPlan(side, entry_price, quantity, notional, margin, stop_loss, take_profit, max_loss)

