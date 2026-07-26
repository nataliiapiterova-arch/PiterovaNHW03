import subprocess
from pathlib import Path

from .. import config, manifest as manifest_store

RESOLUTION = "1280:720"
FPS = "30"


def assemble(project: str) -> Path:
    manifest = manifest_store.load(project)
    ready_shots = [
        s for s in sorted(manifest["shots"], key=lambda s: s["id"])
        if s["status"] in ("generated", "approved")
    ]
    if not ready_shots:
        raise RuntimeError("No rendered shots to assemble. Run `agent.py render` first.")

    project_dir = manifest_store.project_dir(project)
    out_dir = manifest_store.output_dir(project)
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = out_dir / "_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    normalized = []
    for shot in ready_shots:
        src = project_dir / shot["file"]
        dst = tmp_dir / f"norm_{shot['id']:02d}.mp4"
        _run(
            [
                "ffmpeg", "-y", "-i", str(src),
                "-vf", f"scale={RESOLUTION}:force_original_aspect_ratio=decrease,"
                       f"pad={RESOLUTION}:(ow-iw)/2:(oh-ih)/2,fps={FPS}",
                "-c:v", "libx264", "-c:a", "aac", "-ar", "44100",
                str(dst),
            ]
        )
        normalized.append(dst)

    concat_list = tmp_dir / "concat.txt"
    concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in normalized))

    assembled = tmp_dir / "assembled.mp4"
    _run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c", "copy", str(assembled),
        ]
    )

    srt_path = tmp_dir / "captions.srt"
    _write_srt(ready_shots, srt_path)
    captioned = tmp_dir / "captioned.mp4"
    escaped_srt = str(srt_path.resolve()).replace("\\", "/").replace(":", "\\:")
    _run(
        [
            "ffmpeg", "-y", "-i", str(assembled),
            "-vf", f"subtitles={escaped_srt}",
            "-c:a", "copy", str(captioned),
        ]
    )

    final_path = out_dir / "final.mp4"
    music_file = manifest.get("music", {}).get("file")
    music_path = config.MUSIC_DIR / music_file if music_file else None
    if music_path and music_path.exists():
        _run(
            [
                "ffmpeg", "-y", "-i", str(captioned), "-i", str(music_path),
                "-filter_complex", "[1:a]volume=0.15[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2",
                "-c:v", "copy", str(final_path),
            ]
        )
    else:
        _run(["ffmpeg", "-y", "-i", str(captioned), "-c", "copy", str(final_path)])

    return final_path


def _write_srt(shots: list, srt_path) -> None:
    lines = []
    t = 0.0
    idx = 1
    for shot in shots:
        duration = shot["duration_sec"]
        if shot["type"] == "host" and shot.get("text"):
            start = _fmt_ts(t)
            end = _fmt_ts(t + duration)
            lines.append(f"{idx}\n{start} --> {end}\n{shot['text']}\n")
            idx += 1
        t += duration
    srt_path.write_text("\n".join(lines))


def _fmt_ts(seconds: float) -> str:
    ms = int(round((seconds - int(seconds)) * 1000))
    s = int(seconds) % 60
    m = (int(seconds) // 60) % 60
    h = int(seconds) // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _run(cmd: list) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr}")
