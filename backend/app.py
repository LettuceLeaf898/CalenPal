import sys
import os
import json
import PyPDF2
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from ClientRunner import agent_response

app = Flask(__name__, template_folder="../framework", static_folder="../static")
CORS(app)

items = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

@app.route("/ask-agent", methods=["POST"])
def ask_agent():
    data = request.get_json()
    print("Received data:", data)

    # Extract the user's message
    prompt = data.get("query")  # frontend sends {"query": "..."}
    if not prompt:
        return jsonify({"error": "Missing 'query' in request"}), 400
    print("User prompt:", prompt)
    response_json = agent_response(prompt)

    return jsonify(response_json), 201

EVENTS_FILE = "events.json"

@app.route("/upload-syllabus", methods=["POST"])
def upload_syllabus():
    print("Upload syllabus endpoint hit")

    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({"error": "No file part in request"}), 400

    file = request.files.get('file')
    if not file or file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400

    # Save uploaded file
    try:
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        uploads_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        save_path = os.path.join(uploads_dir, filename)
        file.save(save_path)
        print(f"Saved uploaded syllabus to: {save_path}")
        return jsonify({"filename": filename, "saved_to": save_path}), 201
    except Exception as e:
        print("Error saving uploaded file:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)


# JSON 
