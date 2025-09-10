from flask import Flask, render_template, request, jsonify, send_from_directory
import json, subprocess, os
from datetime import datetime

app = Flask(__name__)

# Load knowledge base
with open("knowledge.json", "r") as f:
    knowledge = json.load(f)

MODEL_NAME = "uchbot"
LOG_DIR = "logs"

# Ensure logs folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_message(ip, user_input, reply):
    """Log IP, timestamp, user input, and bot reply into daily file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIR, f"{today}.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] IP: {ip} | User: {user_input} | Bot: {reply}\n")

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

    # capture client IP
    user_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    # 1. Try knowledge base (RAG)
    rag_response = query_knowledge_base(user_input)
    if rag_response:
        log_message(user_ip, user_input, rag_response)
        return jsonify({"reply": rag_response})

    # 2. Fallback to ollama system call
    try:
        result = subprocess.run(
            ["/usr/local/bin/ollama", "run", MODEL_NAME, user_input],
            capture_output=True,
            text=True
        )
        reply = result.stdout.strip()
        log_message(user_ip, user_input, reply)
        return jsonify({"reply": reply})
    except Exception as e:
        error_msg = f"⚠️ Error: {e}"
        log_message(user_ip, user_input, error_msg)
        return jsonify({"reply": error_msg})

@app.route("/download_cv")
def download_cv():
    return send_from_directory("static", "cv.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

