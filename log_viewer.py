import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox

class LogViewerWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Session Log Viewer")
        self.geometry("800x500")
        self.configure(bg="#1a1a1a")

        self.create_widgets()
        self.populate_file_list()

    def create_widgets(self):
        tk.Label(self, text="📂 Select a session log to view", font=("Helvetica", 14, "bold"),
                 fg="#00ffcc", bg="#1a1a1a").pack(pady=10)

        self.file_listbox = tk.Listbox(self, font=("Helvetica", 11), bg="#262626", fg="white", height=6)
        self.file_listbox.pack(pady=5, fill="x", padx=20)
        self.file_listbox.bind("<<ListboxSelect>>", self.load_selected_log)

        self.tree = ttk.Treeview(self, columns=("Time", "Pilot", "Transcript", "Match", "Score"), show="headings")
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#1a1a1a", foreground="white", fieldbackground="#1a1a1a", rowheight=24)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#262626", foreground="#00ffcc")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

    def populate_file_list(self):
        self.file_listbox.delete(0, tk.END)
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logs = [f for f in os.listdir("logs") if f.endswith(".csv")]
        if not logs:
            self.file_listbox.insert(tk.END, "No logs found.")
        else:
            for file in logs:
                self.file_listbox.insert(tk.END, file)

    def load_selected_log(self, event):
        selection = self.file_listbox.curselection()
        if not selection:
            return
        filename = self.file_listbox.get(selection[0])
        filepath = os.path.join("logs", filename)

        self.tree.delete(*self.tree.get_children())

        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 5:
                        self.tree.insert("", tk.END, values=row[:5])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log file:\n{e}")
