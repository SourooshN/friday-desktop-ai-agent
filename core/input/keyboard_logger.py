import os
import threading
from pynput import mouse, keyboard
from core.utils.logger_utils import ensure_log_dir, get_timestamp, write_log
from core.input.screenshot_capture import take_screenshot

stop_flag = threading.Event()

def on_press(key):
    if key == keyboard.Key.esc:
        stop_flag.set()
        print("[🔴] Escape pressed. Exiting logger...")
        return False  # Stop keyboard listener
    try:
        log_entry = f"[KEYDOWN] {get_timestamp()} - {key.char}\n"
    except AttributeError:
        log_entry = f"[KEYDOWN] {get_timestamp()} - {key}\n"
    write_log(log_entry)

def on_click(x, y, button, pressed):
    if pressed:
        log_entry = f"[CLICK] {get_timestamp()} - {button} at ({x}, {y})\n"
        write_log(log_entry)
        take_screenshot()

def start_keyboard_mouse_logger():
    ensure_log_dir()
    print("[🟢] Keyboard and mouse logger started. Press ESC to exit.")

    with keyboard.Listener(on_press=on_press) as kl, \
         mouse.Listener(on_click=on_click) as ml:
        while not stop_flag.is_set():
            kl.join()
            ml.join()
