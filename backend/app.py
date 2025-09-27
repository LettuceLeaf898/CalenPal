from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="../frontend")

items = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    new_item = request.get_json()
    items.append(new_item)
    return jsonify({"message": "Item added", "items": items}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)