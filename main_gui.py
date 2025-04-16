from phrasebook import faa_phrases, cowboy_phrases
import tkinter as tk
from tkinter import messagebox, simpledialog
from phrasebook import faa_phrases, cowboy_phrases
from training_session_gui import TrainingSessionWindow
from log_viewer import LogViewerWindow


class PhrasebookWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Phrasebook")
        self.geometry("600x600")
        self.configure(bg="#1a1a1a")
        self.create_ui()

    def create_ui(self):
        tk.Label(self, text="📘 ATC Phrasebook", font=("Helvetica", 16, "bold"),
                 fg="#00ffcc", bg="#1a1a1a").pack(pady=10)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var, font=("Helvetica", 12), width=40)
        search_entry.pack(pady=5)
        search_entry.bind("<KeyRelease>", self.update_results)

        self.text_frame = tk.Frame(self, bg="#1a1a1a")
        self.text_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_box = tk.Text(self.text_frame, wrap="word", font=("Helvetica", 11),
                                   bg="#262626", fg="white")
        self.results_box.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.text_frame, command=self.results_box.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_box.config(yscrollcommand=scrollbar.set)
        self.update_results()

    def update_results(self, event=None):
        query = self.search_var.get().strip().lower()
        self.results_box.config(state="normal")
        self.results_box.delete(1.0, tk.END)

        def show_section(title, data_dict):
            self.results_box.insert(tk.END, f"\n🔷 {title}\n", "section")
            found = False
            for call, data in data_dict.items():
                if query in call.lower():
                    found = True
                    response = data.get("expected_response", "N/A")
                    definition = data.get("definition", "No description available.")
                    self.results_box.insert(tk.END, f"\n🛩️ Pilot: {call}\n🎧 ATC: {response}\n📘 Meaning: {definition}\n")
            if not found:
                self.results_box.insert(tk.END, "\n⚠ No matching phrase found in this section.\n")

        show_section("FAA Phraseology", faa_phrases)
        show_section("Cowboy Phraseology", cowboy_phrases)

        self.results_box.tag_config("section", foreground="#00ccff", font=("Helvetica", 12, "bold"))
        self.results_box.config(state="disabled")


class ATCVoiceTrainerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATC Voice AI Trainer")
        self.geometry("600x460")
        self.configure(bg="#1a1a1a")
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="ATC Voice AI Trainer", font=("Helvetica", 24, "bold"), fg="#00ffcc", bg="#1a1a1a")
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
        tk.Button(self, text="Replay Previous Sessions", command=self.view_logs, **button_style).pack(pady=10)
        tk.Button(self, text="Exit", command=self.quit, **button_style).pack(pady=20)

    def start_session(self):
            TrainingSessionWindow(self, {}, [])

    def open_options(self):
        messagebox.showinfo("Options", "Options window goes here.")

    def view_phrasebook(self):
        PhrasebookWindow(self)

    def view_logs(self):
        LogViewerWindow(self)


if __name__ == "__main__":
    app = ATCVoiceTrainerApp()
    app.mainloop()
