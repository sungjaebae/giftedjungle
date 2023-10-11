from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


def insert_user():
    with open('./static/seed_data/user.json', 'r', encoding='UTF8') as f:
        data = json.load(f)
        db.users.insert_many(data)


def insert_category():
    with open('./static/seed_data/category.json', 'r', encoding='UTF8') as f:
        data = json.load(f)
        db.categories.insert_many(data)


def insert_gift():
    with open('./static/seed_data/gift.json', 'r', encoding='UTF8') as f:
        data = json.load(f)
        db.gifts.insert_many(data)


def drop_all():
    db.users.delete_many({})
    db.categories.delete_many({})
    db.gifts.delete_many({})


if __name__ == '__main__':
    drop_all()
    insert_user()
    insert_category()
    insert_gift()
