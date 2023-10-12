from flask import Blueprint, render_template, jsonify
from bson import ObjectId
from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys


notification = Blueprint('notification', __name__)
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


@notification.route('/notification')
def notification_list():

    myid = request.args.get("myid", 0)

    notifications = list(db.notification.find({"receiptionusr": myid}))

    # let giftname = notification['giftname']
    # let giftmsg = notification['giftmsg']
    # let sentusr = notification['sentusr']
    # let receiptionusr = notification['receiptionusr']
    # let ischeck = notification['ischeck']
    #       let isaccept = notification['isaccept']

    # notifications = list(db.notification.find({"$or":[
    #     {"sentusr" : myid},
    #     {"receiptionusr" : myid}
    # ]}))

    notifications = list(db.notification.find({}))
    # 알림 목록 페이지
    return render_template('notification_list.html', notifications=notifications)


@notification.route('/notification/<id>')
def notification_detail():
    return render_template('notification.html')  # 알림 상세 페이지


@notification.route('/received_gift')
def received_gift():
    return render_template('received_gift.html')  # 받은 선물함 페이지
