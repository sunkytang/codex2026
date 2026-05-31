from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .priority_scan import scan_once


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state"
LATEST_PATH = STATE_DIR / "priority_latest.md"
LOG_PATH = STATE_DIR / "priority_monitor.log"
PID_PATH = STATE_DIR / "priority_monitor.pid"


def now_bjt() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def is_allowed_time(value: datetime) -> bool:
    return 7 <= value.hour <= 23


def action_zh(action: str) -> str:
    return {
        "wait": "等待",
        "pullback_trigger_watch": "回踩触发观察",
        "breakout_trigger_watch": "突破触发观察",
        "support_reclaim_watch": "支撑修复观察",
        "near_breakout_watch": "接近突破观察",
    }.get(action, action)


def bias_zh(bias: str) -> str:
    return {
        "long": "偏多",
        "short": "偏空",
        "none": "中性",
    }.get(bias, bias)


def render(rows: list[dict]) -> str:
    stamp = now_bjt().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# 重点合约 5 分钟简报",
        "",
        f"北京时间：{stamp}",
        "",
        "| 币种 | 价格 | 总分 | T/P/R | 方向 | 状态 |",
        "|---|---:|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['symbol']} | {row['price']} | {row['score']}/10 | "
            f"{row['tpr']} | {bias_zh(row['bias'])} | {action_zh(row['action'])} |"
        )

    conclusion = "暂无确认下单点"
    if any(row["action"] in {"breakout_trigger_watch", "pullback_trigger_watch"} for row in rows):
        conclusion = "有币种接近触发位，需要人工确认后才可下单"
    lines.extend(["", f"结论：{conclusion}", ""])
    return "\n".join(lines)


def write_outputs(rows: list[dict]) -> None:
    STATE_DIR.mkdir(exist_ok=True)
    text = render(rows)
    LATEST_PATH.write_text(text, encoding="utf-8")
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"time_bjt": now_bjt().isoformat(), "rows": rows}, ensure_ascii=False))
        file.write("\n")
    print(text, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Stable local 5-minute priority futures monitor.")
    parser.add_argument("--interval", type=int, default=300, help="Normal scan interval in seconds.")
    parser.add_argument("--once", action="store_true", help="Run one scan and exit.")
    args = parser.parse_args()

    STATE_DIR.mkdir(exist_ok=True)
    PID_PATH.write_text(str(os.getpid()), encoding="utf-8")

    while True:
        current = now_bjt()
        if is_allowed_time(current):
            rows = scan_once()
            write_outputs(rows)
        else:
            message = f"{current:%Y-%m-%d %H:%M:%S} 北京时间非监控时段，暂停。"
            LATEST_PATH.write_text(message + "\n", encoding="utf-8")
            print(message, flush=True)

        if args.once:
            return
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
