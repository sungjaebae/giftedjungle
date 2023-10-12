from flask import Blueprint, render_template, jsonify
from bson import ObjectId
from pymongo import MongoClient,ReturnDocument

from flask import Flask, render_template, jsonify, request,redirect,url_for
from flask.json.provider import JSONProvider

import json
import sys


notification = Blueprint('notification', __name__)
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


@notification.route('/notification')
def notification_list():
    notifications = list(db.notification.find({}))
    # 알림 목록 페이지
    return render_template('notification_list.html', notifications=notifications)


@notification.route('/notification/<notif_id>')
def notification_detail(notif_id):
    notificationdetail = db.notification.find_one({'notif_id':int(notif_id)})
    return render_template('notification.html', notificationdetail = notificationdetail)  # 알림 상세 페이지

@notification.route('/notification/accept/<notif_id>')
def update_accept_received(notif_id):
    db.notification.find_one_and_update({'notif_id':int(notif_id)}, {'$set':{'ischeck':True}})
    db.notification.find_one_and_update({'notif_id':int(notif_id)}, {'$set':{'isaccept':True}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'notif_id':int(notif_id)},{'_id':0})
    print(returnnotification)
    db.received.insert_one(returnnotification)
    return redirect(url_for('notification.received_gift'))
    #return render_template('received_gift.html')

@notification.route('/notification/refuse/<notif_id>')
def update_refuse_received(notif_id):
    db.notification.find_one_and_update({'notif_id':int(notif_id)}, {'$set':{'ischeck':True}})
    db.notification.find_one_and_update({'notif_id':int(notif_id)}, {'$set':{'isaccept':False}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'notif_id':int(notif_id)},{'_id':0})
    print(returnnotification)
    # db.received.insert_one(returnnotification)
    
    notifications = list(db.notification.find({})) 
    #return redirect(url_for('notification.notification_list'))
    return render_template('notification_list.html', notifications = notifications)

@notification.route('/received_gift')
def received_gift():
    received = list(db.received.find({}))
    return render_template('received_gift.html', received=received)  # 받은 선물함 페이지