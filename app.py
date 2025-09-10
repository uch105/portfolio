from flask import Flask, render_template, request, jsonify, send_from_directory
import json, subprocess

app = Flask(__name__)

# Load knowledge base
with open("knowledge.json", "r") as f:
    knowledge = json.load(f)

MODEL_NAME = "uchbot"

def query_knowledge_base(user_input):
    """Simple RAG: check if any key matches inside user input"""
    for key, answer in knowledge.items():
        if key.lower() in user_input.lower():
            return answer
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # 1. Try knowledge base (RAG)
    rag_response = query_knowledge_base(user_input)
    if rag_response:
        return jsonify({"reply": rag_response})

    # 2. Fallback to ollama system call
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, user_input],
            capture_output=True,
            text=True
        )
        return jsonify({"reply": result.stdout.strip()})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {e}"})

@app.route("/download_cv")
def download_cv():
    return send_from_directory("static", "cv.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
