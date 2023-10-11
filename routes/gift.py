from bson import ObjectId
from flask import Blueprint, render_template
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbgiftedjungle

gift = Blueprint('gift', __name__)


@gift.route('/gift')
def gift_list():
    categories = list(db.categories.find({}, {}))
    return render_template('index.html', categories=categories)  # 선물 목록 페이지


@gift.route('/gift/<id>')
def gift_detail(id):
    return render_template('gift.html')  # 선물 상세 페이지


@gift.route('/recipient')
def recipient():
    return render_template('recipient.html')  # 수령인 선택 페이지


@gift.route('/api/category/<id>')
def gifts_of_category(id):
    # 이 부분이 매우 중요합니다. category.name이 아니라 category["name"]으로 해야 합니다.
    category = db.categories.find_one({'_id': ObjectId(id)}, {})
    gifts = db.gifts.find({'category.name': category["name"]}, {})
    return list(gifts)
