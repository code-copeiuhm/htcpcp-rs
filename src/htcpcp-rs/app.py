from flask import Flask
from flask import request, session
import json

from .coffeeMachine import CoffeeMachine
from .coffeeLogger import CoffeeLogger
from .coffeeError import CanisterError, PotOccupiedError, PotPourError

app = Flask(__name__)
app.secret_key = "secret"

coffeeMachine = CoffeeMachine(3, 1, 30)
coffeeMachine.fillCanister(0, 500)
coffeeMachine.fillCanister(1, 500)
coffeeMachine.fillCanister(2, 500)
coffeeLogger = CoffeeLogger()

accepted_additions = ["Cream", "Half-and-half", "Whole-milk", "Part-Skim", "Skim", "Non-Dairy", "Vanilla", "Almond", "Raspberry", "Chocolate", "Whisky", "Rum", "Kahlua", "Aquavit"]

@app.route("/pot-<pot>", methods=["BREW", "POST"])
def brew(pot):
    global coffeeMachine, coffeeLogger
    session["id"] = coffeeLogger.nextSession()

    rawBrewData = request.get_data().decode("utf-8")

    if request.content_type != "application/coffee-pot-command" or rawBrewData == "":
        return "Expected coffee pot command", 406
    
    additions = request.headers.get("Accept-Additions", "").strip().split(";")
    if "" in additions:
        additions.remove("")
    print(additions)
    if len(additions) > 0 and any(a not in accepted_additions for a in additions):
        return {"Accepted-Additions": accepted_additions}, 406

    brewData = json.loads(rawBrewData)

    potID = int(pot)
    try: 
        time = coffeeMachine.brewCoffee(potID, additions, brewData["canister"], brewData["beanAmount"], brewData["temp"], brewData["mil"])
    except CanisterError as e:
        return str(e), 500
    except PotOccupiedError as e:
        return str(e), 406
    except IndexError:
        return {"message": f"This Coffee Machine only have {coffeeMachine.potAmount}"}, 406


    coffeeLogger.createLog(
        potID, 
        session["id"], 
        additions, 
        brewData["canister"], 
        brewData["beanAmount"], 
        brewData["temp"], 
        brewData["mil"],
        time, 
        len(additions) > 0
        )

    return {"message:":"Coffee with " + "and ".join(a + " " for a in additions)}, 200

@app.route("/", methods=["GET"])
def get():
    return "Coffee Machine"

@app.route("/", methods=["PROPFIND"])
def propfind():
    global coffeeLogger, accepted_additions
    return {"logs": coffeeLogger.logs, "opots": coffeeMachine.occupiedPots, "canisters": coffeeMachine.canisterStatus, "accepted-additions": accepted_additions}, 200

@app.route("/pot-<pot>", methods=["WHEN"])
def when(pot: str):
    potID = int(pot)
    global coffeeMachine
    try:
        time = coffeeMachine.stopPouring(potID)
        coffeeLogger.setPourTime(session["id"], time)
    except PotPourError as e:
        return {"message": str(e)}, 406
    return {"message": "Elapsed time", "time": time}, 200


