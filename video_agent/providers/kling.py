"""Kling B-roll (text-to-video) rendering.

Kling's official API is only broadly available through a handful of access
routes (direct Kuaishou API access, or aggregators like fal.ai / PiAPI /
segmind), and the exact endpoint paths and auth scheme differ between them.
Set KLING_BASE_URL and KLING_API_KEY in .env to match whichever route you
use, and adjust the request/response field names below to match that
provider's current docs before relying on this in production.
"""

import time

import requests

from .. import config

POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 600


def generate_clip(visual_prompt: str, duration_sec: int, out_path) -> None:
    if not config.KLING_API_KEY:
        raise RuntimeError("KLING_API_KEY is not set (see .env.example)")

    headers = {
        "Authorization": f"Bearer {config.KLING_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "prompt": visual_prompt,
        "duration": duration_sec,
        "mode": "std",  # budget/standard tier, not "pro"
    }

    resp = requests.post(
        f"{config.KLING_BASE_URL}/v1/videos/text2video", headers=headers, json=payload, timeout=30
    )
    resp.raise_for_status()
    task_id = resp.json()["data"]["task_id"]

    video_url = _poll_until_ready(task_id, headers)
    _download(video_url, out_path)


def _poll_until_ready(task_id: str, headers: dict) -> str:
    deadline = time.time() + POLL_TIMEOUT_SEC
    while time.time() < deadline:
        resp = requests.get(
            f"{config.KLING_BASE_URL}/v1/videos/text2video/{task_id}", headers=headers, timeout=30
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("task_status")
        if status == "succeed":
            return data["task_result"]["videos"][0]["url"]
        if status == "failed":
            raise RuntimeError(f"Kling render failed: {data.get('task_status_msg')}")
        time.sleep(POLL_INTERVAL_SEC)
    raise TimeoutError(f"Kling render {task_id} did not finish within {POLL_TIMEOUT_SEC}s")


def _download(url: str, out_path) -> None:
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1 << 16):
            f.write(chunk)
