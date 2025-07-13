# core/ui/tray_icon.py

import sys
import threading
from PIL import Image
import pystray

from core.brain.self_optimizer import summarize_interactions, print_summary
from core.brain.routing_optimizer import optimize_routing

ICON_PATH = "assets/friday_icon.png"

def on_run_summary(icon, item):
    summary = summarize_interactions()
    print_summary(summary)

def on_optimize_routing(icon, item):
    optimize_routing()

def on_exit(icon, item):
    icon.stop()
    sys.exit(0)

def create_tray():
    image = Image.open(ICON_PATH)
    menu = pystray.Menu(
        pystray.MenuItem("Run Memory Summary", on_run_summary),
        pystray.MenuItem("Optimize Routing", on_optimize_routing),
        pystray.MenuItem("Exit Friday", on_exit),
    )
    icon = pystray.Icon("Friday", image, "Friday AI", menu)
    icon.run()

def start_tray_in_thread():
    threading.Thread(target=create_tray, daemon=True).start()
