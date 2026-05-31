from __future__ import annotations

from pathlib import Path

from . import full_report
from .pro_analysis import score_symbol
from .wechat_push import post_markdown, read_env


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "state" / "full_report_latest.md"


def short_push_content() -> str:
    account = full_report.account_state()
    symbols = ["BTCUSDT", "HYPEUSDT", "DOGEUSDT", "币安人生USDT", "TURBOUSDT", "TRUMPUSDT"]
    items = []
    for symbol in symbols:
        try:
            items.append(score_symbol(symbol))
        except Exception:
            continue

    positions = account.get("positions", {}).get("items", [])
    position_lines = []
    for position in positions:
        position_lines.append(
            f"> 持仓 {position['symbol']} {position['positionSide']} {position['positionAmt']} "
            f"入场 {position['entryPrice']} 标记 {position['markPrice']} "
            f"PnL {float(position['unRealizedProfit']):.4f}U"
        )
    if not position_lines:
        position_lines.append("> 当前空仓")

    ranked = sorted(items, key=lambda item: (item["score"], item["quote_volume"]), reverse=True)
    top = ranked[:3]
    opportunity_lines = []
    for item in top:
        f15 = item["frames"]["15m"]
        f1h = item["frames"]["1h"]
        opportunity_lines.append(
            f"> {item['symbol']} {item['price']}｜{item['score']}/10｜"
            f"15m {f15['trend']} RSI {f15['rsi14']}｜1h {f1h['trend']}"
        )

    conclusion = "暂无必须新开仓，优先管理现有持仓。"
    turbo_position = next((p for p in positions if p.get("symbol") == "TURBOUSDT"), None)
    if turbo_position:
        mark = float(turbo_position["markPrice"])
        if mark >= 0.001085:
            conclusion = "TURBO 接近第一目标，可考虑上移止损到成本附近。"
        else:
            conclusion = "TURBO 盈利中，未到第一目标，继续观察。"
    else:
        hype = next((item for item in items if item["symbol"] == "HYPEUSDT"), None)
        if hype and hype["score"] >= 9:
            conclusion = "HYPE 仍最强，但等回踩守住或突破站稳。"

    stamp = full_report.now_bjt().strftime("%H:%M")
    return "\n".join(
        [
            f"**合约短报 {stamp}**",
            "",
            *position_lines,
            "",
            "**机会前三**",
            *opportunity_lines,
            "",
            f"**结论**：{conclusion}",
        ]
    )


def main() -> None:
    full_report.main()
    webhook_url = read_env("WECOM_WEBHOOK_URL") or read_env("WECHAT_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("missing WECOM_WEBHOOK_URL")
    post_markdown(webhook_url, short_push_content())
    print("full_report_wechat_ok")


if __name__ == "__main__":
    main()
