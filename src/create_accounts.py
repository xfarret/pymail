from manager.account_manager import AccountManager
from entity.account import Account

accountManager = AccountManager.get_instance()

gmailAccount = Account()
gmailAccount.name = 'Gmail'
gmailAccount.firstname = 'Xavier'
gmailAccount.lastname = 'Farret'
gmailAccount.email = 'mail@gmail.com'
gmailAccount.password = 'password'
gmailAccount.imap_server = 'imap.gmail.com'
accountManager.add_account(gmailAccount)

freeAccount = Account()
freeAccount.name = 'Free'
freeAccount.firstname = 'Xavier'
freeAccount.lastname = 'Farret'
freeAccount.email = 'mail@free.fr'
freeAccount.password = 'password'
freeAccount.imap_server = 'imap.free.fr'
accountManager.add_account(freeAccount)

accounts = dict(accountManager.list()).items()

for (key, account) in accounts:
    print(account.name + " created")


