from __future__ import annotations

import csv
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REVIEWS_PATH = SKILL_DIR / "references" / "reviews.md"


def short(value: str, limit: int = 260) -> str:
    value = (value or "").replace("\n", " ").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def main() -> None:
    journal = Path.cwd() / "trade_journal.csv"
    if not journal.exists():
        raise SystemExit("trade_journal.csv not found in current directory")

    rows = list(csv.DictReader(journal.open("r", encoding="utf-8")))
    lines: list[str] = [
        "# Closed-Trade Lessons",
        "",
        "Generated from `trade_journal.csv`. Use the CSV/XLSX files for exact accounting.",
        "",
    ]

    hard_rules: list[str] = []
    for row in rows:
        trade_id = row.get("id", "")
        symbol = row.get("symbol", "")
        side = row.get("side", "")
        lines.extend(
            [
                f"## {trade_id} {symbol} {side}",
                "",
                f"- Entry: `{row.get('entry_price', '')}` at {row.get('entry_time_bjt', '')}",
                f"- Exit: `{row.get('exit_price', '')}` at {row.get('exit_time_bjt', '')}",
                f"- Stop: `{row.get('stop_price', '')}`",
                f"- Net PnL: `{row.get('net_pnl_usdt', '')} USDT`",
                f"- Core conclusion: {short(row.get('core_conclusion', ''))}",
                f"- Reason: {short(row.get('success_failure_reason', ''))}",
                f"- Next rule: {short(row.get('next_avoidance', ''))}",
                "",
            ]
        )
        rule = short(row.get("next_avoidance", ""), 180)
        if rule:
            hard_rules.append(rule)

    lines.extend(["## Current Hard Rules From These Trades", ""])
    if hard_rules:
        seen: set[str] = set()
        for rule in hard_rules:
            if rule in seen:
                continue
            seen.add(rule)
            lines.append(f"- {rule}")
    else:
        lines.append("- No closed-trade rules recorded yet.")
    lines.append("")

    REVIEWS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(REVIEWS_PATH)


if __name__ == "__main__":
    main()
