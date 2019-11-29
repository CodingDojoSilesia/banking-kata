import uuid

import pytest

from account import *


def test_account_deposit():
    acc = Account(uuid.uuid4())

    acc.deposit(100)

    assert acc.balance == 100


def test_account_withdrawal_enough_balance():
    acc = Account(uuid.uuid4(), balance=100)

    acc.withdrawal(100)

    assert acc.balance == 0


def test_account_withdrawal_short_balance():
    acc = Account(uuid.uuid4())

    with pytest.raises(BalanceTooLow):
        acc.withdrawal(100)


def test_account_history_log():
    acc_no = uuid.uuid4()
    acc = Account(acc_no, balance=100)
    acc.withdrawal(100)
    with pytest.raises(BalanceTooLow):
        acc.withdrawal(100)
    acc.deposit(100)
    cash = acc.close()

    assert cash == 100
    assert acc.history == sorted(acc.history)  # is it sorted?
    assert [x.message for x in acc.history] == [
        f"Account {acc_no} opened with balance 100",
        "Withdrawal 100",
        "Withdrawal 100 failed. BalanceTooLow",
        "Deposit of 100",
        f"Account {acc_no} closed. Returned 100 cash",
    ]
