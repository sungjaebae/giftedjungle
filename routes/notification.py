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
    return render_template('notification_list.html', notifications = notifications)    # 알림 목록 페이지


@notification.route('/notification/<id>')
def notification_detail(id):
    notificationdetail = db.notification.find_one({'id':id})
    return render_template('notification.html', notificationdetail = notificationdetail)  # 알림 상세 페이지

@notification.route('/notification/accept/<id>')
def update_accept_received(id):
    print("id : ", id)
    db.notification.find_one_and_update({'id':10}, {'$set':{'ischeck':True}})
    db.notification.find_one_and_update({'id':10}, {'$set':{'isaccept':True}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'id':10},{'_id':0})
    # if(returnnotification==None):
    #     print("받은 선물함 업데이트 실패!")
    #     return
    # else:
    print(returnnotification)
    db.received.insert_one(returnnotification)
    return redirect(url_for('notification.received_gift'))
    #return render_template('received_gift.html')

@notification.route('/notification/refuse/<id>')
def update_refuse_received(id):
    print("id : ", id)
    db.notification.find_one_and_update({'id':10}, {'$set':{'ischeck':True}})
    db.notification.find_one_and_update({'id':10}, {'$set':{'isaccept':False}}, return_document=ReturnDocument.AFTER )
    returnnotification= db.notification.find_one({'id':10},{'_id':0})
    # if(returnnotification==None):
    #     print("받은 선물함 업데이트 실패!")
    #     return
    # else:
    print(returnnotification)
    db.received.insert_one(returnnotification)
    
    notifications = list(db.notification.find({})) 
    #return redirect(url_for('notification.notification_list'))
    return render_template('notification_list.html', notifications = notifications)

@notification.route('/received_gift')
def received_gift():
    received = list(db.received.find({}))
    return render_template('received_gift.html', received=received)  # 받은 선물함 페이지
