# training_session_gui.py

import tkinter as tk
from tkinter import messagebox
import random
import datetime
import os
import pyttsx3
from session_utils import record_audio, transcribe_audio, match_phrase

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# FAA Phrases (import inside instead of phrasebook.py to stay modular)
faa_phrases = {
    "Request taxi to runway two seven": {"expected_controller": "Taxi to runway two seven via Alpha, Bravo"},
    "Ready for departure runway one eight": {"expected_controller": "Cleared for takeoff runway one eight"},
    "Inbound for landing, three mile final": {"expected_controller": "Cleared to land runway two seven"},
    "Holding short of runway one six": {"expected_controller": "Hold short of runway one six"},
    "Request cross runway two seven": {"expected_controller": "Cross runway two seven and contact ground on point eight"}
}

flight_sequence = [
    {"pilot": "Ground, this is Tiger 5 requesting radio check", "expected_controller": "Tiger 5, radio check loud and clear"},
    {"pilot": "Request taxi to runway two seven", "expected_controller": "Taxi to runway two seven via Alpha, Bravo"},
    {"pilot": "Holding short of runway two seven", "expected_controller": "Hold short of runway two seven"},
    {"pilot": "Ready for departure runway two seven", "expected_controller": "Cleared for takeoff runway two seven"},
    {"pilot": "Inbound for landing, three mile final", "expected_controller": "Cleared to land runway two seven"}
]

class TrainingSessionWindow(tk.Toplevel):
    def __init__(self, parent, config, custom_phrases):
        super().__init__(parent)
        self.title("ATC Training Session")
        self.geometry("700x550")
        self.configure(bg="#1a1a1a")

        self.config_data = config
        self.custom_phrases = custom_phrases
        self.log_file = self.create_log_file()

        self.withdraw()  # Hide the Training Session window initially
        self.select_mode()  # Open the mode selection window

        self.create_widgets()

    def create_widgets(self):
    # Main container
        main_frame = tk.Frame(self, bg="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

     # Scrollable chat box
        self.chat_display = tk.Text(main_frame, wrap="word", font=("Helvetica", 12),
                                bg="#262626", fg="white", height=20)
        self.chat_display.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_frame, command=self.chat_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.chat_display.config(yscrollcommand=scrollbar.set, state="disabled")

    # Recording indicator
        self.recording_label = tk.Label(self, text="", font=("Helvetica", 12, "bold"),
                                    fg="#00ffcc", bg="#1a1a1a")
        self.recording_label.pack(pady=(0, 5))

    # Run button
        self.run_button = tk.Button(self, text="▶️ Run", command=self.run_round,
                                font=("Helvetica", 13), bg="#00cc99", fg="black", width=16)
        self.run_button.pack(pady=5)

    # End Session button
        self.end_button = tk.Button(self, text="❌ End Session", command=self.end_session,
                                font=("Helvetica", 12), bg="#333333", fg="white", width=16)
        self.end_button.pack(pady=10)

    def create_log_file(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/gui_session_log_{timestamp}.csv"
        with open(filename, "w") as f:
            f.write("Time,Pilot Phrase,User Transcript,Matched As,Score\n")
        return filename

    def select_mode(self):
        self.mode_window = tk.Toplevel(self)
        self.mode_window.title("Select Training Mode")
        self.mode_window.geometry("350x200")
        self.mode_window.configure(bg="#1a1a1a")

        tk.Label(self.mode_window, text="Choose a training mode:", font=("Helvetica", 14), fg="#00ffcc", bg="#1a1a1a").pack(pady=20)

        tk.Button(self.mode_window, text="🚀 Rapid Fire Mode", font=("Helvetica", 12), width=25,
                  bg="#262626", fg="white", command=self.start_rapid_mode).pack(pady=10)

        tk.Button(self.mode_window, text="🧭 Full Flight Scenario", font=("Helvetica", 12), width=25,
                  bg="#262626", fg="white", command=self.start_flight_mode).pack(pady=5)

    def start_rapid_mode(self):
        self.training_mode = "rapid"
        self.mode_window.destroy()
        self.deiconify()  # Show the main window
        self.phrase_pool = self.load_phrase_pool()
        self.prepare_round()

    def start_flight_mode(self):
        self.training_mode = "flight"
        self.mode_window.destroy()
        self.deiconify()  # Show the main window
        self.sequence_index = 0
        self.phrase_pool = flight_sequence
        self.prepare_round()

    def load_phrase_pool(self):
        from phrasebook import faa_phrases
        base_pool = [{"pilot": call, "expected_controller": data["expected_response"]} for call, data in faa_phrases.items()]
        return base_pool + self.custom_phrases


    def prepare_round(self):
        if self.training_mode == "rapid":
            self.round_data = random.choice(self.phrase_pool)
        elif self.training_mode == "flight":
            if self.sequence_index >= len(self.phrase_pool):
                self.append_chat("✅ FLIGHT COMPLETE")
                self.run_button.config(state="disabled")
                return
            self.round_data = self.phrase_pool[self.sequence_index]

        self.append_chat(f"🛩️ PILOT: {self.round_data['pilot']}\n\n(Press ▶️ Run when ready)", clear=False)
        self.run_button.config(state="normal")

    def run_round(self):
        self.run_button.config(state="disabled")
        speak(self.round_data["pilot"])

        self.recording_label.config(text="🎙️ Recording...")
        self.update()
        filename = record_audio()
        self.recording_label.config(text="")  # clear after recording

        transcript = transcribe_audio(filename)
        matched, score = match_phrase(transcript)

        self.append_chat(f"🎧 YOU: {transcript}")
        self.append_chat(f"✅ MATCH: {matched}")
        self.append_chat(f"🧠 SCORE: {score}%\n" + "-" * 50)

        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()},{self.round_data['pilot']},{transcript},{matched},{score}\n")

        if self.training_mode == "flight":
            self.sequence_index += 1

        self.after(500, self.prepare_round)

    def append_chat(self, text, clear=False):
        self.chat_display.config(state="normal")
        if clear:
            self.chat_display.delete(1.0, tk.END)
        self.chat_display.insert(tk.END, f"{text}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")


    def end_session(self):
        messagebox.showinfo("Session Ended", f"Session log saved to:\n{self.log_file}")
        self.destroy()
