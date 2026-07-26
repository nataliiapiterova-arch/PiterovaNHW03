import json
from pathlib import Path

from . import config

MANIFEST_VERSION = 1


def project_dir(name: str) -> Path:
    return config.PROJECTS_DIR / name


def manifest_path(name: str) -> Path:
    return project_dir(name) / "manifest.json"


def clips_dir(name: str) -> Path:
    return project_dir(name) / "clips"


def output_dir(name: str) -> Path:
    return project_dir(name) / "output"


def load(name: str) -> dict:
    path = manifest_path(name)
    if not path.exists():
        raise FileNotFoundError(f"No project '{name}' found at {path}")
    return json.loads(path.read_text())


def save(name: str, manifest: dict) -> None:
    path = manifest_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2))


def create(name: str, topic: str, tone: str, duration_sec: int, shots: list) -> dict:
    manifest = {
        "version": MANIFEST_VERSION,
        "project": name,
        "topic": topic,
        "tone": tone,
        "duration_sec": duration_sec,
        "shots": shots,
        "music": {"status": "pending", "file": None},
    }
    project_dir(name).mkdir(parents=True, exist_ok=True)
    clips_dir(name).mkdir(parents=True, exist_ok=True)
    output_dir(name).mkdir(parents=True, exist_ok=True)
    save(name, manifest)
    return manifest


def get_shot(manifest: dict, shot_id: int) -> dict:
    for shot in manifest["shots"]:
        if shot["id"] == shot_id:
            return shot
    raise KeyError(f"No shot with id {shot_id}")


def load_avatar_config() -> dict:
    if not config.AVATAR_CONFIG_PATH.exists():
        return {}
    return json.loads(config.AVATAR_CONFIG_PATH.read_text())


def save_avatar_config(avatar_id: str, voice_id: str) -> None:
    config.AVATAR_CONFIG_PATH.write_text(
        json.dumps({"avatar_id": avatar_id, "voice_id": voice_id}, indent=2)
    )
