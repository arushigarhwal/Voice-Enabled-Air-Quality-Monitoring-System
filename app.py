# from flask import Flask, render_template, jsonify, redirect, url_for
# import matplotlib.pyplot as plt
# import sqlite3
# import os
# import queue
# import sounddevice as sd
# import json
# from vosk import Model, KaldiRecognizer
# import joblib
#
# # Load ML model and vectorizer
# intent_model = joblib.load("intent_model.pkl")
# vectorizer = joblib.load("vectorizer.pkl")
#
# # Load VOSK model
# vosk_model = Model("vosk-model-small-en-us-0.15")
#
# # Constants
# DATA_FILE = "gas_data.db"
# sensor_status = {"is_on": True}
#
# # App setup
# app = Flask(__name__)
#
#
# # Intent extraction function
# def extract_intent(text):
#     X = vectorizer.transform([text])
#     return intent_model.predict(X)[0]
#
#
# @app.route("/")
# def home():
#     return render_template("index.html")
#
#
# @app.route("/start-voice")
# def start_voice():
#     q = queue.Queue()
#
#     def callback(indata, frames, time, status):
#         q.put(bytes(indata))
#
#     with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
#         recognizer = KaldiRecognizer(vosk_model, 16000)
#         print("🎤 Listening...")
#
#         while True:
#             data = q.get()
#             if recognizer.AcceptWaveform(data):
#                 result = json.loads(recognizer.Result())
#                 text = result.get("text", "")
#                 if text.strip():
#                     break
#
#     intent = extract_intent(text)
#     print(f"🧠 Intent Detected: {intent}")
#
#     # Rerouting logic
#     if intent == "get_current":
#         return redirect(url_for("quality"))
#     elif intent == "get_last_10":
#         return redirect(url_for("last_10"))
#     elif intent == "draw_graph":
#         return redirect(url_for("graph"))
#     elif intent == "get_by_day":
#         return redirect(url_for("by_day", date="2025-06-28"))  # Can be made dynamic
#     elif intent == "show_bad_days":
#         return redirect(url_for("bad_days"))
#     elif intent == "good_days":
#         return redirect(url_for("good_days"))
#     elif intent == "sensor_off":
#         return redirect(url_for("sensor_off"))
#     elif intent == "sensor_on":
#         return redirect(url_for("sensor_on"))
#     elif intent == "exit":
#         return "👋 Goodbye! Exiting (dummy route)", 200
#     elif intent == "get_quality_label":
#         return redirect(url_for("quality"))
#     else:
#         return jsonify({
#             "text": text,
#             "intent": intent,
#             "response": "❓ Unknown command"
#         })
#
#
# @app.route("/sensor/on")
# def sensor_on():
#     sensor_status["is_on"] = True
#     return jsonify({"status": "Sensor turned ON"})
#
#
# @app.route("/sensor/off")
# def sensor_off():
#     sensor_status["is_on"] = False
#     return jsonify({"status": "Sensor turned OFF"})
#
#
# @app.route("/sensor/status")
# def sensor_state():
#     return jsonify({"sensor_status": "ON" if sensor_status["is_on"] else "OFF"})
#
#
# @app.route("/last-10")
# def last_10():
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT timestamp, value FROM gas_reading ORDER BY timestamp DESC LIMIT 10")
#     rows = cursor.fetchall()
#     conn.close()
#     readings = [{"timestamp": r[0], "value": r[1]} for r in rows]
#     return render_template("last_10.html", readings=readings)
#
#
# @app.route("/graph")
# def graph():
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT timestamp, value FROM gas_reading ORDER BY timestamp DESC LIMIT 50")
#     data = cursor.fetchall()
#     conn.close()
#
#     timestamps = [r[0] for r in reversed(data)]
#     values = [r[1] for r in reversed(data)]
#
#     plt.figure(figsize=(8, 4))
#     plt.plot(timestamps, values, marker='o')
#     plt.title("Recent Air Quality Readings")
#     plt.xlabel("Time")
#     plt.xticks(rotation=45)
#     plt.ylabel("Value")
#     plt.tight_layout()
#
#     path = os.path.join("static", "graph.png")
#     plt.savefig(path)
#     plt.close()
#     return render_template("graph.html", graph_url="/static/graph.png")
#
#
# @app.route("/day/<date>")
# def by_day(date):
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT timestamp, value FROM gas_reading WHERE date(timestamp) = ?", (date,))
#     rows = cursor.fetchall()
#     conn.close()
#     readings = [{"timestamp": r[0], "value": r[1]} for r in rows]
#     return render_template("day_view.html", readings=readings, date=date)
#
#
# @app.route("/bad-days")
# def bad_days():
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT DATE(timestamp) as day, COUNT(*)
#         FROM gas_reading
#         WHERE value > 3000
#         GROUP BY day
#     """)
#     results = cursor.fetchall()
#     conn.close()
#     days = [{"timestamp": row[0], "count": row[1]} for row in results]
#     return render_template("bad_days.html", days=days)
#
#
# @app.route("/good-days")
# def good_days():
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT DATE(timestamp) as day, COUNT(*)
#         FROM gas_reading
#         WHERE value < 500
#         GROUP BY day
#     """)
#     results = cursor.fetchall()
#     conn.close()
#     days = [{"timestamp": row[0], "count": row[1]} for row in results]
#     return render_template("good_days.html", days=days)
#
#
# @app.route("/quality")
# def quality():
#     conn = sqlite3.connect(DATA_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT value FROM gas_reading ORDER BY timestamp DESC LIMIT 1")
#     result = cursor.fetchone()
#     conn.close()
#
#     value = result[0] if result else 0
#
#     if value > 3000:
#         status = "High"
#     elif value > 1500:
#         status = "Moderate"
#     else:
#         status = "Low"
#
#     return render_template("quality_status.html", value=value, status=status)
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, jsonify, redirect, url_for, request
import matplotlib.pyplot as plt
import sqlite3
import os
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import joblib
from datetime import datetime

# === Constants ===
DB_FILE = "gas_data.db"
VOSK_PATH = "vosk-model-small-en-us-0.15"
intent_model = joblib.load("intent_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
vosk_model = Model(VOSK_PATH)
sensor_status = {"is_on": True}

# === Flask App ===
app = Flask(__name__)

# === DB Initialization ===
def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gas_reading (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def insert_gas_value(value):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO gas_reading (value) VALUES (?)', (value,))
        conn.commit()

def get_latest_value():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM gas_reading ORDER BY timestamp DESC LIMIT 1')
        result = cursor.fetchone()
        return result[0] if result else "N/A"

# === Intent Detection ===
def extract_intent(text):
    X = vectorizer.transform([text])
    return intent_model.predict(X)[0]

# === Routes ===
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json()
    if data and "gas_value" in data:
        insert_gas_value(data["gas_value"])
        return jsonify({"status": "saved", "value": data["gas_value"]})
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route("/latest")
def latest():
    value = get_latest_value()
    return jsonify({"gas_value": value})

# @app.route("/sensor/on")
# def sensor_on():
#     sensor_status["is_on"] = True
#     return jsonify({"status": "Sensor turned ON"})
#
# @app.route("/sensor/off")
# def sensor_off():
#     sensor_status["is_on"] = False
#     return jsonify({"status": "Sensor turned OFF"})
#
# @app.route("/sensor/status")
# def sensor_state():
#     return jsonify({"sensor_status": "ON" if sensor_status["is_on"] else "OFF"})

@app.route("/start-voice")
def start_voice():
    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
        recognizer = KaldiRecognizer(vosk_model, 16000)
        print("🎤 Listening for command...")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text.strip():
                    print("🗣️ You said:", text)
                    break

    intent = extract_intent(text)
    print("🧠 Detected Intent:", intent)

    # Route based on intent
    if intent == "get_current":
        return redirect(url_for("quality"))
    elif intent == "get_last_10":
        return redirect(url_for("last_10"))
    elif intent == "draw_graph":
        return redirect(url_for("graph"))
    elif intent == "get_by_day":
        return redirect(url_for("by_day", date=str(datetime.today().date())))
    elif intent == "show_bad_days":
        return redirect(url_for("bad_days"))
    elif intent == "good_days":
        return redirect(url_for("good_days"))
    elif intent == "sensor_off":
        return redirect(url_for("sensor_off"))
    elif intent == "sensor_on":
        return redirect(url_for("sensor_on"))
    elif intent == "exit":
        return "👋 Goodbye!", 200
    else:
        return jsonify({"text": text, "intent": intent, "response": "❓ Unknown command"})

@app.route("/last-10")
def last_10():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, value FROM gas_reading ORDER BY timestamp DESC LIMIT 10")
        rows = cursor.fetchall()
    readings = [{"timestamp": r[0], "value": r[1]} for r in rows]
    return render_template("last_10.html", readings=readings)

@app.route("/graph")
def graph():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, value FROM gas_reading ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()

    timestamps = [r[0] for r in reversed(rows)]
    values = [r[1] for r in reversed(rows)]

    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, values, marker='o')
    plt.title("Recent Air Quality Readings")
    plt.xlabel("Time")
    plt.xticks(rotation=45)
    plt.ylabel("Value")
    plt.tight_layout()

    graph_path = os.path.join("static", "graph.png")
    plt.savefig(graph_path)
    plt.close()

    return render_template("graph.html", graph_url="/static/graph.png")

@app.route("/day/<date>")
def by_day(date):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, value FROM gas_reading WHERE date(timestamp) = ?", (date,))
        rows = cursor.fetchall()
    readings = [{"timestamp": r[0], "value": r[1]} for r in rows]
    return render_template("day_view.html", readings=readings, date=date)

@app.route("/bad-days")
def bad_days():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(timestamp), COUNT(*) 
            FROM gas_reading 
            WHERE value > 3000 
            GROUP BY DATE(timestamp)
        """)
        rows = cursor.fetchall()
    days = [{"timestamp": r[0], "count": r[1]} for r in rows]
    return render_template("bad_days.html", days=days)

@app.route("/good-days")
def good_days():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(timestamp), COUNT(*) 
            FROM gas_reading 
            WHERE value < 500 
            GROUP BY DATE(timestamp)
        """)
        rows = cursor.fetchall()
    days = [{"timestamp": r[0], "count": r[1]} for r in rows]
    return render_template("good_days.html", days=days)

@app.route("/quality")
def quality():
    value = get_latest_value()
    if value == "N/A":
        status = "No data"
    elif value > 3000:
        status = "High"
    elif value > 1500:
        status = "Moderate"
    else:
        status = "Low"
    return render_template("quality_status.html", value=value, status=status)

# === Run App ===
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
