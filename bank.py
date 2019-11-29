import uuid
from collections import UserDict
from datetime import datetime
from functools import wraps
from typing import Dict, Tuple, Union

from account import Account
from history_tool import AddHistoryMixIn, History


class AccountDoesNotExist(Exception):
    pass 


class AccountExist(Exception):
    pass


class InvalidOpeningBalance(Exception):
    pass


class InsufficientTransferBalance(Exception):
    pass


class DictAccount(UserDict):

    def get(self, key: str):
        """
        Method return value if key exist 
        If not method raise Exception.
        """
        try:
            value = self[key]
        except KeyError:
            raise AccountDoesNotExist("Account about this id not exist")
        return value  


def payment_for_account(func):
    """
    Decorator checks if 200 operations have been performed on the account. 
    If so, a fee is charged for each account.
    """
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        bank = args[0]
        if bank.uptime == 199:
            bank.uptime = 0
            for account in bank.accounts.values():
                account.balance -= account.balance * bank.storage_commission
        result = func(*args, **kwargs)
        return result
    return wrapped_function


class Bank(AddHistoryMixIn):
    
    def __init__(self, name :str = 'PKO', storage_commission :float = 0.00000001,
                 transfer_commission :float = 0.0000001) -> None:
        super().__init__()
        self.name = name
        self.add_history(
            message=f"Bank {self.name} has been founded.",
            date=datetime.timestamp(datetime.utcnow())
        )
        self.transfer_commission = transfer_commission
        self.storage_commission = storage_commission
        self.accounts = DictAccount()
        self.income = 0.00
        self.uptime = 0

    @payment_for_account
    def open_account(self, name :str = '', balance :Union[int, float] = 0):
        """
        Method open new account.
        """
        self.uptime += 1
        if balance < 0:
            raise InvalidOpeningBalance("You can't open account with deficit.")
        id = uuid.uuid4().hex
        try:
            account = self.accounts.get(id)
        except AccountDoesNotExist:
            pass
        else:
            if account.active != False:
                raise AccountExist("Account about this id exists.")
        self.accounts[id] = Account(
            id=id,
            client_name=name,
            balance=balance
        )
        self.add_history(
            message=f"Account {id} has been opened."
        )
        self.add_history(
            message=f"Account {id} balance is {balance}"
        )
        return id

    @payment_for_account
    def close_account(self, id_client) -> Tuple:
        """
        Method close user account.
        """
        account = self.accounts.get(id_client)
        return account.id, account.close()

    @payment_for_account
    def transfer(self, source, target, amount :Union[int, float]) -> None:
        """
        The method performs operations between accounts.
        """
        self.uptime += 1
        account_source = self.accounts.get(source)
        account_target = self.accounts.get(target)
        account_source.add_history(
            message=f"Withdrawal of {amount}. Commission {amount * self.transfer_commission}"
        )
        self.add_history(
            message=f"Transfer of {amount} from account: {source} to account: {target}"
        )
        try:
            account_source.withdrawal(
                value=amount + amount * self.transfer_commission
            )
            account_target.deposit(value=amount)
            self.income = amount * self.transfer_commission
        except Exception:
            raise InsufficientTransferBalance
        self.accounts.update(
            {
                source: account_source,
                target: account_target
            }
        )
        return {
            "status": "done",
            "source": {
                "account_number": source,
                "balance": account_source.balance,
            },
            "target": {
                "account_number": target, 
                "balance": account_target.balance
            },
            "commission": amount * self.transfer_commission,
        }

    @payment_for_account
    def deposit(self, id_client, value :Union[int, float]):
        """
        The method pays money to the account.
        """
        self.uptime += 1
        self.accounts.get(id_client).deposit(value)

    @payment_for_account
    def withdrawal(self, id_client, value :Union[int, float]):
        """
        The method pays money from the account.
        """
        self.uptime += 1
        self.accounts.get(id_client).deposit(value)