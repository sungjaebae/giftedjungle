import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient  

client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle
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
        'notif-id' : 10,
        'gift-img' : "/img/launch.jpg",
        'gift-name' : "10월 15일 점심",
        'gift-msg' : "밥먹자",
        'snd-usr-id' : 1,
        'snd-usr-name' : "김훈이",
        'snd-usr-img' : "/img/usrimg.png",
        'rcv-usr-id' : 2,
        'rcv-usr-name' : "김영희",
        'rcv-usrimg' : "/img/usrimg.png",
        'ischeck' : False,
        'isaccept' : False,
    }
    db.notification.insert_one(doc)
    print('완료 : ')

def insert_received():
    receiveddoc={
        'id' : 10,
        #'giftimg' : "C:\Users\푸린\Desktop\activity\jungle\0주차\giftedjungle\templates\img\launch.jpeg",
        'giftname' : "10월 15일 점심",
        'giftmsg' : "밥먹자",
        'sentusrid' : 1,
        'sentusrname' : "김훈이",
        #'sentusrimg' : "C:\Users\푸린\Desktop\activity\jungle\0주차\giftedjungle\templates\img\usrimg.png",
        'receiptionusrid' : 2,
        'receiptionusrname' : "김영희",
        #'receiptionusrimg' : "C:\Users\푸린\Desktop\activity\jungle\0주차\giftedjungle\templates\img\usrimg.png",
        'ischeck' : False,
        'isaccept' : False,
    }
    db.received.insert_one(receiveddoc)
    print('받은선물 입력 완료 : ')
def drop_all():
    pass


if __name__ == '__main__':
    drop_all()
    insert_user()
    insert_gift()
    insert_received()
