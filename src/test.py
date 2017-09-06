from db.engine import DbEngine

session = DbEngine.get_session()
print(session)
