from .. import manifest as manifest_store
from ..providers import llm


def build(project: str, topic: str, tone: str, duration_sec: int) -> dict:
    shots = llm.generate_storyboard(topic, tone, duration_sec)
    return manifest_store.create(project, topic, tone, duration_sec, shots)
