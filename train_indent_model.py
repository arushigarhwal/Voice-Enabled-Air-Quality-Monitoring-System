from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# (A) Training data (samples + intents)
samples = [
    ("show me the current reading", "get_current"),
    ("what’s the air quality now", "get_current"),
    ("give me the latest sensor value", "get_current"),

    ("show last 10 readings", "get_last_10"),
    ("tell me the last 10 entries", "get_last_10"),

    ("draw a graph for last week", "draw_graph"),
    ("plot values from monday to friday", "draw_graph"),

    ("show readings for today", "get_by_day"),
    ("give me data from June 25th", "get_by_day"),

    ("exit the app", "exit"),
    ("quit", "exit"),

    ("when was the air quality bad", "show_bad_days"),
    ("show me high pollution days", "show_bad_days"),

    ("what is the air quality right now", "get_quality_label"),
    ("is the quality high or low", "get_quality_label"),

    ("exit the app", "exit"),
    ("quit", "exit"),

    ("show good air quality days", "good_days"),
    ("list clean air days", "good_days"),

    ("turn off the sensor", "sensor_off"),
    ("switch on sensor", "sensor_on"),

]

texts = [s[0] for s in samples]
labels = [s[1] for s in samples]

# (B) Vectorizer + classifier
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

# (C) Save model and vectorizer
joblib.dump(model, "intent_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Trained and saved intent model.")
