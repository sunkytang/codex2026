from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL = "https://fapi.binance.com"


def read_secret(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value.strip()

    candidates = [
        Path.cwd() / ".env",
        Path.home() / ".openclaw" / "secrets.env",
        Path.home() / ".env",
    ]
    for path in candidates:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    return None


def signed_request(
    method: str,
    path: str,
    params: dict[str, Any],
    api_key: str,
    secret_key: str,
) -> tuple[int, str]:
    payload = {key: str(value) for key, value in params.items() if value is not None}
    payload["timestamp"] = str(int(time.time() * 1000))
    payload["recvWindow"] = "5000"
    query = urllib.parse.urlencode(payload)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    body = f"{query}&signature={signature}".encode("utf-8")
    url = f"{BASE_URL}{path}"
    if method == "GET":
        url = f"{url}?{body.decode('utf-8')}"
        data = None
    else:
        data = body

    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "X-MBX-APIKEY": api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "codex-binance-futures-lab/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def public_get(path: str) -> Any:
    with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Place a small Binance USD-M futures trade")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--quantity", required=True)
    parser.add_argument("--price", required=True)
    parser.add_argument("--stop-price", required=True)
    parser.add_argument("--leverage", type=int, default=2)
    args = parser.parse_args()

    api_key = read_secret("BINANCE_API_KEY")
    secret_key = read_secret("BINANCE_SECRET_KEY")
    if not api_key or not secret_key:
        raise RuntimeError("missing BINANCE_API_KEY or BINANCE_SECRET_KEY")

    ticker = public_get(f"/fapi/v1/ticker/price?symbol={args.symbol}")
    print(json.dumps({"symbol": args.symbol, "lastPrice": ticker["price"]}, indent=2))

    leverage_status, leverage_text = signed_request(
        "POST",
        "/fapi/v1/leverage",
        {"symbol": args.symbol, "leverage": args.leverage},
        api_key,
        secret_key,
    )
    print(f"set_leverage_status={leverage_status}")
    print(leverage_text)
    if leverage_status != 200:
        raise RuntimeError("failed to set leverage")

    entry_status, entry_text = signed_request(
        "POST",
        "/fapi/v1/order",
        {
            "symbol": args.symbol,
            "side": args.side,
            "positionSide": "SHORT" if args.side == "SELL" else "LONG",
            "type": "LIMIT",
            "timeInForce": "GTC",
            "quantity": args.quantity,
            "price": args.price,
            "newClientOrderId": f"agent-entry-{int(time.time())}",
        },
        api_key,
        secret_key,
    )
    print(f"entry_order_status={entry_status}")
    print(entry_text)
    if entry_status != 200:
        raise RuntimeError("failed to place entry order")

    stop_side = "BUY" if args.side == "SELL" else "SELL"
    stop_status, stop_text = signed_request(
        "POST",
        "/fapi/v1/algoOrder",
        {
            "algoType": "CONDITIONAL",
            "symbol": args.symbol,
            "side": stop_side,
            "positionSide": "SHORT" if args.side == "SELL" else "LONG",
            "type": "STOP_MARKET",
            "triggerPrice": args.stop_price,
            "closePosition": "true",
            "workingType": "MARK_PRICE",
            "newClientOrderId": f"agent-stop-{int(time.time())}",
        },
        api_key,
        secret_key,
    )
    print(f"stop_order_status={stop_status}")
    print(stop_text)
    if stop_status != 200:
        raise RuntimeError("entry order placed, but failed to place stop order")


if __name__ == "__main__":
    main()
