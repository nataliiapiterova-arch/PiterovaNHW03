"""HeyGen talking-head avatar rendering.

Avatar creation itself (photo avatar upload + training) is done once, by hand,
in the HeyGen dashboard (Avatars > Create Photo/Instant Avatar) — that flow is
a multi-step review process better done visually than scripted. This module
only needs the resulting `avatar_id` and a `voice_id` (also picked in the
dashboard, or your own ElevenLabs voice if HeyGen supports importing one),
stored once via `agent.py avatar-setup` and reused for every video.

Verify the endpoint paths/response shape against HeyGen's current API docs
before relying on this in production — API contracts do shift over time.
"""

import time

import requests

from .. import config

POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 600


def generate_talking_head(avatar_id: str, voice_id: str, text: str, out_path) -> None:
    if not config.HEYGEN_API_KEY:
        raise RuntimeError("HEYGEN_API_KEY is not set (see .env.example)")

    headers = {
        "X-Api-Key": config.HEYGEN_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "video_inputs": [
            {
                "character": {"type": "avatar", "avatar_id": avatar_id, "avatar_style": "normal"},
                "voice": {"type": "text", "input_text": text, "voice_id": voice_id},
            }
        ],
        "dimension": {"width": 1280, "height": 720},
    }

    resp = requests.post(
        f"{config.HEYGEN_BASE_URL}/v2/video/generate", headers=headers, json=payload, timeout=30
    )
    resp.raise_for_status()
    video_id = resp.json()["data"]["video_id"]

    video_url = _poll_until_ready(video_id, headers)
    _download(video_url, out_path)


def _poll_until_ready(video_id: str, headers: dict) -> str:
    deadline = time.time() + POLL_TIMEOUT_SEC
    while time.time() < deadline:
        resp = requests.get(
            f"{config.HEYGEN_BASE_URL}/v1/video_status.get",
            headers=headers,
            params={"video_id": video_id},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("status")
        if status == "completed":
            return data["video_url"]
        if status == "failed":
            raise RuntimeError(f"HeyGen render failed: {data.get('error')}")
        time.sleep(POLL_INTERVAL_SEC)
    raise TimeoutError(f"HeyGen render {video_id} did not finish within {POLL_TIMEOUT_SEC}s")


def _download(url: str, out_path) -> None:
    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1 << 16):
            f.write(chunk)
