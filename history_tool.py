from datetime import datetime
from collections.abc import AsyncIterable

class History:

    def __init__(self, message :str, date=datetime.now()) -> None:
        self.message = message
        self.date = date

    def __lt__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.date < other.date
        elif isinstance(other, (list, tuple)):
            return self.message < other
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.message == other.message
        elif isinstance(other, (list, tuple, str)):
            return self.message == other

    def __repr__(self):
        return self.message


class AddHistoryMixIn:
    
    def __init__(self) -> None:
        self.history = []

    def add_history(self, message :str, date=datetime.utcnow()) -> None:
        """
        The method adds operation history. 
        Method add default date (current date).
        """
        self.history.append(
            History(
                message=message,
                date=date
            )
        )