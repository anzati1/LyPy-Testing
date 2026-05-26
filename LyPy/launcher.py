import ctypes
import traceback

from config import ensure_config_dir_writable


def _show_error(title: str, message: str):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)


def main() -> int:
    try:
        ensure_config_dir_writable()
    except Exception as exc:
        _show_error(
            "LyPy Startup Error",
            "LyPy cannot access its settings folder.\n\n"
            f"{exc}\n\n"
            "Check folder permissions in your AppData directory.",
        )
        return 1

    try:
        from main import main as app_main
        app_main()
        return 0
    except Exception:
        _show_error(
            "LyPy Startup Error",
            "LyPy failed to start.\n\n"
            f"{traceback.format_exc()}",
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
