from entity.folder import Folder
from entity.mail import Mail
from manager.account_manager import AccountManager
from manager.folder_manager import FolderManager


class MailManager:
    __accountManager__ = None

    def __init__(self):
        self.__accountManager__ = AccountManager.get_instance()

    # def get_mails(self, account, email_uids):
    #     """
    #     Get mails from specific account
    #     :param account: Account
    #     :return:
    #     """
    #     mails_to_return = {}
    #     ressource = account.login()
    #     for uid in email_uids:
    #         typ, msg_data = ressource.uid('fetch', uid, '(RFC822)')
    #         for response_part in msg_data:
    #             if isinstance(response_part, tuple):
    #                 msg = email.message_from_bytes(response_part[1])
    #
    #                 mail = Mail()
    #                 # for header in ['subject', 'to', 'from']:
    #                 mail.date = msg['date']
    #                 mail.to_field = msg['to']
    #                 mail.from_field = msg['from']
    #                 mail.reply_to = msg['reply-to']
    #                 mail.cc = 'None'
    #                 mail.bcc = 'None'
    #                 mail.message_id = msg['message-id']
    #                 mail.subject = msg['subject']
    #                 mail.header = 'None'
    #                 mail.content_type = msg.get_content_type()
    #                 mail.body = {}
    #
    #                 if msg.is_multipart():
    #                     for payload in msg.get_payload():
    #                         mail.body[payload.get_content_type()] = payload.get_payload()
    #                 else:
    #                     mail.body[mail.content_type] = msg.get_payload()
    #                     # print('%-8s: %s' % (header.upper(), msg[header]))
    #                 mail.priority = msg['priority']
    #                 mail.charset = msg.get_content_charset()
    #                 # mail.label = label
    #                 mail.account_id = account.id
    #                 mails_to_return[uid] = mail
    #
    #     return mails_to_return

    def get_mail_uids(self, account, folder_path):
        """
        Get mail uids from specific account
        :param account: Account
        :param label: str
        :return:
        """
        ressource = account.login()
        ressource.select('"%s"' % folder_path, readonly=True)
        result, data = ressource.uid('search', None, "ALL")
        return data[0].split()

    def get_new_mails(self, imapconn, account, folder):
        """
        Get new mails for a specific account
        :param imapconn:
        :param account:
        :param folder:
        :return:
        """
        if imapconn is None:
            imapconn = account.login()
        imapconn.select('"%s"' % folder.path, readonly=True)

        session = self.__accountManager__.get_session(account)
        label_id = Folder.get_id(session, folder.path)
        if label_id is None:
            return 0

        last_email = Mail.get_last(session, label_id)
        last_uid = None
        if last_email is not None:
            last_uid = last_email.uid.decode()

        if last_uid is None:
            command = "ALL"
            last_uid = -1
        else:
            command = "UID {}:*".format(last_uid)

        result, data = imapconn.uid('search', None, command)
        messages = data[0].split()
        added_messages = 0

        for message_uid in messages:
            # SEARCH command *always* returns at least the most
            # recent message, even if it has already been synced
            if int(message_uid) > int(last_uid):
                result, data = imapconn.uid('fetch', message_uid, '(RFC822)')
                mail = Mail()
                mail.mail_from_bytes(data[0][1], message_uid)
                mail.label_id = label_id
                mail.flags = MailManager.get_flags(imapconn, message_uid)
                mail.persist(session)
                added_messages += 1
                # print('mail [' + str(mail.uid) + '] created for account [' + account.email + ']')

        return added_messages

    def check_remote_deleted_emails(self, imapconn, account, folder):
        if imapconn is None:
            imapconn = account.login()
        imapconn.select('"%s"' % folder.path, readonly=True)

        session = self.__accountManager__.get_session(account)
        label_id = Folder.get_id(session, folder.path)
        if label_id is None:
            return 0

        local_uids = Mail.get_uids(session, label_id)
        remote_uids = self.get_mail_uids(account, folder.path)
        diff_uids = list(set(local_uids) - set(remote_uids))

        for uid in diff_uids:
            Mail.get_mail(session, uid).delete(session)

        return len(diff_uids)

    def sync_emails(self, account, folder_path):
        """
        Synchronize mails for a specific label. Check removed & new mails
        :param account: account to use
        :param folder_path: folder path
        :return:
        """
        imapconn = account.login()
        folder = FolderManager.get_folder(account, folder_path)

        print("check deleted mails")
        v = self.check_remote_deleted_emails(imapconn, account, folder)
        print("%d mails removed" % v)
        print("check new mails")
        v = self.get_new_mails(imapconn, account, folder)
        print("%d mails added" % v)

    def check_unseen_messages(self, imapconn, account, label='INBOX'):
        """
        TODO
        :param imapconn:
        :param account:
        :param label:
        :return:
        """
        if imapconn is None:
            imapconn = account.login()
        imapconn.select(label, readonly=True)

        session = self.__accountManager__.get_session(account)

        status, response = imapconn.uid('search', None, "(UNSEEN)")
        if status == 'OK':
            unread_msg_nums = response[0].split()
            for uid in unread_msg_nums:
                mail = Mail.get_mail(session, uid)
                # mail.set

    @staticmethod
    def get_flags(imapconn, uid):
        status, response = imapconn.uid('FETCH', uid, "FLAGS")
        if status == 'OK':
            flags = response[0].split()
            flags_str = b"".join(flags[4:]).decode()
            flags_str = flags_str.replace("(", "")
            flags_str = flags_str.replace("))", "")
            flags_str = flags_str.replace("\\\\", "\\")
            return flags_str

        return ""
