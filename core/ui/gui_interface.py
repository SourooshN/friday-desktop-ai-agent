# core/ui/gui_interface.py

import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from core.brain.agent_router import route_and_query
from core.voice.intent_handler import speak_response

class FridayGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Friday Assistant")
        self.window.geometry("500x400")

        # Chat display (read-only)
        self.chat_display = ScrolledText(self.window, state="disabled", wrap="word")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Entry field for your command
        self.entry = tk.Entry(self.window)
        self.entry.pack(fill="x", padx=5, pady=(0,5))
        self.entry.bind("<Return>", lambda event: self.send())

        # “Send” button
        self.send_button = tk.Button(self.window, text="Send", command=self.send)
        self.send_button.pack(pady=(0,5))

    def append_message(self, sender: str, message: str):
        self.chat_display["state"] = "normal"
        self.chat_display.insert(tk.END, f"{sender}: {message}\n")
        self.chat_display["state"] = "disabled"
        self.chat_display.see(tk.END)

    def send(self):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)

        # Show your message
        self.append_message("You", user_text)

        # Route through the agent router and get a response
        response = route_and_query("text", user_text)

        # Show Friday’s response in the window
        self.append_message("Friday", response)

        # Speak it asynchronously
        threading.Thread(target=speak_response, args=(response,), daemon=True).start()

    def run(self):
        self.window.mainloop()
