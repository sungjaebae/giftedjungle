from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
import jwt
client: MongoClient = MongoClient('localhost', 27017)
db = client.dbgiftedjungle

gift = Blueprint('gift', __name__)
SECRET_KEY = 'JUNGLE'


@gift.route('/gift')
def gift_list():
    categories = list(db.categories.find({}, {}))
    return render_template('index.html', categories=categories)  # 선물 목록 페이지


@gift.route('/gift/<id>')
def gift_detail(id):
    token_receive = request.cookies.get('mytoken')

    try:
        # token디코딩합니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.users.find_one({'id': payload['id']}, {})
        gift = db.gifts.find_one({'_id': ObjectId(id)}, {})
        # 선물 상세 페이지
        return render_template('gift.html', gift=gift, sender=user)
    except jwt.ExpiredSignatureError:
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        return redirect("/login")


@gift.route('/recipient', methods=['POST'])
def recipient():
    message = request.form["message"]
    gift_id = request.form["gift_id"]
    sender_id = request.form["sender_id"]
    users = list(db.users.find({}, {}))
    # 수령인 선택 페이지
    return render_template('recipient.html', message=message, gift_id=gift_id, users=users, sender_id=sender_id)


@gift.route('/process_gift', methods=['POST'])
def process_gift():
    message = request.form["message"]
    gift_id = request.form["gift_id"]
    sender_id = request.form["sender_id"]
    recipient_id = request.form["recipient_id"]

    gift = db.gifts.find_one({'_id': ObjectId(gift_id)}, {})
    recipient = db.users.find_one({'_id': ObjectId(recipient_id)}, {})
    sender = db.users.find_one({'_id': ObjectId(sender_id)}, {})
    db.notifications.insert_one(
        {"gift": gift, "recipient": recipient, "sender": sender, "message": message, "is_read": False, "is_deleted": False})

    return redirect('/')
    # return redirect(url_for('index')) 이렇게 하는걸 추천한다고 한다


@gift.route('/api/category/<id>')
def gifts_of_category(id):
    # category.name이 아니라 category["name"]으로 해야 한다
    category = db.categories.find_one({'_id': ObjectId(id)}, {})
    gifts = db.gifts.find({'category.name': category["name"]}, {})
    gifts = list(gifts)
    return gifts
