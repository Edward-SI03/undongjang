from flask import Flask, render_template, jsonify, request, Blueprint, url_for
# 회원가입시 pw 암호화 해싱
import hashlib

# jwt 토큰 생성
import jwt

# 시간 라이브러리
import datetime
# 토큰을 만들때 유효기간을 설정하기 위해서 서버시간을 가져와서 그로부터 얼마만큼 유효하게 설정하기 위해 필요
from datetime import datetime, timedelta

######## bson 패키지 설치 필요! ########
#pymongo에서 _id의 ObjectId를 사용하기 위해 필요
from bson.objectid import ObjectId

# 파이몽고 라이브러리
from pymongo import MongoClient

SECRET_KEY = "sparta"

app = Flask(__name__)

# client = MongoClient('localhost', 27017)
client = MongoClient('15.165.158.21', 27017, username="test", password="test")
db = client.playGround


# 메인 페이지 이동
@app.route('/')
def home():
    # print("hi")
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"idenfier": payload["idenfier"]})
        return render_template('main.html', userid=user_info["idenfier"])
    else:
        return render_template('main.html')

# 작성된 글 불러오기
@app.route('/getpost', methods=['GET'])
def show_postlist():
    posts = list(db.postbox.find({}))
    # print(posts)
    for post in posts:
        post["_id"] = str(post["_id"])
        # print(post["_id"])
    return jsonify({'all_post': posts, "msg":"가져오기 성공"})

# 세부 내용 보기(모달)
@app.route('/modal', methods=['POST'])
def show_modal():
    print("모달열기")
    post_id_receive = request.form["post_id_give"]

    # ObjectId 로 데이터 찾을때 bson 패키지 설치 필요
    post = db.postbox.find_one({'_id': ObjectId(post_id_receive)})
    # print(post['file'])
    # print(post)

    post["_id"] = str(post["_id"])
    # print(post["_id"])

    data = {
        'postid': post["_id"],
        'userid': post['userid'],
        'placeName': post['placeName'],
        'location': post['location'],
        'workout': post['workout'],
        'address': post['address'],
        'comment': post['comment'],
        'file': post['file'],
    }

    return jsonify({
        'result': {
            'success': 'true',
            'message': 'modal 가져오기 성공',
            'data': data,
        }
    })

# 게시물 삭제(모달)
@app.route('/delpost', methods=['POST'])
def del_post():
    print("게시물 삭제")
    post_id_receive = request.form["post_id_give"]

    db.postbox.delete_one({'_id': ObjectId(post_id_receive)})

    return jsonify({
        'result': {
            'success': 'true',
            'msg': '게시물이 삭제 되었습니다.',
        }
    })


# 글작성 페이지 이동
@app.route('/write')
def write():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"idenfier": payload["idenfier"]})
        return render_template('writing.html', userid=user_info["idenfier"])
    else:
        # return jsonify({'result': 'fail', 'msg': '로그인 후 글 작성 가능합니다.'})
        return render_template('main.html', msg="로그인 후 글 작성 가능합니다.")


# 글 작성(디비저장)
@app.route('/post', methods=['POST'])
def save_post():
    try:
        userid_receive = request.form["userid_give"]
        placeName_receive = request.form["placeName_give"]
        location_receive = request.form["location_give"]
        workout_receive = request.form["workout_give"]
        address_receive = request.form["address_give"]
        comment_receive = request.form["comment_give"]
        file_receive = request.files["file_give"]

        file = file_receive

        extension = file.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

        filename = f'file-{mytime}'

        save_to = f'static/postimg/{filename}.{extension}'
        file.save(save_to)

        doc = {
            "userid": userid_receive,
            'placeName': placeName_receive,
            'location': location_receive,
            'workout': workout_receive,
            'address': address_receive,
            'comment': comment_receive,
            'file': f'{filename}.{extension}'
        }
        db.postbox.insert_one(doc)

        return jsonify({'msg': '저장완료'})

    # except를 한 이유는 사진 파일이 없을경우 디비에 아에 빈 데이터로 저장이 되어서 
    # ""로라도 저장하면 나중에 앞에서 데이터 처리하기 편해서 만든건데 이방법이 좋은건지는 모르겠네요
    except KeyError:
        userid_receive = request.form["userid_give"]
        placeName_receive = request.form["placeName_give"]
        location_receive = request.form["location_give"]
        workout_receive = request.form["workout_give"]
        address_receive = request.form["address_give"]
        comment_receive = request.form["comment_give"]

        doc = {
            "userid": userid_receive,
            'placeName': placeName_receive,
            'location': location_receive,
            'workout': workout_receive,
            'address': address_receive,
            'comment': comment_receive,
            'file': "",
        }
        db.postbox.insert_one(doc)

        return jsonify({'msg': '저장완료'})


# 로그인 페이지 이동
@app.route('/login')
def loginPage():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"idenfier": payload["idenfier"]})
        return render_template('main.html', userid=user_info["idenfier"])
    else:
        return render_template('login.html')


# user 사용자 로그인 여부 확인 api
@app.route('/islogin', methods=['POST'])
def checkcookie():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        return jsonify({
            'result': {'success': 'true'}
        })
    else:
        return jsonify({
            'result': {'success': 'false'}
        })


# 로그인 시도
@app.route('/login', methods=['POST'])
def login():
    idenfier_receive = request.form['id_give']
    password_receive = request.form['pw_give']

    # 받은 비밀번호를 암호 알고리즘화 하여 해싱(관리자도 볼수 없게 암호화)
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # id와 해싱된 pw를 디비에서 찾는다
    result = db.users.find_one({'idenfier': idenfier_receive, 'password': password_hash}, {'_id': False})

    # 디비에 일치하는 정보가 있다면 로그인토큰을 만들것이고 없어서 None이라면 fail 결과가 나옴
    if result is not None:
        payload = {
            'idenfier': idenfier_receive,
            # 토큰의 유효기간을 설정(지금은 24시간 유효기간으로 설정해놈)(시간지나면 로그인이 풀림)
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        # SECRET_KEY를 임의로 설정하여 SECRET_KEY를 가지고 알고리즘 암호화 하여 토큰을 만듬(로컬서버때 사용)
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # 로컬 서버가 아닌 ec2 서버에 배포시 로그인 오류 문제 발생
        # python3에서는 기본이 utf-8이기 때문에 굳이 decode를 사용할 필요가 없다고 함
        # token 생성 코드에 .decode(‘utf-8’)을 붙여 스트링 값으로 바꿔서 해결(Local서버에서 실행 시, decode() 함수 제거해야 동작됨)
        # 아래는 ec2 서버에 올릴때 사용 롤컬서버는 .decode(‘utf-8’) 미사용
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # 토큰을 만들면 클라이언트쪽으로 보내줌
        return jsonify({'result': 'success', 'msg': '로그인 성공.', 'token': token, })
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 페이지 이동
@app.route('/signup')
def signup():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"idenfier": payload["idenfier"]})
        return render_template('main.html', userid=user_info["idenfier"])
    else:
        return render_template('signup.html')


# 회원가입
@app.route('/users', methods=['POST'])
def createUser():
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']
    idenfier_receive = request.form['idenfier_give']
    password_receive = request.form['password_give']
    email_receive = request.form['email_give']
    number_receive = request.form['number_give']
    address_receive = request.form['address_give']

    userid = db.users.find_one({'idenfier':idenfier_receive},{"_id" : False})

    if userid == None :
        # 받은 비밀번호를 암호 알고리즘화 하여 해싱(관리자도 볼수 없게 암호화)
        password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

        doc = {
            'name': name_receive,
            'nick': nick_receive,
            'idenfier': idenfier_receive,
            'password': password_hash,
            'email': email_receive,
            'number': number_receive,
            'address': address_receive,

        }
        db.users.insert_one(doc)

        return jsonify({'result': 'success', 'msg': '회원가입 완료'})
    else:
        return jsonify({'result': 'false', 'msg': '중복된 아이디 입니다.'})


  # 회원정보 수정 페이지
@app.route('/modify/<idenfier>')
def user(idenfier):

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        status = (idenfier == payload["idenfier"])  # 내 프로필이면 True, 다른 사람 프로필 페이지면 False

        user_info = db.users.find_one({"idenfier": idenfier}, {"_id": False})

        return render_template('modify.html', userid=user_info,  status=status)

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


# 회원정보수정하기
@app.route('/update_user', methods=['POST'])
def updateUser():
    name_receive = request.form['name_give']
    nick_receive = request.form['nick_give']
    idenfier_receive = request.form['idenfier_give']
    # password_receive = request.form['password_give']
    email_receive = request.form['email_give']
    number_receive = request.form['number_give']
    address_receive = request.form['address_give']

    # 받은 비밀번호를 암호 알고리즘화 하여 해싱(관리자도 볼수 없게 암호화)
    # password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    db.users.update_one({'idenfier': idenfier_receive}, {'$set': {'name': name_receive, 'nick': nick_receive, 'idenfier': idenfier_receive, 'email': email_receive,'number': number_receive, 'address': address_receive}})

    return jsonify({'result': 'success', 'msg': '회원수정 완료'})

# 회원정보 삭제하기
@app.route('/delete_user', methods=['POST'])
def deleteUser():
    idenfier_receive = request.form['idenfier_give']

    db.users.delete_one({'idenfier': idenfier_receive})

    return jsonify({'result': 'success', 'msg': '회원탈퇴 완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
