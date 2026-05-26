"""
Spotify Lyrics Overlay — Main entry point.
No login, no credentials, no setup needed.
Just run it and play music!
"""

import os
import sys
import ctypes

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from config import load_config
from spotify_client import MediaSession
from lyrics_fetcher import LyricsFetcher
from lyrics_window import LyricsWindow


def _resource_path(*parts: str) -> str:
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def main():
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("LyPy.Desktop")
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setApplicationName("LyPy")
    app.setApplicationDisplayName("LyPy")
    app.setOrganizationName("LyPy")
    app.setOrganizationDomain("lypy.app")
    app_icon = QIcon(_resource_path("assets", "app_icon.png"))
    if not app_icon.isNull():
        app.setWindowIcon(app_icon)

    # Dark application style
    app.setStyle("Fusion")
    dark_palette = app.palette()
    dark_palette.setColor(dark_palette.Window, Qt.black)
    dark_palette.setColor(dark_palette.WindowText, Qt.white)
    app.setPalette(dark_palette)

    config = load_config()

    # Build service objects — no credentials needed!
    media = MediaSession()
    lyrics = LyricsFetcher()

    # Launch overlay
    window = LyricsWindow(config, media, lyrics)
    if not app_icon.isNull():
        window.setWindowIcon(app_icon)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
