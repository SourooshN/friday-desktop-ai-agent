# core/input/input_logger.py

from pynput import keyboard, mouse
from core.utils.logger_utils import log_event

keyboard_listener = None
mouse_listener = None

def on_click(x, y, button, pressed):
    event = "Mouse click"
    details = f"{'Pressed' if pressed else 'Released'} {button} at ({x}, {y})"
    log_event(event, details)

def on_press(key):
    try:
        if key == keyboard.Key.esc:
            print("\n👋 Friday is shutting down gracefully. See you soon!")
            stop_listeners()
            exit(0)
        event = "Key press"
        details = f"Key: {key.char}"
    except AttributeError:
        event = "Special key press"
        details = f"Key: {key}"
    log_event(event, details)

def start_listeners():
    global keyboard_listener, mouse_listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()

def stop_listeners():
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()
