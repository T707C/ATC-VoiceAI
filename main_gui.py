import tkinter as tk
from tkinter import messagebox, simpledialog
from phrasebook import phrasebook
from session_runner import run_session  # ⬅️ LIVE session backend

# === Global Session Config ===
session_config = {
    "mode": "FAA",
    "cowboy_mode": False,
    "phrase_matching": True,
    "live_feedback": True
}

custom_phrase_pairs = []

# === Main GUI Application ===
class ATCVoiceTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ATC Voice AI Trainer")
        self.geometry("600x400")
        self.configure(bg="#1a1a1a")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self,
            text="ATC Voice AI Trainer",
            font=("Helvetica", 24, "bold"),
            fg="#00ffcc",
            bg="#1a1a1a"
        )
        title.pack(pady=30)

        button_style = {
            "font": ("Helvetica", 14),
            "width": 30,
            "bg": "#262626",
            "fg": "#ffffff",
            "activebackground": "#00cc99",
            "activeforeground": "#ffffff",
            "bd": 0,
            "highlightthickness": 0
        }

        tk.Button(self, text="Start Training Session", command=self.start_session, **button_style).pack(pady=10)
        tk.Button(self, text="Options", command=self.open_options, **button_style).pack(pady=10)
        tk.Button(self, text="View Phrasebook", command=self.view_phrasebook, **button_style).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit, **button_style).pack(pady=20)

    def start_session(self):
        self.withdraw()  # Hide GUI during terminal session
        try:
            run_session(session_config, custom_phrase_pairs)
        except Exception as e:
            messagebox.showerror("Error", f"Session failed to start:\n{e}")
        self.deiconify()  # Show GUI again after session

    def open_options(self):
        OptionsWindow(self)

    def view_phrasebook(self):
        PhrasebookWindow(self)


# === Options Window ===
class OptionsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Options")
        self.geometry("400x400")
        self.configure(bg="#1a1a1a")
        self.create_options_ui()

    def create_options_ui(self):
        label = tk.Label(self, text="Session Settings", font=("Helvetica", 16, "bold"), fg="#00ffcc", bg="#1a1a1a")
        label.pack(pady=15)

        # === Mode Dropdown ===
        mode_label = tk.Label(self, text="Training Mode:", font=("Helvetica", 12), fg="white", bg="#1a1a1a")
        mode_label.pack()

        self.mode_var = tk.StringVar(value=session_config["mode"])
        mode_dropdown = tk.OptionMenu(self, self.mode_var, "FAA", "Military", "Custom")
        mode_dropdown.config(font=("Helvetica", 12), bg="#262626", fg="white", width=20)
        mode_dropdown["menu"].config(bg="#262626", fg="white")
        mode_dropdown.pack(pady=5)

        self.create_toggle("Cowboy Mode", "cowboy_mode")
        self.create_toggle("Phrase Matching", "phrase_matching")
        self.create_toggle("Live Feedback", "live_feedback")

        tk.Button(
            self,
            text="➕ Add Custom Phrase Pair",
            font=("Helvetica", 12),
            bg="#333333",
            fg="white",
            command=self.add_custom_phrase
        ).pack(pady=20)

        tk.Button(
            self,
            text="✅ Done",
            font=("Helvetica", 12),
            bg="#00cc99",
            fg="black",
            width=15,
            command=self.save_and_close
        ).pack(pady=10)

    def create_toggle(self, label_text, config_key):
        def toggle():
            session_config[config_key] = not session_config[config_key]
            button.config(text=f"{label_text}: {'On' if session_config[config_key] else 'Off'}")

        button = tk.Button(
            self,
            text=f"{label_text}: {'On' if session_config[config_key] else 'Off'}",
            font=("Helvetica", 12),
            width=30,
            bg="#262626",
            fg="white",
            command=toggle
        )
        button.pack(pady=5)

    def add_custom_phrase(self):
        pilot_phrase = simpledialog.askstring("Pilot Phrase", "Enter the phrase the pilot will say:")
        if not pilot_phrase:
            return
        controller_phrase = simpledialog.askstring("ATC Response", "Enter the expected ATC response:")
        if not controller_phrase:
            return

        custom_phrase_pairs.append({
            "pilot": pilot_phrase.strip(),
            "expected_controller": controller_phrase.strip()
        })
        messagebox.showinfo("Success", "✅ Custom phrase added successfully.")

    def save_and_close(self):
        session_config["mode"] = self.mode_var.get()
        self.destroy()


# === Phrasebook Viewer Window ===
class PhrasebookWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Phrasebook")
        self.geometry("500x500")
        self.configure(bg="#1a1a1a")
        self.create_ui()

    def create_ui(self):
        title = tk.Label(self, text="📘 ATC Phrasebook", font=("Helvetica", 16, "bold"), fg="#00ffcc", bg="#1a1a1a")
        title.pack(pady=10)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var, font=("Helvetica", 12), width=40)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", self.update_results)

        self.text_frame = tk.Frame(self, bg="#1a1a1a")
        self.text_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_box = tk.Text(self.text_frame, wrap="word", font=("Helvetica", 11), bg="#262626", fg="white")
        self.results_box.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.text_frame, command=self.results_box.yview)
        scrollbar.pack(side="right", fill="y")

        self.results_box.config(yscrollcommand=scrollbar.set)
        self.update_results()

    def update_results(self, event=None):
        query = self.search_var.get().strip().lower()
        self.results_box.delete(1.0, tk.END)

        matches = [
            (phrase, explanation)
            for phrase, explanation in phrasebook.items()
            if query in phrase.lower()
        ]

        if matches:
            for phrase, explanation in matches:
                self.results_box.insert(tk.END, f"\n🛩️ {phrase}\n   📘 {explanation}\n")
        else:
            self.results_box.insert(tk.END, "\n⚠ No matching phrase found.")


# === Launch the App ===
if __name__ == "__main__":
    app = ATCVoiceTrainerApp()
    app.mainloop()
