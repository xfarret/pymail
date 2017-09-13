from db.engine import DbEngine
from entity.mail import Mail
from manager.account_manager import AccountManager
import email
import re


class FolderManager:
    __accountManager__ = None

    def __init__(self):
        self.__accountManager__ = AccountManager.get_instance()

