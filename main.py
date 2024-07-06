import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

class StudyPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Planner")
        self.root.geometry("400x600")

        self.sessions = []
        self.load_sessions()

        self.subject_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        self.notes_var = tk.StringVar()

        self.create_widgets()
        self.display_sessions()

    def create_widgets(self):
        tk.Label(self.root, text="Subject").pack(pady=5)
        tk.Entry(self.root, textvariable=self.subject_var).pack(pady=5)

        tk.Label(self.root, text="Date (YYYY-MM-DD)").pack(pady=5)
        tk.Entry(self.root, textvariable=self.date_var).pack(pady=5)

        tk.Label(self.root, text="Start Time (HH:MM)").pack(pady=5)
        tk.Entry(self.root, textvariable=self.start_time_var).pack(pady=5)

        tk.Label(self.root, text="End Time (HH:MM)").pack(pady=5)
        tk.Entry(self.root, textvariable=self.end_time_var).pack(pady=5)

        tk.Label(self.root, text="Notes").pack(pady=5)
        tk.Entry(self.root, textvariable=self.notes_var).pack(pady=5)

        tk.Button(self.root, text="Add Session", command=self.add_session).pack(pady=20)

        self.session_frame = tk.Frame(self.root)
        self.session_frame.pack(pady=10)

    def add_session(self):
        subject = self.subject_var.get()
        date = self.date_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        notes = self.notes_var.get()

        if not (subject and date and start_time and end_time):
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(start_time, '%H:%M')
            datetime.strptime(end_time, '%H:%M')
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid date or time format")
            return

        session = {
            "subject": subject,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "notes": notes,
            "completed": False
        }

        self.sessions.append(session)
        self.save_sessions()
        self.display_sessions()

    def display_sessions(self):
        for widget in self.session_frame.winfo_children():
            widget.destroy()

        for idx, session in enumerate(self.sessions):
            session_str = f"{session['subject']} on {session['date']} from {session['start_time']} to {session['end_time']}"
            label = tk.Label(self.session_frame, text=session_str)
            label.grid(row=idx, column=0, sticky="w")
            if session['completed']:
                label.config(fg="green")

            tk.Button(self.session_frame, text="Complete", command=lambda idx=idx: self.complete_session(idx)).grid(row=idx, column=1)
            tk.Button(self.session_frame, text="Delete", command=lambda idx=idx: self.delete_session(idx)).grid(row=idx, column=2)

    def complete_session(self, idx):
        self.sessions[idx]['completed'] = True
        self.save_sessions()
        self.display_sessions()

    def delete_session(self, idx):
        del self.sessions[idx]
        self.save_sessions()
        self.display_sessions()

    def save_sessions(self):
        with open("sessions.json", "w") as f:
            json.dump(self.sessions, f)

    def load_sessions(self):
        if os.path.exists("sessions.json"):
            with open("sessions.json", "r") as f:
                self.sessions = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudyPlanner(root)
    root.mainloop()
