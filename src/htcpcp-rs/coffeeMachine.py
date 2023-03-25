from .coffeeError import CanisterError, PotOccupiedError, PotPourError
import time
from copy import deepcopy

class CoffeeMachine:
    def __init__(self, beanCanisters: int, pots: int, boilTime: float) -> None:
        self.__boilTime = boilTime
        self.__beanCanisters = [0] * beanCanisters
        self.__pots = [False] * pots
        self.__pouringJobs = [0] * pots

    @property
    def canisterAmount(self):
        return len(self.__beanCanisters)
    
    @property
    def canisterStatus(self):
        return deepcopy(self.__beanCanisters)

    @property
    def occupiedPots(self):
        return [i for i, p in enumerate(self.__pots) if not p]
    
    @property
    def potAmount(self):
        return len(self.__pots)

    def brewCoffee(self, potIndex: int, additions: list[str], canister: int, beanAmount: float, temp: int, mil: int):
        if self.__pots[potIndex]:
            raise PotOccupiedError(f"Pot {potIndex} is occupied")
        self.__pots[potIndex] = True
    
        brewTime = self.__brewTime(canister, beanAmount, temp, mil)
        addLiquid = True if len(additions) > 0 else False

        time.sleep(brewTime)
        if addLiquid:
            self.__pouringJobs[potIndex] = time.time()
        else:
            self.__pots[potIndex] = False
        return brewTime

    def stopPouring(self, potIndex: int):
        if not self.__pots[potIndex]:
            raise PotPourError(f"Pot {potIndex} is not pouring!")
        self.__pots[potIndex] = False
        pourTime = time.time() - self.__pouringJobs[potIndex]
        self.__pouringJobs[potIndex] = 0
        return pourTime
    
    def fillCanister(self, canister: int, amount: float):
        if canister > self.canisterAmount - 1:
            raise CanisterError(f"Canister {canister} does not exist!")
        self.__beanCanisters[canister] += amount

    def __brewTime(self, canister: int, beanAmount: float, temp: int, mil: int):
        if canister > self.canisterAmount - 1:
            raise CanisterError(f"Canister {canister} does not exist!")
       
        newAmount = self.__beanCanisters[canister] - beanAmount

        if newAmount < 0:
            raise CanisterError(f"Canister {canister} does not have enough beans! Has {self.__beanCanisters[canister]} beans")
        
        self.__beanCanisters[canister] = newAmount
        
        return (mil / 100) * self.__boilTime * (temp / 100)

