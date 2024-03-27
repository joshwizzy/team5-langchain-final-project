import os
from typing import Any

import requests


def make_request(method: str, path: str, payload: dict[str, Any] | None = None):
    api_url = os.environ["API_URL"]
    api_key = os.environ.get("API_KEY", None)
    headers = {"X-API-Key": api_key} if api_key else {}

    timeout = (1, 30)
    payload = payload if payload else {}

    return requests.request(
        method,
        f"{api_url}{path}",
        headers=headers,
        timeout=timeout,
        json=payload,
    )
