from .. import manifest as manifest_store
from ..providers import heygen, kling


def render_pending(project: str, only_shot_ids=None) -> list:
    manifest = manifest_store.load(project)
    avatar_cfg = manifest_store.load_avatar_config()
    clips_dir = manifest_store.clips_dir(project)
    clips_dir.mkdir(parents=True, exist_ok=True)

    rendered = []
    for shot in manifest["shots"]:
        if only_shot_ids is not None and shot["id"] not in only_shot_ids:
            continue
        if shot["status"] not in ("pending", "rejected"):
            continue

        out_path = clips_dir / f"shot_{shot['id']:02d}.mp4"

        if shot["type"] == "host":
            if not avatar_cfg.get("avatar_id") or not avatar_cfg.get("voice_id"):
                raise RuntimeError(
                    "No avatar configured. Run `agent.py avatar-setup` first."
                )
            heygen.generate_talking_head(
                avatar_cfg["avatar_id"], avatar_cfg["voice_id"], shot["text"], out_path
            )
        elif shot["type"] == "broll":
            kling.generate_clip(shot["visual_prompt"], shot["duration_sec"], out_path)
        else:
            raise ValueError(f"Unknown shot type: {shot['type']}")

        shot["status"] = "generated"
        shot["file"] = str(out_path.relative_to(manifest_store.project_dir(project)))
        rendered.append(shot["id"])
        manifest_store.save(project, manifest)

    return rendered
