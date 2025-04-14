import tkinter as tk
from tkinter import messagebox

# === Main GUI Window ===
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

        # Buttons
        tk.Button(
            self,
            text="Start Training Session",
            font=("Helvetica", 14),
            width=30,
            command=self.start_session
        ).pack(pady=10)

        tk.Button(
            self,
            text="Options",
            font=("Helvetica", 14),
            width=30,
            command=self.open_options
        ).pack(pady=10)

        tk.Button(
            self,
            text="View Phrasebook",
            font=("Helvetica", 14),
            width=30,
            command=self.view_phrasebook
        ).pack(pady=10)

        tk.Button(
            self,
            text="Exit",
            font=("Helvetica", 14),
            width=30,
            command=self.quit
        ).pack(pady=20)

    # === Placeholder Functions ===
    def start_session(self):
        messagebox.showinfo("Session", "This will start the training session.")

    def open_options(self):
        messagebox.showinfo("Options", "Options screen not yet implemented.")

    def view_phrasebook(self):
        messagebox.showinfo("Phrasebook", "Phrasebook viewer coming soon.")

# === Launch App ===
if __name__ == "__main__":
    app = ATCVoiceTrainerApp()
    app.mainloop()
