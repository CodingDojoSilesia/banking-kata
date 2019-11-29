from history_tool import History, AddHistoryMixIn
from typing import Union


class NegativeValue(Exception):
    pass


class BalanceTooLow(Exception):
    pass


class Account(AddHistoryMixIn):

    def __init__(self, id, balance :Union[int, float] = 0, client_name :str = '') -> None:
        super().__init__()
        self.client_name = client_name
        self.id = id
        if balance < 0:
            raise NegativeValue("You can't deposit a negative value or equal to zero.")
        self.balance = balance
        self.add_history(
            message=f"Account {id} opened with balance {balance}"
        )
        self.active = True

    def deposit(self, value :Union[int, float]) -> None:
        self.add_history(
            message=f"Deposit of {value}"
        )
        if value <= 0:
            raise NegativeValue("You can't deposit a negative value or equal to zero.")
        self.balance += value

    def withdrawal(self, value :Union[int, float]) -> None:
        if self.balance - value < 0:
            self.add_history(
                message=f"Withdrawal {value} failed. BalanceTooLow"
            )
            raise BalanceTooLow("You don't have enough money on your account.")
        self.add_history(
            message=f"Withdrawal {value}"
        )
        self.balance -= value

    def close(self) -> Union[int, float]:
        self.active = False
        self.add_history(
            message=f"Account {self.id} closed. Returned {self.balance} cash",
        )
        return self.balance