from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

quotes = []
with open('quotes.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        quotes.append(line)

def fetch_quote():
    import random
    return random.choice(quotes)

# Command definitions
COMMANDS = {
    "help": {
        "description": "Show this help message",
        "response": {
            "type": "text",
            "content": """Available commands:
help --------- Show this help message
about -------- Who I am and what I do
reveal-face -- If you wanna see me!
projects ----- My featured projects
contact ------ How to reach me
clear -------- Clear the terminal
joke --------- Get a tech joke
resume ------- View/download my resume
skills ------- My technical skills matrix
secret ------- 🤫 Try and see
motivate ----- Get a motivational quote
asciiart ----- Show cool ASCII art
weather  ----- Check local weather (simulated)
""",
        }
    },
    "about": {
        "description": "Show information about me",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "## About Me\nFull-stack developer, Linux enthusiast, and problem solver."},
                {"type": "text", "content": "### Skills:\n- Python\n- HTML+CSS+JS\n- Linux Server management\n- CI/CD\n- Web scrapping & automations\n"}
            ]
        }
    },
    "reveal-face": {
        "description": "Show picture of me",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "image", "url": "/static/images/founder.jpg", "alt": "My Photo"}
            ]
        }
    },
    "projects": {
        "description": "Show my projects",
        "response": {
            "type": "gallery",
            "content": [
                {
                    "title": "Prescribemate",
                    "description": "Healthcare SaaS platform with AI integration",
                    "image": "/static/images/prescribemate.jpg",
                    "link": "https://prescribemate.com/"
                },
                {
                    "title": "Kamrul Academy",
                    "description": "Educational platform with 10,000+ students",
                    "image": "/static/images/ka.jpg",
                    "link": "https://kamrulacademy.com/"
                }
            ]
        }
    },
    "contact": {
        "description": "Show contact information",
        "response": {
            "type": "links",
            "content": [
                {"text": "📧 Email", "url": "mailto:tanvirsaklan3660@gmail.com"},
                {"text": "💼 LinkedIn", "url": "https://www.linkedin.com/in/uch105/"},
                {"text": "🐙 GitHub", "url": "https://github.com/uch105"},
                {"text": "💬 WhatsApp", "url": "https://wa.me/+8801635817747"},
            ]
        }
    },
    "joke": {
        "description": "Random fun fact about me",
        "response": {
            "type": "text",
            "content": """
- Why are mountains so funny? They’re hill areas.
- I tried to catch fog yesterday. Mist.
- Two bytes meet. The first byte asks, “Are you ill?” The second byte replies, “No, just feeling a bit off.”
- How do robots eat pizza? One byte at a time.
- How did the first program die? It was executed.
- Why do programmers always mix up Halloween and Christmas? Because Oct 31 equals Dec 25.
- My resume says you take things too literally. When the hell did my resume learn to talk?
- Why do submarines and spaceships all run Linux? Because you can't open windows there.
"""
        }
    },
    "resume": {
        "description": "View/download my resume",
        "response": {
            "type": "links",
            "content": [
                {"text": "📄 View Resume (PDF)", "url": "/static/docs/resume.pdf"},
                {"text": "⬇️ Download Resume", "url": "/static/docs/resume.pdf", "download": True}
            ]
        }
    },
    "skills": {
        "description": "My technical skills matrix",
        "response": {
            "type": "text",
            "content": """My skills (self-assessed):

Python 🐍 : ██████████ 100%
Web Scrapping : ██████████ 100%
Automation : ██████████ 100%
AI : ██████████ 100%
Linux   : ██████████ 100%
JavaScript : █████████░ 90%
HTML+CSS : █████████░ 90%
Nginx  : █████████░ 80%
Postgresql     : ████████░░ 80%
Docker   : ███████░░░ 70%
Pentesting : ███████░░░ 70%
"""
        }
    },
    "secret": {
        "description": "🤫 Try and see",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "Wanna know my secrets? 🎉"},
                {"type": "text", "content": "Here are some secrets just for you:"},
                {"type": "text", "content": """
                (•_•)
                I may look happy, but deep down, i need money. Only money can fix me.
                """},
                {"type": "text", "content": """
                (•_•)
                I love faluda, egg-fry, custard, sweets a lot.
                """}
            ]
        }
    },
    "motivate": {
        "description": "Get a motivational quote",
        "execute": lambda: {
            "type": "text",
            "content": fetch_quote()
        }
    },
    "asciiart": {
        "description": "Show cool ASCII art",
        "response": {
            "type": "text",
            "content": """
            Here's some ASCII art for you:

            ( ͡° ͜ʖ ͡°) uch approves your visit!
            """
        }
    },
    "weather": {
        "description": "Check local weather (simulated)",
        "response": {
            "type": "text",
            "content": """Current weather in Developerland:
☀️  Sunny with a chance of bugs
🌡️  72°F (22°C)
💨  Light git pushes at 5 mph
☕  Coffee index: High

Weather forecast:
Tomorrow: 🌧️  Rain of new features
Weekend:  🚀  Perfect for side projects
"""
        }
    },
    "clear": {
        "description": "Clear the terminal",
        "response": {
            "type": "clear"
        }
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.get_json()
    command = data.get('command', '').strip().lower()
    
    if command == "clear":
        return jsonify({"type": "clear"})
    
    if command in COMMANDS:
        if callable(COMMANDS[command].get("execute")):
            return jsonify(COMMANDS[command]["execute"]())
        return jsonify(COMMANDS[command]["response"])
    
    return jsonify({
        "type": "error",
        "content": f"Command not found: {command}. Type 'help' for available commands."
    })

if __name__ == '__main__':
    app.run(debug=True)
