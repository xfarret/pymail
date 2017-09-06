from db.engine import DbEngine
from entity.account import Account


class AccountManager:
    __accounts__ = {}
    __logged__ = {}
    __instance__ = None

    def __init__(self):
        session = DbEngine.get_session()
        for account in session.query(Account):
            self.__accounts__[account.id] = account
        session.close()

    @staticmethod
    def get_instance():
        """
        Singelton return AccountManager unique instance
        :return: AccountManager
        """
        if AccountManager.__instance__ is None:
            AccountManager.__instance__ = AccountManager()
        return AccountManager.__instance__

    def list(self):
        """
        Get all accounts
        :return: dict
        """
        return self.__accounts__

    def get(self, account_id):
        """
        Get a specific account
        :param account_id: the account's reference
        :return: Account if found, None otherwise
        """
        if account_id in self.__accounts__:
            return self.__accounts__[account_id]
        return None

    def add_account(self, account):
        """
        Add an account on the account's list and store it on the database
        :param account:
        :return: True if no error occures, False otherwise
        """
        session = DbEngine.get_session()
        try:
            session.add(account)
            session.commit()
            self.__accounts__[account.id] = account
            session.close()
        except:
            return False
        finally:
            session.close()
        return True

    def remove_account(self, account):
        """
        Remove an account on the account's list and remove it on the database
        :param account:
        :return: True if no error occures, False otherwise
        """
        session = DbEngine.get_session()
        try:
            account_id = account.id
            session.delete(account)
            session.commit()
            del self.__accounts__[account_id]
        except:
            return False
        finally:
            session.close()
        return True

