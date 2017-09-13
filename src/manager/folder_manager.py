from db.engine import DbEngine
from entity.folder import Folder
from entity.mail import Mail
from manager.account_manager import AccountManager
import email
import re


class FolderManager:
    __accountManager__ = None

    def __init__(self):
        self.__accountManager__ = AccountManager.get_instance()

    @staticmethod
    def init_labels(account):
        imap = account.login()
        typ, labels = imap.list('""')
        for labelElems in labels:
            labelElems = labelElems.decode()
            labelStruct = labelElems.split('/')

            if len(labelStruct) > 2:
                FolderManager.__create_label(None, labelStruct[1], labelStruct[2:])
            else:
                FolderManager.__create_label(None, labelStruct[1], None)
            # for i in range(1, len(labelStruct)):
            #     label = labelStruct[i].replace('" ', '')
            #     label = label.replace('"', '')
            #     print(label)


    @staticmethod
    def __create_label(parent, child_name, children=None):
        # create child
        folder = Folder()
        folder.name = child_name
        if parent is not None:
            folder.parent = parent

        if children is None:
            return folder

        if len(children) > 1:
            return FolderManager.__create_label(parent=folder, child_name=children[0], children=children[1:])
        else:
            return FolderManager.__create_label(parent=folder, child_name=children[0])



    # def get_labels(self, account, directory='""'):
    #     structuredLabels = {'root': []}
    #     mail = account.login()
    #     typ, labels = mail.list(directory)
    #     for labelElems in labels:
    #         labelElems = labelElems.decode()
    #         labelStruct = labelElems.split('/')
    #         if len(labelStruct) == 2:
    #             label = labelStruct[1].replace('" ', '')
    #             label = label.replace('"', '')
    #
    #             structuredLabels['root'].append(label)
    #         else:
    #
    #             for i in range(1, len(labelStruct)):
    #                 label = labelStruct[i].replace('" ', '')
    #                 label = label.replace('"', '')
    #                 print(label)
    #         # structuredLabels['root'] = label
    #
    #     return labels

    # def get_message_labels(self, headers):
    #     if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
    #         labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
    #         return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
    #     else:
    #         return list()
