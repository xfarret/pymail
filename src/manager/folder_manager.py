from sqlalchemy.sql.expression import or_
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
        internal_name = FolderManager.__extract_attribute_name__(attributes)
        if internal_name is None:
            internal_name = child_name

        folder = Folder()
        folder.name = child_name
        folder.internal_name = internal_name
        folder.attributes = attributes
        if parent is not None:
            folder.parent = FolderManager.get_folder(account, parent.name)
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
        # return attribute.replace('\\', '')
        return attribute

    @staticmethod
    def __extract_attribute_name__(attribute_str):
        attributes = attribute_str.replace('\\', '').split(" ")
        for flag in attributes:
            if flag != 'Seen' and flag != 'Answered' and flag != 'Flagged' and flag != 'Deleted' and flag != 'Recent' and \
                            flag != 'HasNoChildren' and flag != 'Draft' and flag != 'Noselect' and \
                            flag != 'HasChildren' and flag != 'NoInferiors' and flag != '':
                return flag
        return None

    @staticmethod
    def __persist__(account, folder):
        session = DbEngine.get_session(account.id, account.db_url)

        query = session.query(Folder).filter(Folder.name == folder.name)
        exists = session.query(query.exists()).one()[0]

        if exists:
            folder = FolderManager.get_folder(account, folder_name=folder.name)
        else:
            session.add(folder)
            session.commit()
            session.close()

        return folder

    @staticmethod
    def get_folder(account, folder_name):
        session = DbEngine.get_session(account.id, account.db_url)
        query = session.query(Folder).filter(or_(Folder.name == folder_name, Folder.internal_name == folder_name))
        result = query.one()
        session.close()

        return result

    @staticmethod
    def get_folder_path(account, internal_name):
        session = DbEngine.get_session(account.id, account.db_url)

        folder = session.query(Folder).filter(Folder.internal_name == internal_name).one()
        if folder.parent_id is not None:
            parent = session.query(Folder).get(folder.parent_id)

            return FolderManager.get_folder_path(account, parent.internal_name) + "/" + folder.internal_name
        return folder.internal_name

    # def get_message_labels(self, headers):
    #     if re.search(r'X-GM-LABELS \(([^\)]+)\)', headers):
    #         labels = re.search(r'X-GM-LABELS \(([^\)]+)\)', headers).groups(1)[0].split(' ')
    #         return map(lambda l: l.replace('"', '').decode("string_escape"), labels)
    #     else:
    #         return list()
