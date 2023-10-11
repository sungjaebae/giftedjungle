from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


def insert_user():
    pass


def insert_gift():
    pass


def drop_all():
    pass


if __name__ == '__main__':
    drop_all()
    insert_user()
    insert_gift()
