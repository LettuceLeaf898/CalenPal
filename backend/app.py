import sys
import os
import json
import PyPDF2
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from ClientRunner import agent_response
from PDFrunner import agent_rep

app = Flask(__name__, template_folder="../framework", static_folder="../static")
CORS(app)

# -------------------------------
# JSON File Handling
# -------------------------------
EVENTS_FILE = os.path.join(os.path.dirname(__file__), "events.json")


def load_events():
    """Load events from the JSON file."""
    if not os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(EVENTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_events(events):
    """Save events to the JSON file in chronological order."""
    # Sort by datetime before saving
    def event_key(ev):
        try:
            return datetime.strptime(ev["date"] + " " + ev["time"], "%Y-%m-%d %H:%M")
        except Exception:
            return datetime.max

    events = sorted(events, key=event_key)
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=2)
    return events


# Initialize events on startup
events = load_events()

# -------------------------------
# Routes
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/events", methods=["GET"])
def get_events():
    """Return all events."""
    global events
    events = load_events()
    return jsonify(events)


@app.route("/events", methods=["POST"])
def add_event():
    """Add a new event and save to JSON file."""
    global events
    data = request.get_json()

    required_fields = ["date", "time", "title", "description", "stress"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields in event"}), 400

    new_event = {
        "date": data["date"],
        "time": data["time"],
        "title": data["title"],
        "description": data["description"],
        "stress": data["stress"],
    }

    events.append(new_event)
    events = save_events(events)
    return jsonify(new_event), 201


@app.route("/ask-agent", methods=["POST"])
def ask_agent():
    data = request.get_json()
    prompt = data.get("query")
    if not prompt:
        return jsonify({"error": "Missing 'query' in request"}), 400
    response_json = agent_response(prompt)
    print(response_json)
    return jsonify(response_json), 201


@app.route("/upload-syllabus", methods=["POST"])
def upload_syllabus():
    """Upload syllabus PDF and save to uploads folder (AI processing later)."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = secure_filename(file.filename)
        uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        save_path = os.path.join(uploads_dir, filename)
        print("Saving file to:", save_path)
        file.save(save_path)
        response = agent_rep(save_path)
        print(response)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)

