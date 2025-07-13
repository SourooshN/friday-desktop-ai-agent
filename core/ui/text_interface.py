# core/ui/text_interface.py

import tkinter as tk
from core.brain.agent_router import route_and_query
from core.voice.intent_handler import speak_response

def open_text_prompt():
    """Launch a simple GUI window to type commands for Friday."""
    def on_submit():
        user_input = entry.get().strip()
        prompt.destroy()
        if not user_input:
            return
        # Send through the router → model → memory → speak
        try:
            resp = route_and_query("text", user_input)
            speak_response(resp)
        except Exception as e:
            speak_response(f"Sorry, I hit an error: {e}")

    prompt = tk.Tk()
    prompt.title("Friday — Text Input")
    prompt.geometry("400x140")
    tk.Label(prompt, text="Enter your command:").pack(pady=(10, 5))
    entry = tk.Entry(prompt, width=50)
    entry.pack(padx=10)
    entry.focus()
    tk.Button(prompt, text="Submit", command=on_submit).pack(pady=10)
    prompt.mainloop()
