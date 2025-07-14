# main.py

from dotenv import load_dotenv
import threading
import sys

from core.input.input_logger import start_listeners
from core.ui.tray_icon import start_tray_in_thread
from core.ui.hotkey_listener import start_hotkey_listener
from core.voice.voice_interface import recognize_speech_and_act
from core.brain.self_optimizer import summarize_interactions, print_summary
from core.brain.routing_optimizer import optimize_routing
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def run_self_optimizer():
    summary = summarize_interactions()
    print_summary(summary)

def main():
    # Load environment variables
    load_dotenv()
    print("🤖 Friday AI Assistant is starting up...")

    # 1) Start the input logger in its own thread
    threading.Thread(
        target=start_listeners,
        name="InputLoggerThread",
        daemon=True
    ).start()
    print("🎧 Input logger running.")

    # 2) Launch the system tray icon (right-click → Open GUI / Quit)
    start_tray_in_thread()
    print("🍊 System tray icon launched. Right-click to open GUI or Quit.")

    # 3) Start the global hotkey listener (Ctrl+Shift+F)
    threading.Thread(
        target=start_hotkey_listener,
        name="HotkeyListenerThread",
        daemon=True
    ).start()
    print("⌨️ Listening for global hotkey: Ctrl+Shift+F")

    # 4) Schedule daily tasks (self-summary at 08:00; routing optimizer at 08:05)
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_self_optimizer,
        CronTrigger(hour=8, minute=0),
        id="daily_summary"
    )
    scheduler.add_job(
        optimize_routing,
        CronTrigger(hour=8, minute=5),
        id="routing_optimizer"
    )
    scheduler.start()
    print("📅 Scheduled daily summary at 08:00.")
    print("🔄 Scheduled routing optimizer at 08:05.")

    # 5) Voice loop fallback (if GUI/hotkey not used)
    try:
        while True:
            recognize_speech_and_act()
    except (KeyboardInterrupt, SystemExit):
        print("👋 Shutting down Friday...")
        sys.exit(0)

if __name__ == "__main__":
    main()
