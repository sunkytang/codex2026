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


BASE_URLS = {
    "futures-mainnet": "https://fapi.binance.com",
    "spot-mainnet": "https://api.binance.com",
    "testnet": "https://demo-fapi.binance.com",
}


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


def signed_get(
    base_url: str,
    api_key: str,
    secret_key: str,
    path: str,
    params: dict[str, str] | None = None,
) -> tuple[int, str]:
    payload = dict(params or {})
    payload["timestamp"] = str(int(time.time() * 1000))
    payload["recvWindow"] = "5000"
    query = urllib.parse.urlencode(payload)
    signature = hmac.new(
        secret_key.encode("utf-8"),
        query.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    url = f"{base_url}{path}?{query}&signature={signature}"
    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "X-MBX-APIKEY": api_key,
            "User-Agent": "codex-binance-futures-lab/0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8")


def summarize_balance(text: str) -> dict[str, Any]:
    data = json.loads(text)
    usdt = next((row for row in data if row.get("asset") == "USDT"), None)
    if not usdt:
        return {"ok": True, "message": "connected; USDT balance row not found"}
    return {
        "ok": True,
        "asset": "USDT",
        "balance": usdt.get("balance"),
        "availableBalance": usdt.get("availableBalance"),
        "crossWalletBalance": usdt.get("crossWalletBalance"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Binance USD-M Futures account access")
    parser.add_argument(
        "--env",
        choices=["futures-mainnet", "spot-mainnet", "testnet"],
        default="futures-mainnet",
    )
    args = parser.parse_args()

    if args.env in {"futures-mainnet", "spot-mainnet"}:
        api_key = read_secret("BINANCE_API_KEY")
        secret_key = read_secret("BINANCE_SECRET_KEY")
    else:
        api_key = read_secret("BINANCE_TESTNET_API_KEY")
        secret_key = read_secret("BINANCE_TESTNET_SECRET_KEY")

    if not api_key or not secret_key:
        raise RuntimeError(f"missing {args.env} API key or secret")

    path = "/api/v3/account" if args.env == "spot-mainnet" else "/fapi/v2/balance"
    status, text = signed_get(BASE_URLS[args.env], api_key, secret_key, path)
    print(f"status={status}")
    if status == 200 and args.env != "spot-mainnet":
        print(json.dumps(summarize_balance(text), ensure_ascii=False, indent=2))
    elif status == 200:
        data = json.loads(text)
        non_zero = [
            {
                "asset": row["asset"],
                "free": row["free"],
                "locked": row["locked"],
            }
            for row in data.get("balances", [])
            if float(row["free"]) > 0 or float(row["locked"]) > 0
        ]
        print(
            json.dumps(
                {
                    "ok": True,
                    "canReadSpotAccount": True,
                    "accountType": data.get("accountType"),
                    "permissions": data.get("permissions", []),
                    "nonZeroBalances": non_zero[:20],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(text)


if __name__ == "__main__":
    main()
