import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from Client_agent.agent import get_agent_response

app = Flask(__name__, template_folder="../frontend", static_folder="/static")
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
    response_json = get_agent_response(prompt)
    print("Agent response:", response_json)

    return response_json, 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    