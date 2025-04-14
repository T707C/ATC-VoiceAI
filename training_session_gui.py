import tkinter as tk
from tkinter import messagebox
import random
import datetime
import os
import pyttsx3
from session_utils import record_audio, transcribe_audio, match_phrase

# === Text-to-Speech ===
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

# === Sample Phrase Pools ===
faa_pairs = [
    {"pilot": "Request taxi to runway two seven", "expected_controller": "Taxi to runway two seven via Alpha, Bravo"},
    {"pilot": "Ready for departure runway one eight", "expected_controller": "Cleared for takeoff runway one eight"},
    {"pilot": "Inbound for landing, three mile final", "expected_controller": "Cleared to land runway two seven"},
    {"pilot": "Holding short of runway one six", "expected_controller": "Hold short of runway one six"},
    {"pilot": "Request cross runway two seven", "expected_controller": "Cross runway two seven and contact ground on point eight"}
]

military_pairs = [
    {"pilot": "Approach, three in the green", "expected_controller": "Cleared to land runway one six"},
    {"pilot": "Ready for departure, IFR clearance received", "expected_controller": "Cleared for takeoff runway one eight, maintain runway heading"}
]

# === GUI Session Class ===
class TrainingSessionWindow(tk.Toplevel):
    def __init__(self, parent, config, custom_phrases):
        super().__init__(parent)
        self.title("ATC Training Session")
        self.geometry("700x500")
        self.configure(bg="#1a1a1a")

        self.config_data = config
        self.custom_phrases = custom_phrases
        self.phrase_pairs = self.load_phrase_pool()
        self.log_file = self.create_log_file()

        self.create_widgets()
        self.next_round()

    def create_widgets(self):
        self.title_label = tk.Label(self, text="ATC Simulation", font=("Helvetica", 20, "bold"), fg="#00ffcc", bg="#1a1a1a")
        self.title_label.pack(pady=15)

        self.pilot_label = tk.Label(self, text="🛩️ Pilot will speak...", font=("Helvetica", 14), fg="white", bg="#1a1a1a")
        self.pilot_label.pack(pady=10)

        self.user_response = tk.Label(self, text="🎧 Your Response:", font=("Helvetica", 12), fg="#cccccc", bg="#1a1a1a", wraplength=600)
        self.user_response.pack(pady=5)

        self.feedback = tk.Label(self, text="", font=("Helvetica", 12), fg="#00cc99", bg="#1a1a1a", wraplength=600)
        self.feedback.pack(pady=5)

        self.score_label = tk.Label(self, text="", font=("Helvetica", 12, "bold"), fg="#ffffff", bg="#1a1a1a")
        self.score_label.pack(pady=5)

        tk.Button(
            self, text="▶️ Respond", command=self.run_response,
            font=("Helvetica", 13), bg="#00cc99", fg="black", width=15
        ).pack(pady=10)

        tk.Button(
            self, text="❌ End Session", command=self.end_session,
            font=("Helvetica", 12), bg="#333333", fg="white", width=15
        ).pack(pady=10)

    def load_phrase_pool(self):
        mode = self.config_data.get("mode", "FAA")
        base_pool = []

        if mode == "FAA":
            base_pool = faa_pairs
        elif mode == "Military":
            base_pool = military_pairs
        else:
            base_pool = faa_pairs + military_pairs

        return base_pool + self.custom_phrases

    def create_log_file(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"logs/gui_session_log_{timestamp}.csv"
        with open(filename, "w") as f:
            f.write("Time,Pilot Phrase,User Transcript,Matched As,Score\n")
        return filename

    def next_round(self):
        self.round_data = random.choice(self.phrase_pairs)
        self.pilot_label.config(text=f"🛩️ Pilot says: \"{self.round_data['pilot']}\"")
        speak(self.round_data["pilot"])
        self.user_response.config(text="🎧 Your Response:")
        self.feedback.config(text="")
        self.score_label.config(text="")

    def run_response(self):
        record_audio()
        transcript = transcribe_audio()
        self.user_response.config(text=f"🎧 You said: \"{transcript}\"")

        matched, score = match_phrase(transcript, cowboy_mode=self.config_data.get("cowboy_mode", False))
        self.feedback.config(text=f"Expected: \"{self.round_data['expected_controller']}\"\nMatched: \"{matched}\"")
        self.score_label.config(text=f"🧠 Score: {score}%")

        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()},{self.round_data['pilot']},{transcript},{matched},{score}\n")

        self.after(500, self.next_round)

    def end_session(self):
        messagebox.showinfo("Session Ended", f"Session log saved to:\n{self.log_file}")
        self.destroy()
