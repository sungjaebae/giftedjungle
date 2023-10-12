from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for
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
    gift = db.gifts.find_one({'_id': ObjectId(id)}, {})
    return render_template('gift.html', gift=gift)  # 선물 상세 페이지


@gift.route('/recipient', methods=['POST'])
def recipient():
    message = request.form["message"]
    gift_id = request.form["gift_id"]
    users = list(db.users.find({}, {}))
    # 수령인 선택 페이지
    return render_template('recipient.html', message=message, gift_id=gift_id, users=users)


@gift.route('/process_gift', methods=['POST'])
def process_gift():
    message = request.form["message"]
    gift_id = request.form["gift_id"]
    recipient_id = request.form["recipient_id"]
    return redirect('/')
    # return redirect(url_for('index')) 이렇게 하는걸 추천한다고 한다


@gift.route('/api/category/<id>')
def gifts_of_category(id):
    # category.name이 아니라 category["name"]으로 해야 한다
    category = db.categories.find_one({'_id': ObjectId(id)}, {})
    gifts = db.gifts.find({'category.name': category["name"]}, {})
    gifts = list(gifts)
    return gifts
