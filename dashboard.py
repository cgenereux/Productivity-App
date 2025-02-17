from flask import Flask, render_template, jsonify
import json, os, datetime, random

# Define file paths relative to this script’s location
ACTUAL_DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')
SYNTHETIC_DATA_FILE = os.path.join(os.path.dirname(__file__), 'synthetic_data.json')

# Toggle this flag:
USE_SYNTHETIC_DATA = True  # Set to True to use synthetic data for visualization purposes 

app = Flask(__name__)

def generate_synthetic_data():
    """Generate synthetic data for the past 30 days."""
    data = []
    today = datetime.date.today()
    for i in range(30):
        day = today - datetime.timedelta(days=i)
        entry = {
            "date": day.isoformat(),
            "morning_routine": random.choice([True, False]),
            "wakeup_time": f"{random.uniform(5,9):.1f}",
            "sleep_hours": f"{random.uniform(6,9):.1f}",
            "healthy_eat": str(random.randint(1,10)),
            "running": random.choice([True, False]),
            "exercise_minutes": str(random.randint(0,60)),
            "homework_minutes": str(random.randint(0,120)),
            "productivity": str(random.randint(1,10)),
            "mood": str(random.randint(1,10)),
            "valuable": "Synthetic activity data.",
            "regret": "Synthetic regret.",
            "realization": "Synthetic realization."
        }
        data.append(entry)
    return data

def load_data():
    if USE_SYNTHETIC_DATA:
        # Try to load synthetic data from file; if not available, generate and save it.
        if os.path.exists(SYNTHETIC_DATA_FILE):
            with open(SYNTHETIC_DATA_FILE, 'r') as f:
                try:
                    return json.load(f)
                except Exception:
                    synthetic = generate_synthetic_data()
                    with open(SYNTHETIC_DATA_FILE, 'w') as wf:
                        json.dump(synthetic, wf, indent=4)
                    return synthetic
        else:
            synthetic = generate_synthetic_data()
            with open(SYNTHETIC_DATA_FILE, 'w') as f:
                json.dump(synthetic, f, indent=4)
            return synthetic
    else:
        # Use actual data from file; if file doesn't exist or fails, return empty list.
        if os.path.exists(ACTUAL_DATA_FILE):
            with open(ACTUAL_DATA_FILE, 'r') as f:
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

def save_data(data):
    # Save only actual data when synthetic mode is off.
    if not USE_SYNTHETIC_DATA:
        with open(ACTUAL_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('dashboard.html', data=data)

@app.route('/data')
def data():
    return jsonify(load_data())

if __name__ == '__main__':
    app.run(debug=True)