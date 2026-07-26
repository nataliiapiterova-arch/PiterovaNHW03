# video_agent

An agent-driven pipeline that produces short promo/affiliate videos with a
recurring AI presenter: Claude writes the storyboard, HeyGen renders the
presenter's talking-head shots, Kling renders B-roll cutaways, and ffmpeg
assembles the final cut with captions and background music.

Stack: **Claude (storyboard) + HeyGen (consistent AI presenter) + Kling
(B-roll) + ffmpeg (assembly)**. See the parent README/conversation for why
this combination was chosen over Runway/Synthesia/Arcads.

## Setup

1. `pip install -r requirements.txt`
2. Install `ffmpeg` and make sure it's on your `PATH` (`ffmpeg -version`).
3. Copy `.env.example` to `.env` in the repo root and fill in your API keys.
4. Create your AI presenter once, by hand, in the HeyGen dashboard
   (Avatars > Create Photo/Instant Avatar), and note the `avatar_id` and a
   `voice_id`. This is a one-time step — the same presenter is reused for
   every video after that.

## Workflow

```bash
# One-time: register your recurring AI presenter
python -m video_agent.agent avatar-setup --avatar-id <id> --voice-id <id>

# 1. Generate a storyboard (free — just an LLM call)
python -m video_agent.agent init my_promo \
  --topic "Promote [product] affiliate link, highlight the 20% discount code" \
  --tone "upbeat, confident" --duration 45

# Review the printed shot list. Edit video_agent/projects/my_promo/manifest.json
# directly if you want to tweak lines/prompts before spending anything on rendering.

# 2. Render all shots (this is the step that costs money)
python -m video_agent.agent render my_promo

# 3. Review clips in video_agent/projects/my_promo/clips/, then:
python -m video_agent.agent reject my_promo 3 5      # regenerate only these shots
python -m video_agent.agent render my_promo           # re-renders just shot 3 and 5
python -m video_agent.agent approve my_promo 1 2 3 4 5 6

# 4. Cut the final video (free — local ffmpeg)
python -m video_agent.agent assemble my_promo
# -> video_agent/projects/my_promo/output/final.mp4
```

`status` shows the state of every shot at any point:

```bash
python -m video_agent.agent status my_promo
```

## Background music

Drop royalty-free tracks into `video_agent/assets/music/`, then set
`"music": {"file": "your_track.mp3"}` in the project's `manifest.json` before
running `assemble`. Manual curation keeps this free and license-safe; swap
in a royalty-free API later if you want it automated.

## Cost (budget tier, ~45s video, roughly half host / half B-roll)

| Step | Rate | Approx. cost |
|---|---|---|
| Storyboard (Claude) | pennies/call | ~$0.05 |
| Presenter setup | one-time | ~$1 (once, ever) |
| Host shots (HeyGen) | ~$0.05/sec | ~$1.10 (22s) |
| B-roll shots (Kling) | ~$0.08–0.12/sec | ~$1.80–2.75 (23s) |
| Assembly (ffmpeg) | local | free |
| **Total per video** | | **~$3–4**, plus ~$1 once for the presenter |

Regenerating a rejected shot only re-renders that one clip, not the whole
video — reject liberally, it's cheap.

## What's stubbed vs. real

- Storyboard generation (Claude) is fully wired — works as soon as
  `ANTHROPIC_API_KEY` is set.
- HeyGen and Kling calls are written against each provider's typical
  API shape (submit job → poll status → download), but you should verify
  the exact endpoint paths/fields against your provider's current docs
  before a real run — these APIs do change, and Kling in particular varies
  by which access route (official vs. aggregator) you use.
- ffmpeg assembly (normalize, concat, burn captions, mix music) is real,
  local, and runs against whatever clips exist in a project's `clips/`
  folder — you can test it today with any short mp4s dropped in by hand.
