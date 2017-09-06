from manager.account_manager import AccountManager
from entity.account import Account

accountManager = AccountManager.get_instance()

gmailAccount = Account()
gmailAccount.name = 'Gmail'
gmailAccount.firstname = 'firstname'
gmailAccount.lastname = 'lastname'
gmailAccount.email = 'email@gmail.com'
gmailAccount.password = 'password'
accountManager.add_account(gmailAccount)

freeAccount = Account()
freeAccount.name = 'Free'
freeAccount.firstname = 'firstname'
freeAccount.lastname = 'lastname'
freeAccount.email = 'email@free.fr'
freeAccount.password = 'password'
accountManager.add_account(freeAccount)

accounts = dict(accountManager.list()).items()

for (key, account) in accounts:
    print(account.name)
    accountManager.remove_account(account)


