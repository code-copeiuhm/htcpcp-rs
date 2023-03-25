class CanisterError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class JobTerminatedError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class PotOccupiedError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)

class PotPourError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)