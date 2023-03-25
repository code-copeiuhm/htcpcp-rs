from typing import Any
from flask import Flask
from flask import request
import json
from time import sleep
import time

app = Flask(__name__)

coffee_sessions: dict[int, Any] = dict()
bean_canister = [500.0, 500.0]
coffee_log: dict[int, dict] = dict()

session_id = 0


WATER_TIME = 30 # 10 seconds per 100 ml water

def new_coffee_session() -> str:
    global session_id
    rv = str(session_id)
    session_id = session_id + 1
    return rv

def getBrewTime(canister: int=0, beanAmount: float=0, temp: int=0, mil: int=0, **kwargs) -> float:
    if canister >= len(bean_canister):
        raise Exception("paid bex")
    
    newAmount = bean_canister[canister] - beanAmount
    
    if newAmount < 0:
        raise Exception("Paid Bex 2")
    
    bean_canister[canister] = newAmount

    return (mil / 100) * WATER_TIME * (temp / 100)

@app.route("/", methods=["BREW", "POST"])
def hello_world():    
    raw = request.get_data().decode("utf-8")
    if request.content_type != "application/coffee-pot-command" or raw == "":
        return "Expected coffee pot command", 406

    
    global coffee_sessions, coffee_log, bean_canister

    session = new_coffee_session()
    additions = request.headers.get("Accept-Additions", "").split(";")


    data = json.loads(raw)
    brew_time = getBrewTime(data["canister"], data["beanAmount"], data["temp"], data["mil"]) 
    sleep(brew_time)

    noAdditions = len(additions) == 0
    startTime = 0 if noAdditions else time.time()
    coffee_sessions[session] = startTime

    coffee_log[session] = {
        "sesssion": session,
        "add": additions,
        "brewTime": brew_time,
        "pourTime": startTime,
        "pouring": not noAdditions,
        "data": data
        }

    return json.dumps({"sessionID":session}), 200

@app.route("/", methods=["GET"])
def get():
    return "Coffee Machine"

@app.route("/<session>", methods=["PROPFIND"])
def prop_get(session: str):
    global coffee_log
    if session not in coffee_log:
        return "No Session found!", 406
    
    log = coffee_log[session]
    if log["pouring"] == True:
        log["pourTime"] = time.time() - log["pourTime"]

    return json.dumps(log), 200

@app.route("/<session>", methods=["WHEN"])
def when(session: str):
    global coffee_sessions, coffee_log
    ctime = coffee_sessions[session]

    if ctime == 0:
        return "Not pouring milk!", 406
    
    elapsed = time.time() - ctime
    coffee_sessions[session] = elapsed
    coffee_log[session]["pourTime"] = elapsed
    coffee_log[session]["pouring"] = False

    return json.dumps({"elapsed":elapsed}), 200


