from db.engine import DbEngine
from entity.mail import Mail
from manager.account_manager import AccountManager
import email
import re


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

    def get_labels(self, account, directory='""'):
        structuredLabels = {'root': []}
        mail = account.login()
        typ, labels = mail.list(directory)
        for labelElems in labels:
            labelElems = labelElems.decode()
            labelStruct = labelElems.split('/')
            if len(labelStruct) == 2:
                label = labelStruct[1].replace('" ', '')
                label = label.replace('"', '')

                structuredLabels['root'].append(label)
            else:

                for i in range(1, len(labelStruct)):
                    label = labelStruct[i].replace('" ', '')
                    label = label.replace('"', '')
                    print(label)
            # structuredLabels['root'] = label

        return labels

    def get_message_labels(self, headers):
        if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
            labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
            return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
        else:
            return list()

    # def get_mail_to_download(self):
    #     session = DbEngine.get_session()

