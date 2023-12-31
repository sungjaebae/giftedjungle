from bson import ObjectId
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

from flask import Flask, render_template, jsonify, request
from flask.json.provider import JSONProvider
from routes.authentication import authentication
from routes.gift import gift, gift_list
from routes.notification import notification

import json
import sys

app = Flask(__name__)

client: MongoClient = MongoClient('localhost', 27017)
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

# 페이지, API 라우트를 담당자 별로 분리한다


@app.route('/')
def index():
    return gift_list()


app.register_blueprint(authentication)
app.register_blueprint(gift)
app.register_blueprint(notification)

if __name__ == '__main__':
    print(sys.executable)
    app.run('0.0.0.0', port=5000, debug=True)