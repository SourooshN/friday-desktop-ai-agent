# core/ui/tray_icon.py

import threading
import os
import sys
from PIL import Image
import pystray

def _run_tray():
    # locate project root (../../ from this file)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    icon_path = os.path.join(base, 'assets', 'friday_icon.ico')

    try:
        image = Image.open(icon_path)
    except FileNotFoundError:
        print(f"[TrayIcon] ERROR: Could not find icon at {icon_path}")
        return

    # menu callbacks
    def on_open(icon, item):
        # call our text GUI
        from core.ui.text_interface import open_text_prompt
        open_text_prompt()

    def on_quit(icon, item):
        icon.stop()
        sys.exit(0)

    menu = pystray.Menu(
        pystray.MenuItem('Open GUI', on_open),
        pystray.MenuItem('Quit', on_quit)
    )

    tray = pystray.Icon('Friday', image, 'Friday', menu)
    tray.run()

def start_tray_in_thread():
    threading.Thread(target=_run_tray, name="TrayIconThread", daemon=True).start()
