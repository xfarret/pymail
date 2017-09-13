# from entity.mail import Mail
from datetime import datetime
from email.message import Message
from email.parser import BytesParser

from db.engine import DbEngine
from entity.mail import Mail
from manager.account_manager import AccountManager
import email


class MailManager:
    __accountManager__ = None

    def __init__(self):
        self.__accountManager__ = AccountManager.get_instance()

    def get_mails(self, account, email_uids):
        """
        Get mails from specific account
        :param account: Account
        :return:
        """
        mails_to_return = {}
        ressource = account.login()
        for uid in email_uids:
            typ, msg_data = ressource.uid('fetch', uid, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    mail = Mail()
                    # for header in ['subject', 'to', 'from']:
                    mail.date = msg['date']
                    mail.to_field = msg['to']
                    mail.from_field = msg['from']
                    mail.reply_to = msg['reply-to']
                    mail.cc = 'None'
                    mail.bcc = 'None'
                    mail.message_id = msg['message-id']
                    mail.subject = msg['subject']
                    mail.header = 'None'
                    mail.content_type = msg.get_content_type()
                    mail.body = {}

                    if msg.is_multipart():
                        for payload in msg.get_payload():
                            mail.body[payload.get_content_type()] = payload.get_payload()
                    else:
                        mail.body[mail.content_type] = msg.get_payload()
                        # print('%-8s: %s' % (header.upper(), msg[header]))
                    mail.priority = msg['priority']
                    mail.charset = msg.get_content_charset()
                    # mail.label = label
                    mail.account_id = account.id
                    mails_to_return[uid] = mail

        return mails_to_return

    def get_mail_uids(self, account, label='INBOX'):
        """
        Get mail uids from specific account
        :param account: Account
        :param label: str
        :return:
        """
        ressource = account.login()
        ressource.select(label, readonly=True)
        result, data = ressource.uid('search', None, "ALL")
        return data[0].split()

    def get_structured_labels(self, account, directory='""'):
        structuredLabels = {}
        mail = account.login()
        typ, labels = mail.list(directory)
        for labelElems in labels:
            labelElems = labelElems.decode()
            # labelElems = labelElems.replace('"', '')
            labelStruct = labelElems.split('/')
            if len(labelStruct) == 2:
                label = labelStruct[1].replace('" ', '')
                label = label.replace('"', '')
                if 'root' not in structuredLabels:
                    structuredLabels['root'] = []
                structuredLabels['root'].append(label)

            # structuredLabels['root'] = label

        return labels

    def get_label_uids(self, account):
        ressource = account.login()
        uid('FETCH', uid, '(X-GM-LABELS)')
        return ressource.fetch('search', '(X-GM-LABELS)')

    def get_mail_to_download(self):
        session = DbEngine.get_session()

