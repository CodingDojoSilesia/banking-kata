import uuid

import pytest
from bank import Bank
from freezegun import freeze_time


@freeze_time("2019-11-14 12:00:01")
def test_bank_founding():
    bank = Bank("mBank")

    assert bank.history == [(1573729201.0, "Bank mBank has been founded.")]
    assert bank.transfer_commission == 0.0000001
    assert bank.storage_commission == 0.00000001
    assert bank.accounts == {}
    assert bank.income == 0.00
    assert bank.uptime == 0


def test_bank_open_account():
    bank = Bank()

    account_number = bank.open_account("Michał Klich")

    assert uuid.UUID(account_number)
    assert bank.history[0].message == "Bank PKO has been founded."
    assert bank.history[1].message == f"Account{account_number} has been opened."


def test_bank_open_account_with_initial_balance():
    bank = Bank()
    balance = 100

    account_number = bank.open_account("Michał Klich", balance=balance)

    assert uuid.UUID(account_number)
    assert bank.history[0].message == "Bank PKO has been founded."
    assert bank.history[1].message == f"Account {account_number} has been opened."
    assert bank.history[2].message == f"Account {account_number} balance is {balance}"
    assert bank.accounts.get(account_number).balance == 100


def test_bank_open_account_with_negative_balance():
    bank = Bank()
    balance = -1

    with pytest.raises(InvalidOpeningBalance):
        bank.open_account("Michał Klich", balance=balance)


def test_bank_existing_account_fetch():
    bank = Bank()

    account_number = bank.open_account("Michał Klich")

    assert bank.accounts.get(account_number)


def test_bank_non_existing_account_fetch():
    bank = Bank()

    with pytest.raises(AccountDoesNotExist):
        bank.accounts.get("0577a803-43bb-4aa1-9b26-7c4f93b1167d")


def test_bank_close_existing_account():
    bank = Bank()

    account_number = bank.open_account("Michał Klich")

    assert bank.close_account(account_number) == (
        account_number,
        0,
    )  # returns deposited cash


def test_bank_close_not_existing_account():
    bank = Bank()

    with pytest.raises(AccountDoesNotExist):
        bank.close_account("0fc19b67-1966-46bc-a907-eb79a128b746")


def test_bank_transfer_successful():
    bank = Bank()
    acc1 = bank.open_account("Lord Voldemort", balance=100)
    acc2 = bank.open_account("Tom Marvolo Riddle")

    transfer_report = bank.transfer(source=acc1, target=acc2, amount=50)

    assert transfer_report == {
        "status": "done",
        "source": {
            "account_number": acc1,
            "balance": 100 - 50 - 50 * bank.transfer_commission,
        },
        "target": {"account_number": acc2, "balance": 50},
        "commission": 50 * bank.transfer_commission,
    }

    assert bank.accounts[acc1].balance == 100 - 50 - 50 * bank.transfer_commission
    assert bank.accounts[acc2].balance == 50
    assert bank.income == 50 * bank.transfer_commission

    assert (
        sum(bank.accounts[acc1].balance, bank.accounts[acc1].balance, bank.income)
        == 100
    )

    assert f"Transfer of 50 from account: {acc1} to account: {acc2}" in bank.history
    assert (
        f"Withdrawal of 50. Commission {50 * bank.transfer_commission}"
        in bank.accounts[acc1].history
    )
    assert f"Deposit of 50" in bank.accounts[acc2].history


def test_bank_transfer_insufficient_sender_balance():
    bank = Bank()
    acc1 = bank.open_account("Lord Voldemort")
    acc2 = bank.open_account("Tom Marvolo Riddle")

    with pytest.raises(InsufficientTransferBalance):
        bank.transfer(source=acc1, target=acc2, amount=50)

    assert bank.accounts[acc1].balance == 0
    assert bank.accounts[acc2].balance == 0
    assert bank.income == 0

    assert f"Transfer of 50 from account: {acc1} to account: {acc2}" in bank.history
    assert (
        f"Withdrawal of 50. Commission {50 * bank.transfer_commission}"
        in bank.accounts[acc1].history
    )
    assert f"Deposit of 50" in bank.accounts[acc2].history


def test_bank_transfer_to_non_existing_account():
    bank = Bank()
    acc1 = bank.open_account("Lord Voldemort")

    with pytest.raises(AccountDoesNotExist):
        bank.transfer(
            source=acc1, target="931a5ead-5bf8-40e2-b341-62e5ad70e1aa", amount=50
        )


def test_bank_uptime_increase():
    bank = Bank()
    acc1 = bank.open_account("Lord Voldemort")

    assert bank.uptime == 1

    acc1 = bank.open_account("Tom Marvolo Riddle")

    assert bank.uptime == 2

    bank.deposit(acc1, 100)
    bank.deposti(acc2, 100)

    assert bank.uptime == 4


def test_bank_storage_commission():
    bank = Bank()
    opening_balance = 100000000000000
    acc1 = bank.open_account("Richie Rich", balance=opening_balance)

    for _ in range(199):
        bank.open_account()

    assert (
        bank.accounts[acc1].balance
        == opening_balance - opening_balance * bank.storage_commission
    )
