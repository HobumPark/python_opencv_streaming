import os

from flask import Flask, render_template, Response, request, url_for, session
from werkzeug.utils import redirect
from datetime import timedelta

from videoGroup1 import videoGroup1API
from videoGroup2 import videoGroup2API
from videoGroup3 import videoGroup3API
from models import db
from models import User
from sqlalchemy import insert
from sqlalchemy.sql import text
import cv2

app = Flask(__name__)

app.register_blueprint(videoGroup1API, url_prefix="/video_group1")
app.register_blueprint(videoGroup2API, url_prefix="/video_group2")
app.register_blueprint(videoGroup3API, url_prefix="/video_group3")

# rtsp://admin:kiot!@34@121.182.188.74:18554/cam/realmonitor?channel=1&subtype=0 - 사문진
# rtsp://root:kiot!@34@223.171.66.128:1554/axis-media/media.amp - 장성숲체원 서버실
# rtsp://root:kiot!@34@223.171.66.131:1554/axis-media/media.amp - 옥녀봉
# rtsp://root:kiot!@34@223.171.66.133:1554/axis-media/media.amp - 칠곡 숲체원
# rtsp://root:kiot!@34@223.171.66.135:1554/axis-media/media.amp - 두산리
# rtsp://root:kiot!@34@223.171.66.142:1554/axis-media/media.amp - 청도 숲체원 시설 입구
# rtsp://root:kiot!@34@223.171.66.143:1554/axis-media/media.amp - 장성 치유의 숲
# rtsp://root:kiot!@34@223.171.66.145:1554/axis-media/media.amp - 대관령 치유의 숲
# rtsp://root:kiot!@34@223.171.128.30:1554/axis-media/media.amp - 우이천
# rtsp://root:kiot!@34@223.171.128.31:1554/axis-media/media.amp - 도봉천
# rtsp://root:kiot!@34@223.171.128.32:1554/axis-media/media.amp - 중랑천

# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()


@app.route('/')
def index():
    print('root')
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    print('login request!')

    id = request.form['id']
    pw = request.form['pw']
    print(id)
    print(pw)

    result = db.session.query(User).all()
    print(result)
    print('read request!')
    for row in result:
        if row.userid == id and row.password == pw:
            print('아이디,패스워드 일치!')
            print('로그인 성공')
            session['userid'] = id
            app.permanent_session_lifetime = timedelta(minutes=1)#세션 유지기간 1분
            return redirect(url_for('videoGroup3API.video_root'))
        #print(row.userid)
        #print(row.password)

    return redirect(url_for('index'))
    # return render_template('test.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    print('register request!')
    user = User(userid='manager', password='1234')
    db.session.add(user)
    db.session.commit()
    return "register"


@app.route('/read', methods=['POST', 'GET'])
def read():
    # user = User.query.all()
    result = db.session.query(User).all()
    print(result)
    print('read request!')
    for row in result:
        print(row.userid)
        print(row.password)

    return "read"


if __name__ == "__main__":
    app.run()
