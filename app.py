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
education ---- Where i studied, my grades etc.
research ----- My research works during graduation.
projects ----- My featured projects
contact ------ How to reach me
clear -------- Clear the terminal
joke --------- Get a tech joke
resume ------- View/download my resume
skills ------- My technical skills matrix
hobby -------- Who knows, we may have things in common!
achievement -- Ah! My glorious days.
secret ------- 🤫 Try and see
motivate ----- Get a motivational quote
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
                {"type": "text", "content": "### Details:\nHi there, I am a passionate STEM engineer who loves to work in both hardware and software divisions. With a view to sustainable green solution, I aim to integrate hardware and software for better optimization. My academic background provided me a solid knowledge about materials and various tools. I have done several nano-particle synthesis and characterization processes during my academics. On the other hand, my passion took me to the path of programming. I have crawled from design to code via a Cybersecurity path. Through which I have learned Web Development, Automation, Artificial Intelligence, and Cybersecurity.\n"}
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
    "education": {
        "description": "Show educational info",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "## Current status (B.Sc Graduate)"},
                {"type": "text", "content": "### School:\nGorai High School\nTangail, Bangladesh.\nPassing Year: 2015\nGPA: 5.00/5.00\n\n"},
                {"type": "text", "content": "### School:\nSt. Joseph Higher Secondary School\nDhaka, Bangladesh.\nPassing Year: 2017\nGPA: 5.00/5.00\n\n"},
                {"type": "text", "content": "### University:\nB.Sc in Enginerring\nDepartment of Materials Science & Engineering\nUniversity of Rajshahi\nRajshahi, Bangladesh.\nPassing Year: 2024\nCGPA: 3.28\n\n"}
            ]
        }
    },
    "research": {
        "description": "Show my research experiences",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "### Eco Friendly Nano-Particle Synthesis using Food Waste\nTitle : Green Synthesis & Characterization of Ferrimagnetic Nickel Ferrite Nanoparticles Using Seed Extract of Phoenix Dactylifera for Biomedical Applications\nContribution: Expected ferrimagnetic NPs with good particle size and magnetic properties was achieved through several low temperature operations (less than 650℃ ). A formal presentation was presented before the board of faculties on this research.\n\n"},
                {"type": "text", "content": "### Honey Synthesized Maghemite Nanoparticles for Hyperthermia Cancer Treatment\nTitle : Lychee Honey-Mediated Green Synthesis of Maghemite Nanoparticles for Potential Application in Cancer Hyperthermia Therapy.\nContribution: Provided assistantship to my lab-mate to complete his project. Used FESEM & other techniques to characterize which aligns with structural analysis and sustainable material synthesis theme.\n"},
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
                {"text": "📄 View Resume (PDF)", "url": "/static/docs/cv.pdf"},
                {"text": "⬇️ Download Resume", "url": "/static/docs/cv.pdf", "download": True}
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
    "hobby": {
        "description": "Lets know some interests",
        "response": {
            "type": "text",
            "content": """
            🧳 Travelling
            🏀 Basketball
            🚲 Cycling
            🚶‍♂️‍➡️ Hiking
            📚 Reading books
            🥷 Combat trainings
            🚙 Long drive
            🌱 Gardening
            """
        }
    },
    "achievement": {
        "description": "Oh! My glorious days.",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "Champion at Bangladesh Inter-University Basketball Tournament -2024\n\n"},
                {"type": "text", "content": "Champion at Bangladesh Inter-University Basketball Tournament -2023"},
            ]
        }
    },
    "secret": {
        "description": "🤫 Try and see",
        "response": {
            "type": "mixed",
            "content": [
                {"type": "text", "content": "Wanna know my secrets? 🎉"},
                {"type": "text", "content": "Here are some secrets just for you:"},
                {"type": "text", "content": "I may look happy, but deep down, i need money. Only money can fix me."},
                {"type": "text", "content": "I love faluda, egg-fry, custard, sweets a lot."}
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
    "weather": {
        "description": "Check local weather (simulated)",
        "response": {
            "type": "text",
            "content": "Current weather in Developerland:\n ☀️ Sunny with a chance of bugs\n 🌡️ 72°F (22°C)\n 💨 Light git pushes at 5 mph\n ☕ Coffee index: High\n\n Weather forecast:\n Tomorrow: 🌧️ Rain of new features\n Weekend: 🚀 Perfect for side projects"
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
