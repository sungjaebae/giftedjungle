from flask import Blueprint, render_template

notification = Blueprint('notification', __name__)


@notification.route('/notification')
def notification_list():
    return render_template('notification_list.html')  # 알림 목록 페이지


@notification.route('/notification/<id>')
def notification_detail():
    return render_template('notification.html')  # 알림 상세 페이지


@notification.route('/received_gift')
def received_gift():
    return render_template('received_gift.html')  # 받은 선물함 페이지
