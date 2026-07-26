import json

from .. import config

STORYBOARD_SYSTEM_PROMPT = """You are a scriptwriter and storyboard artist for short promotional / affiliate \
marketing videos featuring a recurring AI presenter (the "host").

Given a topic, tone, and target duration, produce a storyboard as a shot list. Output ONLY a JSON object, \
no other text, matching this schema:

{
  "shots": [
    {
      "type": "host",
      "duration_sec": 5,
      "text": "line the presenter speaks to camera"
    },
    {
      "type": "broll",
      "duration_sec": 4,
      "visual_prompt": "visual description for a text-to-video model, no camera/actor names"
    }
  ]
}

Rules:
- type is either "host" (the recurring presenter speaking to camera, lip-synced from `text`) or "broll" \
(a cutaway shot generated from `visual_prompt`, no presenter).
- Alternate host and broll shots; open and close on a host shot (hook, then call-to-action).
- Each shot is 3-8 seconds. The sum of duration_sec should be close to the target duration.
- host shots carry the pitch/CTA; broll shots visually support what the host just said.
- Mention the product/service/affiliate offer by name in at least one host line.
- Do not include markdown fences or commentary, only the JSON object.
"""


def generate_storyboard(topic: str, tone: str, duration_sec: int) -> list:
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is not set (see .env.example)")

    import anthropic

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=config.ANTHROPIC_MODEL,
        max_tokens=2000,
        system=STORYBOARD_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Topic: {topic}\nTone: {tone}\nTarget duration: {duration_sec} seconds",
            }
        ],
    )
    raw = message.content[0].text.strip()
    data = json.loads(raw)

    shots = []
    for i, shot in enumerate(data["shots"], start=1):
        shots.append(
            {
                "id": i,
                "type": shot["type"],
                "duration_sec": shot["duration_sec"],
                "text": shot.get("text"),
                "visual_prompt": shot.get("visual_prompt"),
                "status": "pending",
                "file": None,
            }
        )
    return shots
