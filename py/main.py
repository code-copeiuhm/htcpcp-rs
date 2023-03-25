from flask import Flask
from flask import request

app = Flask(__name__)

coffee_sessions: dict[str, any] = dict()
i = 0
def new_coffee_session() -> str:
    rv = str(i)
    i = i + 1
    return rv

@app.route("/", methods=["BREW", "POST"])
def hello_world():
    if request.content_type != "application/coffee-pot-command":
        return "Expected coffee pot command", 406
    session = new_coffee_session()
    return session, 200

@app.route("/", methods=["GET"])
def get():
    return ""

@app.route("/", methods=["PROPGET"])
def prop_get():
    return ""

@app.route("/", methods=["WHEN"])
def when():
    return ""


