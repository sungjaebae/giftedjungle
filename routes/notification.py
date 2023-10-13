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

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'id': payload['id']}, {})
        notifications = list(db.notifications.find(
            {"$or": [{"sender.id": user["id"], "is_deleted": False}, {"recipient.id": user["id"], "is_deleted": False}]}))
        # 알림 목록 페이지
        return render_template('notification_list.html', notifications=notifications, myid=user['id'])
    except jwt.ExpiredSignatureError:
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        return redirect("/login")


@notification.route('/notification/<notif_id>')
def notification_detail(notif_id):
    notificationdetail = db.notifications.find_one({'_id': ObjectId(notif_id)})
    # 알림 상세 페이지
    print(notificationdetail)
    return render_template('notification.html', notificationdetail=notificationdetail)


@notification.route('/process_accept', methods=['POST'])
def update_accept_received():
    notif_id = request.form["notif_id"]
    notification = db.notifications.find_one_and_update({'_id': ObjectId(notif_id)}, {
        '$set': {'is_read': True, 'is_deleted': True}})

    db.received_gifts.insert_one(
        {'gift': notification['gift'], 'notification': notification})
    return redirect('/received_gift')


@notification.route('/process_deny', methods=['POST'])
def update_refuse_received():
    notif_id = request.form["notif_id"]
    db.notifications.update_one({'_id': ObjectId(notif_id)}, {
        '$set': {'is_read': True, 'is_deleted': True}})

    return redirect('/notification')


@notification.route('/received_gift')
def received_gift():
    token_receive = request.cookies.get('mytoken')

    try:
        # token디코딩합니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'id': payload['id']}, {})
        received_gifts = list(db.received_gifts.find(
            {'notification.recipient.id': user['id']}))
        print(received_gifts[0])
        # 받은 선물함 페이지
        return render_template('received_gift.html', received_gifts=received_gifts)
    except jwt.ExpiredSignatureError:
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        return redirect("/login")
