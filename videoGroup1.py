from flask import Blueprint, Flask, render_template, Response
import cv2

videoGroup1API = Blueprint('videoGroup1API', __name__)

camera1 = cv2.VideoCapture("rtsp://admin:kiot!@34@121.182.188.74:18554/cam/realmonitor?channel=1&subtype=0")  # 사문진
camera2 = cv2.VideoCapture("rtsp://root:kiot!@34@223.171.66.128:1554/axis-media/media.amp")  # 장성숲체원 서버실


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


@videoGroup1API.route("/")
def video_root():
    print('root')
    return render_template('videoGroup1.html')


@videoGroup1API.route("/video_feed1")
def video_feed1():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@videoGroup1API.route("/video_feed2")
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')
