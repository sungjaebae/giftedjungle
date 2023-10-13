from pymongo import MongoClient
import json
client: MongoClient = MongoClient('localhost', 27017)
db = client.dbgiftedjungle
# db.user.deleteMany({})
# db.notifications.deleteMany({})


def insert_user():
    with open('./static/seed_data/user.json', 'r', encoding='UTF8') as f:
        data = json.load(f)
        db.users.insert_many(data)


def insert_notification():
    doc = {
        'notif_id': 10,
        'url': "../static/images/food.webp",
        'giftname': "10월 15일 점심",
        'giftmsg': "밥먹자",
        'sndusrid': 1,
        'sndusrname': "김훈이",
        'sndusrimg': "../static/images/usrimg.png",
        'rcvusrid': 2,
        'rcvusrname': "김영희",
        'rcvusrimg': "../static/images/usrimg.png",
        'ischeck': False,
        'isaccept': False,
    }
    db.notifications.insert_one(doc)


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
    insert_notification()
