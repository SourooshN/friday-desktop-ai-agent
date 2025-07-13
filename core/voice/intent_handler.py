# core/voice/intent_handler.py

import pyttsx3
import webbrowser
import subprocess
from datetime import datetime
import re

from core.voice.system_control import increase_volume, decrease_volume, mute_volume
from core.brain.agent_router import route_task

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)

def speak(text: str):
    """Speak out the given text and also print it."""
    print(f"🗣️ Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def handle_intent(text: str):
    """Detect intents, handle system commands first, otherwise route to LLM."""
    cmd = text.lower().strip()
    
    # 1) TIME
    if "time" in cmd:
        now = datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}")
        return

    # 2) SYSTEM CONTROL: Notepad & Browser
    if "open notepad" in cmd:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")
        return

    if "open google" in cmd:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
        return

    # 3) VOLUME CONTROLS (catch all variants)
    # Any phrase containing "volume" plus a keyword
    if re.search(r"(increase|turn up|volume up|raise).*(volume)", cmd) or re.search(r"(volume up|turn up volume|raise volume)", cmd):
        increase_volume()
        speak("Volume increased.")
        return

    if re.search(r"(decrease|lower|turn down|reduce).*(volume)", cmd) or re.search(r"(volume down|turn down volume|lower volume|reduce volume|lower the volume|reduce the volume)", cmd):
        decrease_volume()
        speak("Volume decreased.")
        return

    if "mute" in cmd and "volume" in cmd:
        mute_volume()
        speak("Volume muted.")
        return

    # 4) ANYTHING ELSE → Route to the appropriate LLM via agent_router
    response = route_task(text)
    print(f"🤖 Friday: {response}")
    speak(response)
