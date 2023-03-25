from copy import deepcopy


class CoffeeLogger:
    def __init__(self) -> None:
        self.__logs: list[dict] = []
        self.__sessionCounter = 0
    
    @property
    def logs(self):
        return deepcopy(self.__logs)
    
    def nextSession(self):
        session = self.__sessionCounter
        self.__sessionCounter += 1
        return session

    def log(self, session: int):
        return deepcopy(self.__logs[session])

    def createLog(self, pot: int, session: int, additions: list[str], canister: int, 
                    beanAmount: float, temp: int, mil: int, brewTime: float, pouring: bool):
        self.__logs.append({
            "pot": pot, 
            "session": session,
            "additions": additions, 
            "canister": canister, 
            "beanAmount": beanAmount, 
            "temperature": temp, 
            "coffeeSize": mil,
            "brewTime": brewTime,
            "pouring": pouring,
        })

    def setPourTime(self, session: int, time: float):
        self.__logs[session]["pourTime"] = time
        self.__logs[session]["pouring"] = False