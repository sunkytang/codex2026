from __future__ import annotations

import argparse
import hashlib
import hmac
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


TESTNET_URL = "https://demo-fapi.binance.com"
MAINNET_URL = "https://fapi.binance.com"


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
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(f"{name}="):
                return line.split("=", 1)[1].strip()
    return None


def signed_request(
    base_url: str,
    api_key: str,
    secret_key: str,
    path: str,
    params: dict[str, str],
) -> tuple[int, str]:
    payload = params.copy()
    payload["timestamp"] = str(int(time.time() * 1000))
    payload["recvWindow"] = "5000"
    query = urllib.parse.urlencode(payload)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    body = f"{query}&signature={signature}".encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        method="POST",
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a Binance USD-M Futures test order")
    parser.add_argument("--env", choices=["testnet", "mainnet"], default="testnet")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--side", choices=["BUY", "SELL"], default="BUY")
    parser.add_argument("--type", default="MARKET")
    parser.add_argument("--quantity", default="0.001")
    args = parser.parse_args()

    if args.env == "testnet":
        api_key = read_secret("BINANCE_TESTNET_API_KEY")
        secret_key = read_secret("BINANCE_TESTNET_SECRET_KEY")
        base_url = TESTNET_URL
    else:
        raise RuntimeError("mainnet test order is locked; use testnet for flow checks")

    if not api_key or not secret_key:
        raise RuntimeError(
            "missing BINANCE_TESTNET_API_KEY or BINANCE_TESTNET_SECRET_KEY"
        )

    status, text = signed_request(
        base_url=base_url,
        api_key=api_key,
        secret_key=secret_key,
        path="/fapi/v1/order/test",
        params={
            "symbol": args.symbol,
            "side": args.side,
            "type": args.type,
            "quantity": args.quantity,
            "newClientOrderId": f"agent-test-{int(time.time())}",
        },
    )
    print(f"status={status}")
    print(text if text else "test order accepted")


if __name__ == "__main__":
    main()
