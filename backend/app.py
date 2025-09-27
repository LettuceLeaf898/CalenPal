from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from Client_agent.agent import root_agent

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
    data = request.get_json()
    Fdata = data.get("input")
    agent_response=my_agent.run(Fdata)
    return jsonify(agent_response), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)