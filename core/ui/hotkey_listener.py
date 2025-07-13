# core/ui/hotkey_listener.py

from pynput import keyboard
from core.ui.text_interface import open_text_prompt
from core.voice.voice_interface import recognize_speech_and_act

def on_activate_text():
    """Ctrl+Shift+T → open text prompt."""
    open_text_prompt()

def on_activate_voice():
    """Ctrl+Shift+F → start voice recognition."""
    recognize_speech_and_act()

def start_hotkey_listener():
    """
    Listen globally for:
      • Ctrl+Shift+T to open the text prompt
      • Ctrl+Shift+F to begin voice recognition
    """
    hotkeys = {
        '<ctrl>+<shift>+t': on_activate_text,
        '<ctrl>+<shift>+f': on_activate_voice,
    }
    with keyboard.GlobalHotKeys(hotkeys) as listener:
        listener.join()
