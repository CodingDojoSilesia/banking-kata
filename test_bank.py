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
    assert bank.accounts == []
    assert bank.income == 0.00


def test_bank_create_account():
    bank = Bank()

    account_number = bank.open_account("Michał Klich")

    assert uuid.UUID(account_number)
    assert bank.history[0].message == "Bank PKO has been founded."
    assert bank.history[1].message == f'Account{account_number} has been opened.'

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

    assert bank.close_account(account_number) == 0  # returns deposited cash

def test_bank_close_not_existing_account():
    bank = Bank()

    with pytest.raises(AccountDoesNotExist):
        bank.close_account("0fc19b67-1966-46bc-a907-eb79a128b746")
