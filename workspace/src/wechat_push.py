from __future__ import annotations

import argparse
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def read_env(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value.strip()
    if not ENV_PATH.exists():
        return None
    for line in ENV_PATH.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip()
    return None


def post_markdown(webhook_url: str, content: str) -> None:
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content[:3900],
        },
    }
    request = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8")
    data = json.loads(body)
    if data.get("errcode") != 0:
        raise RuntimeError(body)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send markdown content to WeCom robot webhook.")
    parser.add_argument("--file", required=True, help="Markdown file to send.")
    args = parser.parse_args()

    webhook_url = read_env("WECOM_WEBHOOK_URL") or read_env("WECHAT_WEBHOOK_URL")
    if not webhook_url:
        raise RuntimeError("missing WECOM_WEBHOOK_URL")

    path = Path(args.file)
    content = path.read_text(encoding="utf-8")
    post_markdown(webhook_url, content)
    print("wechat_push_ok")


if __name__ == "__main__":
    main()
