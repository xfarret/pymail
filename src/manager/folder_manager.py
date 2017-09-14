import base64

from sqlalchemy.orm.query import Query

from db.engine import DbEngine
from entity.folder import Folder
from manager.account_manager import AccountManager


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
        return FolderManager.__imaputf7decode__(label)

    @staticmethod
    def __clean_attribute__(attribute):
        attribute = attribute.replace('"', '')
        attribute = attribute.replace('(', '')
        attribute = attribute.replace(')', '')
        return attribute.replace('\\', '')

    @staticmethod
    def __b64padanddecode__(b):
        """Decode unpadded base64 data"""
        b += (-len(b) % 4) * '='  # base64 padding (if adds '===', no valid padding anyway)
        return base64.b64decode(b, altchars='+,', validate=True).decode('utf-16-be')

    @staticmethod
    def __imaputf7decode__(s):
        """Decode a string encoded according to RFC2060 aka IMAP UTF7.
        Minimal validation of input, only works with trusted data"""
        lst = s.split('&')
        out = lst[0]
        for e in lst[1:]:
            u, a = e.split('-', 1)  # u: utf16 between & and 1st -, a: ASCII chars folowing it
            if u == '':
                out += '&'
            else:
                out += FolderManager.__b64padanddecode__(u)
            out += a
        return out

    @staticmethod
    def __imaputf7encode__(s):
        """"Encode a string into RFC2060 aka IMAP UTF7"""
        s = s.replace('&', '&-')
        iters = iter(s)
        unipart = out = ''
        for c in s:
            if 0x20 <= ord(c) <= 0x7f:
                if unipart != '':
                    out += '&' + base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=') + '-'
                    unipart = ''
                out += c
            else:
                unipart += c
        if unipart != '':
            out += '&' + base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=') + '-'
        return out

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
