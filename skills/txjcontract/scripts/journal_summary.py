from __future__ import annotations

import csv
from pathlib import Path


def main() -> None:
    root = Path.cwd()
    path = root / "trade_journal.csv"
    if not path.exists():
        print("trade_journal.csv not found in current directory")
        return

    rows = list(csv.DictReader(path.open("r", encoding="utf-8")))
    closed = []
    for row in rows:
        try:
            pnl = float(row.get("net_pnl_usdt") or 0)
        except ValueError:
            pnl = 0.0
        closed.append((row, pnl))

    total = len(closed)
    wins = sum(1 for _, pnl in closed if pnl > 0)
    losses = sum(1 for _, pnl in closed if pnl < 0)
    breakeven = total - wins - losses
    net = sum(pnl for _, pnl in closed)
    win_rate = (wins / total * 100) if total else 0.0

    print(f"closed_trades={total}")
    print(f"wins={wins}")
    print(f"losses={losses}")
    print(f"breakeven={breakeven}")
    print(f"win_rate={win_rate:.2f}%")
    print(f"net_pnl_usdt={net:.8f}")

    by_symbol: dict[str, list[float]] = {}
    for row, pnl in closed:
        by_symbol.setdefault(row.get("symbol", ""), []).append(pnl)
    for symbol, pnls in sorted(by_symbol.items()):
        sym_wins = sum(1 for pnl in pnls if pnl > 0)
        sym_rate = sym_wins / len(pnls) * 100 if pnls else 0.0
        print(f"{symbol}: trades={len(pnls)} win_rate={sym_rate:.2f}% net={sum(pnls):.8f}")


if __name__ == "__main__":
    main()
