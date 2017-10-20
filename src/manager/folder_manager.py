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
    def get_labels(account, parent=None):
        session = DbEngine.get_session(account.id, account.db_url)
        query = session.query(Folder).filter(Folder.parent_id == parent)
        folders = query.all()
        session.close()

        return folders

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
            session = DbEngine.get_session(account.id, account.db_url)
            # On réattache l objet à la session
            session.add(parent)
            folder.parent = FolderManager.get_label(account, parent.name)
            folder.path = folder.parent.path + "/" + folder.internal_name
            # On détache l objet de la session
            session.expunge(parent)
        else:
            folder.path = folder.internal_name

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

        query = session.query(Folder).filter(Folder.path == folder.path)
        exists = session.query(query.exists()).one()[0]

        if exists:
            folder = FolderManager.get_label(account, folder_path=folder.path)
        else:
            session.add(folder)
            session.commit()
            session.close()

        return folder

    @staticmethod
    def get_label(account, folder_path):
        session = DbEngine.get_session(account.id, account.db_url)
        query = session.query(Folder).filter(Folder.path == folder_path)
        result = query.one()
        session.close()

        return result
