from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient

import jwt
from datetime import datetime, timedelta
authentication = Blueprint('authentication', __name__)
SECRET_KEY = 'JUNGLE'

client: MongoClient = MongoClient('localhost', 27017)
db = client.dbgiftedjungle


@authentication.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id_recieve = request.form['id_give']
        pw_recieve = request.form['pw_give']

        result = db.users.find_one({'id': id_recieve, 'pw': pw_recieve})

        # JWT 토큰 발급
        if result is not None:
            # JWT 토큰 생성
            payload = {
                'id': id_recieve,
                'exp': datetime.utcnow() + timedelta(days=2)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'result': 'success', 'token': token})
        else:
            return jsonify({'result': 'fail', 'msg': '아이디 또는 비밀번호가 틀렸습니다'})
    else:
        return render_template('login.html')  # 로그인 페이지


@authentication.route('/sign')
def signup():
    return render_template('sign.html')


@authentication.route("/sign", methods=["POST"])  # 회원가입
def join():
    # 사용자 정보 받아오기
    name_recieve = request.form["name_give"]
    id_recieve = request.form["id_give"]
    pw_recieve = request.form["pw_give"]

    result = db.users.find_one({'id': id_recieve})

    if result is not None:
        return jsonify({'result': 'fail', 'msg': 'ID 중복확인을 해주세요'})
    else:
        db.users.insert_one(
            {'id': id_recieve, 'pw': pw_recieve, 'name': name_recieve})

        return jsonify({'result': 'success'})
    
@authentication.route('/sign/check', methods =["POST"])
def checkID():
   id_recieve = request.form["id_give"]
   result = db.users.find_one({'id': id_recieve})
   if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 사용중인 ID입니다'})
   else:
        return jsonify({'result': 'success'})


@authentication.route('/mypage', methods=["GET"])  # 마이페이지read
def mypage():
    token_receive = request.cookies.get('mytoken')

    try:
        # token디코딩합니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.users.find_one({'id': payload['id']}, {'_id': 0})

        return render_template("mypage.html", user_info=userinfo)
    except jwt.ExpiredSignatureError:
        return redirect("/login")
    except jwt.exceptions.DecodeError:
        return redirect("/login")


@authentication.route('/mypage/edit', methods=['POST'])
def modify():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

    pw_recieve = request.form['pw_give']

    db.users.update_many({"id": payload["id"]}, {'$set': {'pw': pw_recieve}})

    return jsonify({"result": "success", "msg": "회원정보가 수정되었습니다."})


@authentication.route('/mypage/logout', methods=['POST'])
def logout():
    # 클라이언트에서는 토큰을 삭제하고 세션을 무효화할 수 있습니다.
    # 여기서는 토큰을 만료시키는 방법을 제시합니다.
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        # 토큰을 만료시킴
        payload['exp'] = datetime.utcnow() - timedelta(hours=1)

        # 새로운 토큰 생성
        new_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # 클라이언트에게 새로운 토큰을 전달하여 현재 토큰을 무효화
        response = jsonify({'result': 'success', 'msg': '로그아웃 되었습니다.'})
        # response.set_cookie('mytoken', new_token, httponly=True)
        response.delete_cookie('mytoken')

        return response
    except jwt.ExpiredSignatureError:
        response = jsonify({'result': 'fail', 'msg': '토큰이 이미 만료되었습니다.'})
        return response
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '토큰 디코딩 오류'})
    
@authentication.route('/mypage/delete', methods=["POST"])
def delete():
    token_receive = request.cookies.get('mytoken')    
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    response = jsonify({'result':'success', 'msg': '회원탈퇴 되었습니다.'})
    response.delete_cookie('mytoken')
    db.users.delete_one({"id":payload["id"]})
    return response
