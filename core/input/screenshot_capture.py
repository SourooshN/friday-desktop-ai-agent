import pyautogui
from core.utils.logger_utils import get_timestamp, ensure_log_dir

def take_screenshot():
    ensure_log_dir()
    timestamp = get_timestamp().replace(":", "-").replace(" ", "_")
    filename = f"screenshot_{timestamp}.png"
    filepath = f"./logs/{filename}"
    pyautogui.screenshot(filepath)
    print(f"[📸] Screenshot saved: {filepath}")
