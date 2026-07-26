#!/usr/bin/env python3
import argparse
import sys

from . import config, manifest as manifest_store
from .pipeline import assemble as assemble_pipeline
from .pipeline import render as render_pipeline
from .pipeline import storyboard as storyboard_pipeline


def cmd_init(args):
    manifest = storyboard_pipeline.build(args.project, args.topic, args.tone, args.duration)
    print(f"Created project '{args.project}' with {len(manifest['shots'])} shots.")
    _print_status(manifest)
    print("\nReview the storyboard above. Edit shots directly in "
          f"{manifest_store.manifest_path(args.project)} if needed, then run "
          f"`agent.py render {args.project}`.")


def cmd_avatar_setup(args):
    manifest_store.save_avatar_config(args.avatar_id, args.voice_id)
    print(f"Saved avatar_id={args.avatar_id} voice_id={args.voice_id} "
          f"to {config.AVATAR_CONFIG_PATH}. This avatar will be reused for every project.")


def cmd_render(args):
    only = set(args.shots) if args.shots else None
    rendered = render_pipeline.render_pending(args.project, only)
    if rendered:
        print(f"Rendered shots: {rendered}")
    else:
        print("Nothing to render (no pending/rejected shots).")
    _print_status(manifest_store.load(args.project))


def cmd_status(args):
    _print_status(manifest_store.load(args.project))


def cmd_approve(args):
    manifest = manifest_store.load(args.project)
    for shot_id in args.shots:
        manifest_store.get_shot(manifest, shot_id)["status"] = "approved"
    manifest_store.save(args.project, manifest)
    _print_status(manifest)


def cmd_reject(args):
    manifest = manifest_store.load(args.project)
    for shot_id in args.shots:
        manifest_store.get_shot(manifest, shot_id)["status"] = "rejected"
    manifest_store.save(args.project, manifest)
    print(f"Marked shots {args.shots} as rejected. Run `agent.py render {args.project}` "
          f"to regenerate only those.")


def cmd_assemble(args):
    final_path = assemble_pipeline.assemble(args.project)
    print(f"Final video: {final_path}")


def _print_status(manifest):
    print(f"\nProject: {manifest['project']}  ({manifest['duration_sec']}s target)")
    for shot in manifest["shots"]:
        label = shot.get("text") or shot.get("visual_prompt") or ""
        print(f"  [{shot['id']:02d}] {shot['type']:5s} {shot['duration_sec']:>2}s "
              f"{shot['status']:9s} {label[:60]}")


def main():
    parser = argparse.ArgumentParser(prog="agent.py", description="Agentic video creation pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Generate a storyboard for a new project")
    p_init.add_argument("project")
    p_init.add_argument("--topic", required=True)
    p_init.add_argument("--tone", default="energetic, casual")
    p_init.add_argument("--duration", type=int, default=60)
    p_init.set_defaults(func=cmd_init)

    p_avatar = sub.add_parser("avatar-setup", help="Register the recurring AI presenter (one-time)")
    p_avatar.add_argument("--avatar-id", required=True, help="HeyGen avatar_id from the dashboard")
    p_avatar.add_argument("--voice-id", required=True, help="HeyGen voice_id from the dashboard")
    p_avatar.set_defaults(func=cmd_avatar_setup)

    p_render = sub.add_parser("render", help="Render pending/rejected shots")
    p_render.add_argument("project")
    p_render.add_argument("--shots", type=int, nargs="*", help="Only render these shot ids")
    p_render.set_defaults(func=cmd_render)

    p_status = sub.add_parser("status", help="Show shot statuses for a project")
    p_status.add_argument("project")
    p_status.set_defaults(func=cmd_status)

    p_approve = sub.add_parser("approve", help="Mark shots as approved")
    p_approve.add_argument("project")
    p_approve.add_argument("shots", type=int, nargs="+")
    p_approve.set_defaults(func=cmd_approve)

    p_reject = sub.add_parser("reject", help="Mark shots as rejected so they re-render")
    p_reject.add_argument("project")
    p_reject.add_argument("shots", type=int, nargs="+")
    p_reject.set_defaults(func=cmd_reject)

    p_assemble = sub.add_parser("assemble", help="Cut approved/generated shots into a final video")
    p_assemble.add_argument("project")
    p_assemble.set_defaults(func=cmd_assemble)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
