from brownie import SimpleStorage, accounts


def test_deploy():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    assert stored_value == 0


def test_update_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(15, {"from": account})

    updated_stored_value = simple_storage.retrieve()

    assert updated_stored_value == 15
