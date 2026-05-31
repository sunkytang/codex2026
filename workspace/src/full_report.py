from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .futures_trade import read_secret, signed_request
from .pro_analysis import score_symbol


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state"
LATEST_PATH = STATE_DIR / "full_report_latest.md"
LOG_PATH = STATE_DIR / "full_report.log"

MAIN_SYMBOLS = ["BTCUSDT", "HYPEUSDT", "DOGEUSDT", "币安人生USDT"]
MEME_CANDIDATES = ["TURBOUSDT", "TRUMPUSDT", "1000PEPEUSDT", "PENGUUSDT", "WIFUSDT", "1000SHIBUSDT"]


def now_bjt() -> datetime:
    return datetime.now(timezone(timedelta(hours=8)))


def allowed_time() -> bool:
    current = now_bjt()
    return 7 <= current.hour <= 23


def account_state() -> dict:
    api_key = read_secret("BINANCE_API_KEY")
    secret_key = read_secret("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        return {"error": "missing api key"}

    result = {}
    for label, path, params in [
        ("open_orders", "/fapi/v1/openOrders", {}),
        ("open_algo_orders", "/fapi/v1/openAlgoOrders", {}),
        ("positions", "/fapi/v2/positionRisk", {}),
    ]:
        status, text = signed_request("GET", path, params, api_key, secret_key)
        data = json.loads(text)
        if label == "positions":
            data = [row for row in data if abs(float(row.get("positionAmt", "0"))) > 0]
        result[label] = {"status": status, "count": len(data), "items": data[:5]}
    return result


def pick_memes() -> list[dict]:
    scored = []
    for symbol in MEME_CANDIDATES:
        try:
            item = score_symbol(symbol)
            scored.append(item)
        except Exception:
            continue
    scored.sort(key=lambda row: (row["score"], row["quote_volume"]), reverse=True)

    selected = []
    seen = set()
    for symbol in ["TURBOUSDT"]:
        for item in scored:
            if item["symbol"] == symbol and symbol not in seen:
                selected.append(item)
                seen.add(symbol)
    for item in scored:
        if item["symbol"] not in seen:
            selected.append(item)
            seen.add(item["symbol"])
        if len(selected) >= 2:
            break
    return selected


def short_frame(item: dict, frame: str) -> str:
    data = item["frames"][frame]
    return f"{data['trend']} / RSI {data['rsi14']}"


def render(items: list[dict], account: dict) -> str:
    stamp = now_bjt().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 合约完整报告",
        "",
        f"北京时间：{stamp}",
        "",
        f"账户：持仓 {account.get('positions', {}).get('count', '?')}，普通挂单 {account.get('open_orders', {}).get('count', '?')}，条件单 {account.get('open_algo_orders', {}).get('count', '?')}",
        "",
        "| 币种 | 价格 | 24h | 评分 | 15m | 1h | 4h | 判断 |",
        "|---|---:|---:|---:|---|---|---|---|",
    ]

    for item in items:
        judgement = "等待"
        if item["score"] >= 9 and item["side"] == "long":
            judgement = "偏强，等确认"
        elif item["side"] == "short":
            judgement = "偏弱，等反抽失败"
        elif item["score"] <= 4:
            judgement = "无优势"
        lines.append(
            f"| {item['symbol']} | {item['price']} | {item['change24h_pct']:.2f}% | "
            f"{item['score']}/10 | {short_frame(item, '15m')} | {short_frame(item, '1h')} | "
            f"{short_frame(item, '4h')} | {judgement} |"
        )

    hype = next((item for item in items if item["symbol"] == "HYPEUSDT"), None)
    conclusion = "当前没有必须操作的单。"
    if hype and hype["score"] >= 9:
        conclusion = "HYPE 仍是主线，但必须等回踩守住或突破站稳，不做情绪化补单。"
    lines.extend(["", f"结论：{conclusion}", ""])
    return "\n".join(lines)


def main() -> None:
    STATE_DIR.mkdir(exist_ok=True)
    if not allowed_time():
        message = f"{now_bjt():%Y-%m-%d %H:%M:%S} 非监控时段，暂停。"
        LATEST_PATH.write_text(message + "\n", encoding="utf-8")
        print(message)
        return

    main_items = [score_symbol(symbol) for symbol in MAIN_SYMBOLS]
    meme_items = pick_memes()
    items = main_items + meme_items
    account = account_state()
    text = render(items, account)
    LATEST_PATH.write_text(text, encoding="utf-8")
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps({"time_bjt": now_bjt().isoformat(), "items": items, "account": account}, ensure_ascii=False))
        file.write("\n")
    print(text)


if __name__ == "__main__":
    main()

