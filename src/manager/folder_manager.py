from db.engine import DbEngine
from entity.folder import Folder
from manager.account_manager import AccountManager
from manager.encoder_manager import EncoderManager


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
                FolderManager.__create_label__(account, None, labelStruct[1], labelStruct[0], labelStruct[2:])
            else:
                FolderManager.__create_label__(account, None, labelStruct[1], labelStruct[0], None)

    @staticmethod
    def __create_label__(account, parent, child_name, attributes, children=None):
        child_name = FolderManager.__clean_label__(child_name)
        attributes = FolderManager.__clean_attribute__(attributes)

        folder = Folder()
        folder.name = child_name
        folder.attributes = attributes
        if parent is not None:
            folder.parent = FolderManager.__get_folder__(account, parent.name)
            # folder.parent = parent

        folder = FolderManager.__persist__(account, folder)

        if children is None:
            return folder

        if len(children) > 1:
            return FolderManager.__create_label__(account, parent=folder, child_name=children[0], attributes=attributes, children=children[1:])
        else:
            return FolderManager.__create_label__(account, parent=folder, child_name=children[0], attributes=attributes)

    @staticmethod
    def __clean_label__(label):
        label = label.replace('" ', '')
        label = label.replace('"', '')
        return EncoderManager.imaputf7decode(label)

    @staticmethod
    def __clean_attribute__(attribute):
        attribute = attribute.replace('"', '')
        attribute = attribute.replace('(', '')
        attribute = attribute.replace(')', '')
        return attribute.replace('\\', '')

    @staticmethod
    def __persist__(account, folder):
        session = DbEngine.get_session(account.id, account.db_url)

        query = session.query(Folder).filter(Folder.name == folder.name)
        exists = session.query(query.exists()).one()[0]

        if exists:
            folder = FolderManager.__get_folder__(account, folder_name=folder.name)
        else:
            session.add(folder)
            session.commit()
            session.close()

        return folder

    @staticmethod
    def __get_folder__(account, folder_name):
        session = DbEngine.get_session(account.id, account.db_url)
        query = session.query(Folder).filter(Folder.name == folder_name)
        result = query.one()
        session.close()

        return result


    # def get_message_labels(self, headers):
    #     if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
    #         labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
    #         return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
    #     else:
    #         return list()
