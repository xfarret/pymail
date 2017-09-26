from manager.account_manager import AccountManager

accountManager = AccountManager.get_instance()

accounts = dict(accountManager.list()).items()

for (key, account) in accounts:
    print(account.name)
    accountManager.remove_account(account, True)
