# core/voice/voice_interface.py

import speech_recognition as sr
from core.voice.intent_handler import handle_intent
import pyttsx3

engine = pyttsx3.init()

def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_speech_and_act():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("🧠 Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"📥 You said: {command}")
        handle_intent(command)

    except sr.UnknownValueError:
        speak("❗ Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        speak(f"❗ Could not request results; {e}")
