from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient, ReturnDocument
import jwt


notification = Blueprint('notification', __name__)
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle
SECRET_KEY = 'JUNGLE'


@notification.route('/notification')
def notification_list():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user = db.users.find_one({'id': payload['id']}, {})
    notifications = list(db.notifications.find({}))
    print(notifications)
    # 알림 목록 페이지
    return render_template('notification_list.html', notifications=notifications, myid=user)


@notification.route('/notification/<notif_id>')
def notification_detail(notif_id):
    notificationdetail = db.notifications.find_one({'_id':notif_id})
    return render_template('notification.html', notificationdetail = notificationdetail)  # 알림 상세 페이지

@notification.route('/notification/accept/<notif_id>')
def update_accept_received(notif_id):
    db.notification.find_one_and_update({'_id':notif_id}, {'$set':{'is_read':True}})
    db.notification.find_one_and_update({'_id':notif_id}, {'$set':{'is_deleted':False}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'_id':notif_id},{'_id':0})
    print(returnnotification)
    db.received.insert_one(returnnotification)
    return redirect(url_for('notification.received_gift'))
    #return render_template('received_gift.html')

@notification.route('/notification/refuse/<notif_id>')
def update_refuse_received(notif_id):
    db.notification.find_one_and_update({'_id':notif_id}, {'$set':{'is_read':True}})
    db.notification.find_one_and_update({'_id':notif_id}, {'$set':{'is_deleted':False}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'_id':notif_id},{'_id':0})
    print(returnnotification)
    # db.received.insert_one(returnnotification)
    
    notifications = list(db.notification.find({})) 
    #return redirect(url_for('notification.notification_list'))
    return render_template('notification_list.html', notifications = notifications)

@notification.route('/received_gift')
def received_gift():
    received = list(db.notification.find({'$and': [{'is_read': True}, {'is_deleted':False}]}))
    return render_template('received_gift.html', received=received)  # 받은 선물함 페이지