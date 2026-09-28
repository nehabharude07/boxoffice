import json
import pickle
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE = Path(__file__).parent
app = Flask(__name__)

model = pickle.load(open(BASE / "model.pkl", "rb"))
scaler = pickle.load(open(BASE / "scaler.pkl", "rb"))

# metrics.json is written by train_model.py (held-out accuracy, typical error, sample values)
try:
    metrics = json.load(open(BASE / "metrics.json"))
except FileNotFoundError:
    metrics = {}

# Same order the model was trained on (after title_length)
FIELDS = {
    "budget": ("Budget", 1e5, 1e9),
    "opening_theaters": ("Opening theaters", 1, 10_000),
    "opening_revenue": ("Opening revenue", 0, 1e9),
    "release_days": ("Days in theaters", 1, 365),
    "domestic_revenue": ("Domestic revenue", 0, 2e9),
}


@app.get("/")
def index():
    return render_template("index.html", metrics=metrics)


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title or len(title) > 80:
        return jsonify(error="Enter a title of up to 80 characters.", field="title"), 400

    values = {}
    for key, (label, lo, hi) in FIELDS.items():
        try:
            v = float(data[key])
        except (KeyError, TypeError, ValueError):
            return jsonify(error=f"{label} must be a number.", field=key), 400
        if not lo <= v <= hi:
            return jsonify(error=f"{label} must be between {lo:,.0f} and {hi:,.0f}.", field=key), 400
        values[key] = v

    features = [[len(title), *values.values()]]
    pred = max(0.0, float(model.predict(scaler.transform(features))[0]))  # float32 -> float for JSON

    mae = metrics.get("mae", 0)
    low = max(0.0, pred + metrics.get("p10", -mae))
    high = pred + metrics.get("p90", mae)
    profit = pred - values["budget"]

    return jsonify(
        title=title,
        prediction=pred,
        low=low,
        high=high,
        profit=profit,
        multiple=pred / values["budget"],
    )


if __name__ == "__main__":
    app.run(debug=True, port=5162)
