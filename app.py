from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    title = (data.get("title") or "").lower()
    description = (data.get("description") or "").lower()
    text = f"{title} {description}"

    keywords = [
        "relocation", "relocates", "move", "moving", "new office",
        "headquarters", "hq", "lease signed"
    ]
    match = any(k in text for k in keywords)

    return jsonify({"isRelevant": match})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

