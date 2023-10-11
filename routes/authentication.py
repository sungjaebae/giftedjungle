from flask import Blueprint, render_template

authentication = Blueprint('authentication', __name__)


@authentication.route('/login')
def login():
    return render_template('login.html')  # 로그인 페이지
