import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

HEYGEN_API_KEY = os.environ.get("HEYGEN_API_KEY")
HEYGEN_BASE_URL = os.environ.get("HEYGEN_BASE_URL", "https://api.heygen.com")

KLING_API_KEY = os.environ.get("KLING_API_KEY")
KLING_BASE_URL = os.environ.get("KLING_BASE_URL", "https://api-singapore.klingai.com")

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"
ASSETS_DIR = BASE_DIR / "assets"
MUSIC_DIR = ASSETS_DIR / "music"
AVATAR_CONFIG_PATH = BASE_DIR / "avatar_config.json"
