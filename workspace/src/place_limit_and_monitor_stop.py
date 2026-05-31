from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from .futures_trade import read_secret, signed_request


def log(path: Path, message: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Place a limit futures order and monitor stop")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=True)
    parser.add_argument("--stop-price", required=True)
    parser.add_argument("--leverage", type=int, default=2)
    parser.add_argument("--poll-seconds", type=int, default=5)
    parser.add_argument("--log", default="state/hype_stop_monitor.log")
    args = parser.parse_args()

    log_path = Path(args.log)
    api_key = read_secret("BINANCE_API_KEY")
    secret_key = read_secret("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        raise RuntimeError("missing BINANCE_API_KEY or BINANCE_SECRET_KEY")

    position_side = "SHORT" if args.side == "SELL" else "LONG"
    stop_side = "BUY" if args.side == "SELL" else "SELL"

    status, text = signed_request(
        "POST",
        "/fapi/v1/leverage",
        {"symbol": args.symbol, "leverage": args.leverage},
        api_key,
        secret_key,
    )
    log(log_path, f"set leverage status={status} response={text}")
    if status != 200:
        return

    status, text = signed_request(
        "POST",
        "/fapi/v1/order",
        {
            "symbol": args.symbol,
            "side": args.side,
            "positionSide": position_side,
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": args.quantity,
            "price": args.price,
            "newClientOrderId": f"agent-entry-{int(time.time())}",
        },
        api_key,
        secret_key,
    )
    log(log_path, f"entry status={status} response={text}")
    if status != 200:
        return

    order = json.loads(text)
    order_id = str(order["orderId"])
    stop_placed = False

    while True:
        status, text = signed_request(
            "GET",
            "/fapi/v1/order",
            {"symbol": args.symbol, "orderId": order_id},
            api_key,
            secret_key,
        )
        log(log_path, f"query order status={status} response={text}")
        if status != 200:
            time.sleep(args.poll_seconds)
            continue

        current = json.loads(text)
        order_status = current.get("status")
        if order_status in {"CANCELED", "EXPIRED", "REJECTED"}:
            log(log_path, f"entry ended without fill: {order_status}")
            return
        if order_status == "FILLED" and not stop_placed:
            stop_status, stop_text = signed_request(
                "POST",
                "/fapi/v1/algoOrder",
                {
                    "algoType": "CONDITIONAL",
                    "symbol": args.symbol,
                    "side": stop_side,
                    "positionSide": position_side,
                    "type": "STOP_MARKET",
                    "triggerPrice": args.stop_price,
                    "closePosition": "true",
                    "workingType": "MARK_PRICE",
                    "clientAlgoId": f"agent-stop-{int(time.time())}",
                },
                api_key,
                secret_key,
            )
            log(log_path, f"stop status={stop_status} response={stop_text}")
            stop_placed = stop_status == 200
            return

        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    main()
