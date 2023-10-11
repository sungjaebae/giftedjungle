from bson import ObjectId
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider

import json
import sys

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class CustomJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


app.json = CustomJSONProvider(app)

# 페이지 라우트. 총 7개의 페이지로 구성된다


@app.route('/')
def index():
    return render_template('index.html')  # 선물 목록 페이지


@app.route('/login')
def login():
    return render_template('login.html')  # 로그인 페이지


@app.route('/gift/<id>')
def gift(id):
    return render_template('gift.html')  # 선물 상세 페이지


@app.route('/recipient')
def recipient():
    return render_template('recipient.html')  # 수령인 선택 페이지


@app.route('/notification')
def notification_list():
    return render_template('notification_list.html')  # 알림 목록 페이지


@app.route('/notification/<id>')
def notification():
    return render_template('notification.html')  # 알림 상세 페이지


@app.route('/received_gift')
def received_gift():
    return render_template('received_gift.html')  # 받은 선물함 페이지

# API 라우트. 페이지의 구현에 따라 추가한다


if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)
