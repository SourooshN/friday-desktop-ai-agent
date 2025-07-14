# core/ui/text_interface.py

import threading
import tkinter as tk
from tkinter import messagebox

from core.brain.agent_router import route_and_query
from core.voice.intent_handler import speak_response

def _show_prompt():
    # 1) Build the window
    root = tk.Tk()
    root.title("Friday — Text Input")
    root.geometry("400x120")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    tk.Label(root, text="Enter your command:").pack(pady=(10, 5))
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10)
    entry.focus_force()

    # 2) Handler for Submit
    def on_submit():
        text = entry.get().strip()
        if not text:
            return

        try:
            # force routing to "general" so select_model_for_intent always returns a valid model
            response = route_and_query("general", text)
            # speak it
            speak_response(response)
            # show popup
            messagebox.showinfo("Friday Response", response, parent=root)
        except Exception as e:
            # catch Ollama errors (timeout, invalid path, etc.)
            messagebox.showerror("Friday Error", f"[X ERROR] {e}", parent=root)
        finally:
            root.destroy()

    entry.bind("<Return>", lambda e: on_submit())
    tk.Button(root, text="Submit", command=on_submit).pack(pady=10)

    root.mainloop()

def open_text_prompt():
    # run the prompt in its own daemon thread
    threading.Thread(target=_show_prompt, daemon=True).start()
