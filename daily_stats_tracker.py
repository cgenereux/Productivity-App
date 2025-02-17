import tkinter as tk
import json, os, datetime, random

DATA_FILE = 'data.json'
SNOOZE_MINUTES = 120  # 2 hours snooze interval

QUOTES = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Life is what happens when you're busy making other plans. - John Lennon",
    "The unexamined life is not worth living. - Socrates",
    "Do not take life too seriously. - Elbert Hubbard",
    "Your time is limited, don't waste it living someone else's life. - Steve Jobs"
]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_custom_date():
    """
    Returns the date for which data is recorded, based on an 8pm-to-8pm day.
    If current time is before 8pm, the entry is attributed to the previous day.
    """
    now = datetime.datetime.now()
    if now.hour < 20:
        day = now.date() - datetime.timedelta(days=1)
    else:
        day = now.date()
    return day.isoformat()

def ordinal(n):
    """Return ordinal string for integer n (e.g., 1 -> '1st')."""
    if 11 <= n % 100 <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def get_day_message():
    """
    Returns a message indicating which day is being recorded,
    formatted as "Today: February 7th" or "Yesterday: February 6th".
    """
    now = datetime.datetime.now()
    if now.hour < 20:
        rec_date = now.date() - datetime.timedelta(days=1)
        label = "Yesterday"
    else:
        rec_date = now.date()
        label = "Today"
    formatted_date = rec_date.strftime("%B ") + ordinal(rec_date.day)
    return f"{label}: {formatted_date}"

def append_entry(entry):
    data = load_data()
    # Remove any existing entry for the same day.
    data = [e for e in data if e.get('date') != entry.get('date')]
    data.append(entry)
    save_data(data)

def get_random_quote():
    return random.choice(QUOTES)

class SurveyWindow(tk.Toplevel):
    def __init__(self, master, submit_callback, snooze_callback):
        super().__init__(master)
        self.submit_callback = submit_callback
        self.snooze_callback = snooze_callback
        self.title("Daily Stats Survey")
        self.create_widgets()
    
    def create_widgets(self):
        # Display the inspirational quote.
        quote = get_random_quote()
        tk.Label(self, text=quote, wraplength=400).pack(pady=5)
        # Display which day is being recorded.
        tk.Label(self, text=get_day_message(), font=("Arial", 10, "italic")).pack(pady=5)
        
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)
        
        # Standard single-line inputs
        self.var_morning_routine = tk.IntVar()
        self.var_wakeup_time = tk.StringVar()
        self.var_sleep_hours = tk.StringVar()
        self.var_healthy_eat = tk.StringVar()
        self.var_running = tk.IntVar()
        self.var_exercise_minutes = tk.StringVar()
        self.var_homework_minutes = tk.StringVar()
        self.var_productivity = tk.StringVar()
        self.var_mood = tk.StringVar()

        row = 0
        tk.Label(frame, text="Did you do your morning routine first thing?").grid(row=row, column=0, sticky="w")
        tk.Checkbutton(frame, variable=self.var_morning_routine, onvalue=1, offvalue=0).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="What time did you wake up? (e.g., 13.5 for 1:30pm)").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_wakeup_time).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How many hours of sleep did you get?").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_sleep_hours).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How healthy did you eat? (1-10)").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_healthy_eat).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="Did you go running?").grid(row=row, column=0, sticky="w")
        tk.Checkbutton(frame, variable=self.var_running, onvalue=1, offvalue=0).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How many minutes did you exercise?").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_exercise_minutes).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How many minutes of homework did you do?").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_homework_minutes).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How productive was your day? (1-10)").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_productivity).grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="How was your mood today? (1-10)").grid(row=row, column=0, sticky="w")
        tk.Entry(frame, textvariable=self.var_mood).grid(row=row, column=1, sticky="w")
        row += 1
        
        # Multi-line text boxes for reflections:
        tk.Label(frame, text="What valuable stuff did you do today?").grid(row=row, column=0, sticky="w")
        self.txt_valuable = tk.Text(frame, height=2, width=40)
        self.txt_valuable.grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="What could you have done today that you regret not doing?").grid(row=row, column=0, sticky="w")
        self.txt_regret = tk.Text(frame, height=2, width=40)
        self.txt_regret.grid(row=row, column=1, sticky="w")
        row += 1

        tk.Label(frame, text="What's one thought/realization you had today?").grid(row=row, column=0, sticky="w")
        self.txt_realization = tk.Text(frame, height=2, width=40)
        self.txt_realization.grid(row=row, column=1, sticky="w")
        row += 1

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Submit", command=self.submit).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Snooze", command=self.snooze).pack(side="left", padx=5)

    def submit(self):
        # Only when submit is clicked, update the data.
        entry = {
            "date": get_custom_date(),
            "morning_routine": bool(self.var_morning_routine.get()),
            "wakeup_time": self.var_wakeup_time.get(),
            "sleep_hours": self.var_sleep_hours.get(),
            "healthy_eat": self.var_healthy_eat.get(),
            "running": bool(self.var_running.get()),
            "exercise_minutes": self.var_exercise_minutes.get(),
            "homework_minutes": self.var_homework_minutes.get(),
            "productivity": self.var_productivity.get(),
            "mood": self.var_mood.get(),
            "valuable": self.txt_valuable.get("1.0", tk.END).strip(),
            "regret": self.txt_regret.get("1.0", tk.END).strip(),
            "realization": self.txt_realization.get("1.0", tk.END).strip()
        }
        append_entry(entry)
        self.submit_callback()
        self.destroy()

    def snooze(self):
        self.snooze_callback()
        self.destroy()

def has_entry_for_today(data):
    today = get_custom_date()
    return any(entry.get('date') == today for entry in data)

def main():
    data = load_data()
    if has_entry_for_today(data):
        print("Quiz already submitted for today. Exiting.")
        return  # Exit if today's quiz already exists

    root = tk.Tk()
    root.withdraw()

    def show_survey():
        SurveyWindow(root, on_submit, on_snooze)

    def on_submit():
        root.destroy()

    def on_snooze():
        root.after(SNOOZE_MINUTES * 60000, show_survey)

    show_survey()
    root.mainloop()

if __name__ == '__main__':
    main()