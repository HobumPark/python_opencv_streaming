import math
import string

from flask import Blueprint, Flask, render_template, Response, request, session, url_for
import cv2
from werkzeug.utils import redirect

videoGroup3API = Blueprint('videoGroup3API', __name__)

camera1 = cv2.VideoCapture("rtsp://root:kiot!@34@223.171.66.131:1554/axis-media/media.amp")  # 옥녀봉
camera2 = cv2.VideoCapture("rtsp://root:kiot!@34@223.171.66.133:1554/axis-media/media.amp")  # 칠곡 숲체원


def gen_frames(input):
    camera = cv2.VideoCapture(input)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_frames1():
    while True:
        success, frame = camera1.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_frames2():
    while True:
        success, frame = camera2.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@videoGroup3API.route("/")
def video_root():
    if 'userid' not in session:
        print('not exist userid')
        return redirect(url_for('index'))

    post_per_page = 3
    video_per_page = 3
    current_page = request.args.get("page", 1, type=int)

    post_list = ['게시글1', '게시글2', '게시글3', '게시글4', '게시글5', '게시글6', '게시글7', '게시글8', '게시글9', '게시글10']
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
    video_list = [
                  'rtsp://root:kiot!@34@223.171.66.128:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.129:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.130:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.131:1554/axis-media/media.amp',
                  #'rtsp://root:kiot!@34@223.171.66.132:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.133:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.134:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.135:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.136:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.139:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.141:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.142:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.143:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.66.145:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.128.30:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.128.31:1554/axis-media/media.amp',
                  'rtsp://root:kiot!@34@223.171.128.32:1554/axis-media/media.amp'
                ]
    # post_len = len(post_list)
    video_len = len(video_list)
    # page_len = math.ceil(post_len / post_per_page)
    page_len = math.ceil(video_len / video_per_page)

    # start_index = (current_page - 1) * post_per_page
    start_index = (current_page - 1) * video_per_page

    # end_index = start_index + post_per_page
    if current_page == page_len:
        end_index = video_len - 1
    else:
        end_index = start_index + video_per_page

    print('start_index:'+str(start_index))
    print('end_index:'+str(end_index))

    return render_template('videoGroup3.html', video_len=video_len, video_per_page=video_per_page, page_len=page_len,
                           current_page=current_page, video_list=video_list, start_index=start_index,
                           end_index=end_index)


@videoGroup3API.route("/video_feed")
def video_feed():
    video_src = request.args.get("video_src", 1, type=str)
    print(video_src)
    return Response(gen_frames(video_src), mimetype='multipart/x-mixed-replace; boundary=frame')


@videoGroup3API.route("/video_feed1")
def video_feed1():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@videoGroup3API.route("/video_feed2")
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')
