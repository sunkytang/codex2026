from __future__ import annotations

from dataclasses import dataclass

from .risk import OrderPlan


@dataclass
class PaperPosition:
    side: str
    entry_price: float
    quantity: float
    stop_loss: float
    take_profit: float


class PaperExecutor:
    def __init__(self, balance_usdt: float) -> None:
        self.balance_usdt = balance_usdt
        self.position: PaperPosition | None = None

    def maybe_open(self, plan: OrderPlan) -> str:
        if self.position is not None:
            return "paper: position already open"
        self.position = PaperPosition(
            side=plan.side,
            entry_price=plan.entry_price,
            quantity=plan.quantity,
            stop_loss=plan.stop_loss,
            take_profit=plan.take_profit,
        )
        return (
            f"paper: opened {plan.side} qty={plan.quantity:.6f} "
            f"entry={plan.entry_price:.2f} sl={plan.stop_loss:.2f} tp={plan.take_profit:.2f}"
        )

    def mark(self, price: float) -> str:
        if self.position is None:
            return "paper: no open position"

        position = self.position
        hit_stop = (
            price <= position.stop_loss if position.side == "LONG" else price >= position.stop_loss
        )
        hit_take_profit = (
            price >= position.take_profit if position.side == "LONG" else price <= position.take_profit
        )

        if not hit_stop and not hit_take_profit:
            pnl = self._unrealized_pnl(price)
            return f"paper: open {position.side}; unrealized_pnl={pnl:.2f} USDT"

        exit_price = position.stop_loss if hit_stop else position.take_profit
        pnl = self._realized_pnl(exit_price)
        self.balance_usdt += pnl
        outcome = "stop_loss" if hit_stop else "take_profit"
        self.position = None
        return f"paper: closed by {outcome}; pnl={pnl:.2f} USDT; balance={self.balance_usdt:.2f}"

    def _unrealized_pnl(self, price: float) -> float:
        if self.position is None:
            return 0.0
        return self._pnl(price, self.position)

    def _realized_pnl(self, price: float) -> float:
        if self.position is None:
            return 0.0
        return self._pnl(price, self.position)

    @staticmethod
    def _pnl(price: float, position: PaperPosition) -> float:
        if position.side == "LONG":
            return (price - position.entry_price) * position.quantity
        return (position.entry_price - price) * position.quantity

