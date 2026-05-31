from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "trade_journal.csv"
MD_PATH = ROOT / "trade_journal.md"

FIELDS = [
    "id",
    "entry_time_bjt",
    "exit_time_bjt",
    "symbol",
    "side",
    "quantity",
    "entry_price",
    "exit_price",
    "stop_price",
    "result",
    "gross_pnl_usdt",
    "costs_usdt",
    "net_pnl_usdt",
    "account_impact",
    "trade_score",
    "core_conclusion",
    "success_failure_reason",
    "next_avoidance",
]


def next_id() -> str:
    if not CSV_PATH.exists():
        return "T001"
    with CSV_PATH.open("r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        return "T001"
    last = rows[-1]["id"].lstrip("T")
    return f"T{int(last) + 1:03d}"


def append_csv(row: dict[str, str]) -> None:
    exists = CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in FIELDS})


def append_markdown(row: dict[str, str]) -> None:
    operation_time = f"开仓 {row['entry_time_bjt']}；平仓 {row['exit_time_bjt']}"
    close_or_stop = row["exit_price"]
    if row.get("stop_price"):
        close_or_stop = f"{row['exit_price']} / 止损 {row['stop_price']}"
    line = (
        f"| {row['id']} | {operation_time} | {row['symbol']} | {row['side']} | "
        f"{row['quantity']} | {row['entry_price']} | {close_or_stop} | {row['result']} | "
        f"{row['net_pnl_usdt']} | {row['account_impact']} | {row['trade_score']} | "
        f"{row.get('core_conclusion', '')} | {row['success_failure_reason']} | "
        f"{row['next_avoidance']} |"
    )
    review = (
        f"\n### {row['id']} {row['symbol']} {row['side']}\n\n"
        f"- 结果：{row['result']}，净PnL {row['net_pnl_usdt']} USDT。\n"
        f"- 核心结论：{row.get('core_conclusion', '')}\n"
        f"- 成功/失败原因：{row['success_failure_reason']}\n"
        f"- 下次规避：{row['next_avoidance']}\n"
    )

    if not MD_PATH.exists():
        MD_PATH.write_text("# 合约交易复盘表\n\n## 总表\n\n", encoding="utf-8")
    text = MD_PATH.read_text(encoding="utf-8")
    if "## 单笔复盘" in text:
        text = text.replace("## 单笔复盘", f"{line}\n\n## 单笔复盘", 1)
        text = f"{text.rstrip()}\n{review}"
    else:
        text = f"{text.rstrip()}\n{line}\n\n## 单笔复盘\n{review}"
    MD_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Append a closed futures trade review.")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=["LONG", "SHORT"])
    parser.add_argument("--entry-time-bjt", required=True)
    parser.add_argument("--exit-time-bjt", required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--entry-price", required=True)
    parser.add_argument("--exit-price", required=True)
    parser.add_argument("--stop-price", default="")
    parser.add_argument("--result", required=True)
    parser.add_argument("--gross-pnl-usdt", required=True)
    parser.add_argument("--costs-usdt", required=True)
    parser.add_argument("--net-pnl-usdt", required=True)
    parser.add_argument("--account-impact", default="")
    parser.add_argument("--trade-score", default="")
    parser.add_argument("--core-conclusion", default="")
    parser.add_argument("--success-failure-reason", required=True)
    parser.add_argument("--next-avoidance", required=True)
    args = parser.parse_args()

    row = vars(args)
    row["id"] = next_id()
    append_csv(row)
    append_markdown(row)
    print(f"saved {row['id']} to {CSV_PATH} and {MD_PATH}")


if __name__ == "__main__":
    main()
