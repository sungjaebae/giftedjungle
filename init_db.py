from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle
#db.user.deleteMany({})
#db.notification.deleteMany({})

def insert_user():
    userdoc1={
        'usrid' : 1,
        'usrimg' : "https://png.pngtree.com/png-vector/20191009/ourmid/pngtree-user-icon-png-image_1796659.jpg",
        'usrname' : "김훈이",
        'usrpassword': 1234,
    }

    userdoc2={
        'usrid' : 2,
        'usrimg' : "https://png.pngtree.com/png-vector/20191009/ourmid/pngtree-user-icon-png-image_1796659.jpg",
        'usrname' : "김철수",
        'usrpassword': 1234,
    }
    db.user.insert_one(userdoc1)
    db.user.insert_one(userdoc2)
    print('유저 정보 입력 완료')


def insert_gift():
    doc ={
        'giftimg' : "https://previews.123rf.com/images/ksuperksu/ksuperksu1601/ksuperksu160100007/51544658-%EB%82%B4-%EC%A0%90%EC%8B%AC-%EC%8B%9D%EC%82%AC-%EB%A7%9B%EC%9E%88%EB%8A%94-%EC%8B%A0%EC%84%A0%ED%95%9C-%EC%9D%8C%EC%8B%9D%EC%9D%98-%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8-%EC%8F%B4-%EC%8B%9D%EC%82%AC%EC%9D%98-%EC%A1%B0%EC%84%B1%EC%9E%85%EB%8B%88%EB%8B%A4-%EB%B3%91-%EC%9D%8C%EB%A3%8C-%EC%83%8C%EB%93%9C%EC%9C%84%EC%B9%98-%EC%83%90%EB%9F%AC%EB%93%9C-%EC%82%AC%EA%B3%BC-%EC%B4%88%EC%BD%9C%EB%A6%BF-%EC%83%8C%EB%93%9C%EC%9C%84%EC%B9%98-%EC%BF%A0%ED%82%A4%EC%99%80-%EB%B2%84%ED%84%B0-%EC%83%9D-%EA%B3%BC%EC%9E%90%EC%9E%85%EB%8B%88%EB%8B%A4.jpg",
        'giftname' : "10월 15일 점심",
        'giftmsg' : "밥먹자",
        'sentusr' : 1,
        'receiptionusr' : 2,
        'ischeck' : 1,
        'isaccept' : 1,
    }
    db.notification.insert_one(doc)
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
