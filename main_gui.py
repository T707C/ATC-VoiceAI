from phrasebook import faa_phrases, cowboy_phrases
import tkinter as tk
from tkinter import messagebox, simpledialog
from phrasebook import faa_phrases, cowboy_phrases


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
