import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

def speak(text):
    """Converts text to speech and plays it."""
    tts = gTTS(text=text, lang='en')
    filename = "voice_test.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def listen():
    """Listens to the microphone and returns recognized speech."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Say something...")
        audio = recognizer.listen(source)
        try:
            print("🧠 Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            speak(f"You said: {text}")
        except sr.UnknownValueError:
            print("❗ Could not understand audio.")
            speak("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"❗ Request error: {e}")
            speak("Sorry, I couldn't reach the speech service.")

if __name__ == "__main__":
    listen()
