from flask import Flask, render_template_string, request
import os
import socket
import requests

app = Flask(__name__)

LEVEL_HINTS = {
    "level1": "✅ Level 1 complete: Port is exposed correctly!",
    "level2": "✅ Level 2 complete: SECRET_KEY detected!",
    "level3": "✅ Level 3 complete: GOAL.txt file found with correct contents!",
    "level4": "✅ Level 4 complete: API service reachable!",
    "level5": "✅ Level 5 complete: Game service reachable!",
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Docker Escape Room</title>
    <style>
        body { font-family: sans-serif; padding: 20px; background: #f9f9f9; }
        .level { margin-bottom: 1.5em; padding: 1em; background: white; border: 1px solid #ddd; border-radius: 8px; }
        .pass { color: green; }
        .fail { color: red; }
        .hint { display: none; margin-top: 10px; color: #444; background: #eef; padding: 10px; border-left: 4px solid #88f; }
    </style>
    <script>
        function toggleHint(id, btn) {
            const hint = document.getElementById(id);
            const isVisible = hint.style.display === 'block';
            hint.style.display = isVisible ? 'none' : 'block';
            btn.innerText = isVisible ? 'Show Hint' : 'Hide Hint';
        }
    </script>
</head>
<body>
    <h1>Docker Escape Room 🐳</h1>

    <div class="level">
    <h2>Level 1: Broken Webserver</h2>
    <p class="{{ 'pass' if level1 else 'fail' }}">{{ level1_msg }}</p>
    {% if level1 %}
        <div class="hint" style="display: block; margin-top: 10px;">
            🧩 Clue to next level: <code>Fusion-the-goats</code>
        </div>
    {% else %}
        <button onclick="toggleHint('hint1', this)">Show Hint</button>
        <div class="hint" id="hint1">
            💡 Try running the container with <code>-p 8080:80</code> to expose the correct port.
        </div>
    {% endif %}
</div>

{% if level1 %}
<div class="level">
    <h2>Level 2: Environment Variable Secret</h2>
    <p class="{{ 'pass' if level2 else 'fail' }}">{{ level2_msg }}</p>
    {% if level2 %}
        <div class="hint" style="display: block; margin-top: 10px;">
            🧩 Clue to next level: "LEVEL 4 IS DOCKER COMPOSE"
        </div>
    {% else %}
        <button onclick="toggleHint('hint2', this)">Show Hint</button>
        <div class="hint" id="hint2">
            💡 This app expects an environment variable named <code>SECRET_KEY</code> with a secret value.
        </div>
    {% endif %}
</div>
{% endif %}

{% if level2 %}
<div class="level">
    <h2>Level 3: Volume Puzzle</h2>
    <p class="{{ 'pass' if level3 else 'fail' }}">{{ level3_msg }}</p>
    {% if level3 %}
        <div class="hint" style="display: block; margin-top: 10px;">
            🧩 Clue to next level: Build and Run an API container and connect via Docker Compose, using the following api.py code:
            <pre><code>from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "You reached the API! Go to Level 5."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)</code></pre>
        </div>
    {% else %}
        <button onclick="toggleHint('hint3', this)">Show Hint</button>
        <div class="hint" id="hint3">
            💡 Create a file called <code>GOAL.txt</code> into <code>/data</code> with the reqired content (remember the clue?).
        </div>
    {% endif %}
</div>
{% endif %}

{% if level3 %}
<div class="level">
    <h2>Level 4: Docker Compose Networking</h2>
    <p class="{{ 'pass' if level4 else 'fail' }}">{{ level4_msg }}</p>
    {% if level4 %}
        <div class="hint" style="display: block; margin-top: 10px;">
            🧩 Clue to next level: Learn about Nginx, so http://localhost:8081 will redirect us to the site of monkeytype.com.
        </div>
    {% else %}
        <button onclick="toggleHint('hint4', this)">Show Hint</button>
        <div class="hint" id="hint4">
            💡 Try using Docker Compose with two services: <code>web</code> and <code>api</code>.
        </div>
    {% endif %}
</div>
{% endif %}

{% if level4 %}
<div class="level">
    <h2>Level 5: Nginx Fun Game!</h2>
    <p class="{{ 'pass' if level5 else 'fail' }}">{{ level5_msg }}</p>
    {% if level5 %}
        <div class="hint" style="display: block; margin-top: 10px;">
            🎉 You escaped the Docker room!
        </div>
    {% else %}
        <button onclick="toggleHint('hint5', this)">Show Hint</button>
        <div class="hint" id="hint5">
            💡 Build something cool with NGINX... maybe try to build a container that exporting <a href="https://monkeytype.com" target="_blank">https://monkeytype.com</a>?
        </div>
    {% endif %}
</div>
{% endif %}
</body>
</html>
'''

@app.route("/")
def index():
    # Level 1
    # port_env = os.environ.get("SERVER_PORT")
    # level1 = port_env in ["80", "8080"]
    level1 = True
    level1_msg = LEVEL_HINTS["level1"] #mif level1 else "❌ Level 1: This server must be reachable on port 80 or 8080." - if they can see it, it means the port is exposed.

    # Level 2
    if level1:
        level2 = os.environ.get("SECRET_KEY") == "Fusion-the-goats"
        level2_msg = LEVEL_HINTS["level2"] if level2 else "❌ Level 2: SECRET_KEY is missing or incorrect."
    else:
        level2 = False
        level2_msg = ""

    # Level 3
    if level2:
        goal_path = "/data/GOAL.txt"
        level3 = os.path.exists(goal_path) and open(goal_path).read().strip() == "LEVEL 4 IS DOCKER COMPOSE"
        level3_msg = LEVEL_HINTS["level3"] if level3 else "❌ Level 3: Missing or incorrect file /data/GOAL.txt."
    else:
        level3 = False
        level3_msg = ""

    # Level 4
    if level3:
        try:
            r = requests.get("http://api:5000", timeout=2)
            level4 = r.ok
        except:
            level4 = False
        level4_msg = LEVEL_HINTS["level4"] if level4 else "❌ Level 4: Could not reach the API service at http://api:5000."
    else:
        level4 = False
        level4_msg = ""
    
    # Level 5
    if level4:
        try:
            r = requests.get("http://game", timeout=2)
            level5 = r.ok
        except:
            level5 = False
        level5_msg = "✅ Level 5 complete: Monkeytype is live at http://game!" if level5 else "❌ Level 5: Could not reach monkeytype at http://game."
    else:
        level5 = False
        level5_msg = ""

    return render_template_string(HTML_TEMPLATE,
                                  level1=level1,
                                  level2=level2,
                                  level3=level3,
                                  level4=level4,
                                  level5=level5,
                                  level1_msg=level1_msg,
                                  level2_msg=level2_msg,
                                  level3_msg=level3_msg,
                                  level4_msg=level4_msg,
                                  level5_msg=level5_msg)

if __name__ == '__main__':
    port = int(os.environ.get("SERVER_PORT", 80))
    app.run(host="0.0.0.0", port=port)