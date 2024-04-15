from flask import Blueprint,Flask, render_template, Response
import cv2

videoGroup2API = Blueprint('videoGroup2API', __name__)

camera1 = cv2.VideoCapture("rtsp://root:kiot!@34@223.171.66.131:1554/axis-media/media.amp")#옥녀봉
camera2 = cv2.VideoCapture("rtsp://root:kiot!@34@223.171.66.133:1554/axis-media/media.amp")#칠곡 숲체원


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


@videoGroup2API.route("/")
def video_root():
    return render_template('videoGroup2.html')


@videoGroup2API.route("/video_feed1")
def video_feed1():
    return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@videoGroup2API.route("/video_feed2")
def video_feed2():
    return Response(gen_frames2(), mimetype='multipart/x-mixed-replace; boundary=frame')
