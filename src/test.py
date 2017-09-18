from db.engine import DbEngine
from manager.account_manager import AccountManager
from manager.folder_manager import FolderManager
from manager.mail_manager import MailManager

session = DbEngine.get_session()
# print(session)

account = AccountManager.get_instance().get(2)
# mailManager = MailManager()
# print(mailManager.get_structured_labels(account))
# uids = mailManager.get_mail_uids(account)
# print(uids)
# mails = mailManager.get_mails(account, uids)
# print(len(mails))

# FolderManager.init_labels(account)

mail_manager = MailManager()
mail_manager.new_mail(None, account, "Sent")

# for mail in new_mail_generator(last_uid=42,
#                                host="imap.example.com", port=143,
#                                login="user@exampl.com",
#                                password="password"):
