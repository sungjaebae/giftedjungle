from flask import Blueprint, render_template

gift = Blueprint('gift', __name__)


@gift.route('/gift')
def gift_list():
    return render_template('index.html')  # 선물 목록 페이지


@gift.route('/gift/<id>')
def gift_detail(id):
    return render_template('gift.html')  # 선물 상세 페이지


@gift.route('/recipient')
def recipient():
    return render_template('recipient.html')  # 수령인 선택 페이지
