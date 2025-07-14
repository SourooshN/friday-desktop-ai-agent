# core/voice/intent_handler.py

import threading
import pyttsx3

from core.brain.agent_router import route_and_query

_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def speak_response(response: str):
    """
    Queue up a TTS response on its own thread so that
    runAndWait() never collides with an already-running loop.
    """
    engine = _get_engine()
    engine.say(response)
    threading.Thread(target=engine.runAndWait, daemon=True).start()

def handle_intent(command: str) -> str:
    """
    Take the raw spoken text, send it through Friday's
    agent_router, speak it, and return the text.
    """
    try:
        # route_and_query(category, text)
        # For voice we use the 'voice' slot in routing_config.json
        response = route_and_query("voice", command)
    except Exception as e:
        response = f"[X ERROR] {e}"
    # speak back
    speak_response(response)
    return response
