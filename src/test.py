from db.engine import DbEngine
from manager.account_manager import AccountManager
from manager.folder_manager import FolderManager
from manager.mail_manager import MailManager

session = DbEngine.get_session()
# print(session)

account = AccountManager.get_instance().get(1)
# mailManager = MailManager()
# print(mailManager.get_structured_labels(account))
# uids = mailManager.get_mail_uids(account)
# print(uids)
# mails = mailManager.get_mails(account, uids)
# print(len(mails))

FolderManager.init_labels(account)

mail_manager = MailManager()
# folder = FolderManager.get_folder(account, "[Gmail]/Important")
mail_manager.sync_emails(account, "[Gmail]/Important")

# path = FolderManager.get_folder_path(account, 'INBOX')
# mail_manager.sync_emails(account, '"%s"' % path)

# imapconn = account.login()
# imapconn.select("INBOX", readonly=True)
# mail_manager.get_flags(imapconn, '472')
