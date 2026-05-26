"""
Configuration management for Spotify Lyrics overlay.
Stores and loads user settings from a JSON file.
"""

import json
import os
import sys
from pathlib import Path

def _module_dir() -> Path:
    return Path(__file__).resolve().parent


def _is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def _dev_config_file() -> Path:
    return _module_dir() / "settings.json"


def _frozen_config_dir() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "LyPy"
    return Path.home() / "AppData" / "Roaming" / "LyPy"


def get_config_file_path() -> Path:
    if _is_frozen():
        return _frozen_config_dir() / "settings.json"
    return _dev_config_file()


def ensure_config_dir_writable() -> Path:
    config_path = get_config_file_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    test_file = config_path.parent / ".write_test"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("ok")
    test_file.unlink(missing_ok=True)
    return config_path

DEFAULT_CONFIG = {
    # ── Window settings ──
    "window_width": 500,
    "window_height": 700,
    "window_opacity": 1.0,
    "window_background_alpha": 255,
    "always_on_top": True,
    "frameless": True,

    # ── Appearance (Spotify-matched) ──
    "font_size": 28,
    "font_family": "Segoe UI, Circular, Helvetica, Arial, sans-serif",
    "bg_saturation": 80,       # 0-100 slider for background color saturation
    "line_spacing": 3,         # 0-10 gap between lyric lines
    "text_alignment": "left",
    "lyrics_color_mode": "spotify_sync",
    "manual_lyrics_color": "#ffffff",
    "show_app_title": True,

    # ── Behaviour ──
    "polling_interval_ms": 50,
    "scroll_animation_ms": 400,

}


def load_config() -> dict:
    """Load config from disk, falling back to defaults for missing keys."""
    config = DEFAULT_CONFIG.copy()
    config_file = get_config_file_path()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                saved = json.load(f)
            if isinstance(saved, dict):
                config.update(saved)
        except (json.JSONDecodeError, OSError):
            pass
    return config


def save_config(config: dict) -> None:
    """Persist current config to disk."""
    config_file = get_config_file_path()
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
