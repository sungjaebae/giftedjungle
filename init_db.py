from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle
#db.user.deleteMany({})
#db.notification.deleteMany({})

def insert_user():
    userdoc1={
        'usrid' : 1,
        #'usrimg' : "https://png.pngtree.com/png-vector/20191009/ourmid/pngtree-user-icon-png-image_1796659.jpg",
        'usrname' : "김훈이",
        'usrpassword': 1234,
    }

    userdoc2={
        'usrid' : 2,
        #'usrimg' : "https://png.pngtree.com/png-vector/20191009/ourmid/pngtree-user-icon-png-image_1796659.jpg",
        'usrname' : "김철수",
        'usrpassword': 1234,
    }
    db.user.insert_one(userdoc1)
    db.user.insert_one(userdoc2)
    print('유저 정보 입력 완료')

    with open('./static/seed_data/user.json', 'r', encoding='UTF8') as f:
        data = json.load(f)
        db.users.insert_many(data)

def insert_notification():
    doc ={
        'notif_id' : 10,
        'url' : "../static/images/food.webp",
        #'gift-img' : "/img/launch.jpg",
        'giftname' : "10월 15일 점심",
        'giftmsg' : "밥먹자",
        'sndusrid' : 1,
        'sndusrname' : "김훈이",
        #'snd-usr-img' : "/img/usrimg.png",
        'rcvusrid' : 2,
        'rcvusrname' : "김영희",
        #'rcv-usr-img' : "/img/usrimg.png",
        'ischeck' : False,
        'isaccept' : False,
    }
    db.notification.insert_one(doc)
    print('완료 : ') 


def insert_git():
    print('완료 : ')
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
    insert_notification()
