import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from Client_agent.agent import get_agent_response

app = Flask(__name__, template_folder="../frontend")
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
    #data = request.get_json()
    #prompt = data.get("input")

    #response_json = get_agent_response(prompt)
   # return jsonify(response_json), 201
   return{"testing": "testing"}

if __name__ == "__main__":
    app.run(debug=True, port=5000)

    