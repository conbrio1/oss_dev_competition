from flask import Blueprint, url_for, current_app, Response, render_template
from werkzeug.utils import redirect
import cv2
import datetime

from .. import db

# from ..models import Video

bp = Blueprint("main", __name__, url_prefix="/")
secondsForNewVideo = 20

@bp.route("/")
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M:%S")
    templateData = {"title": "Image Streaming", "time": timeString}
    return render_template("index.html", **templateData)


def compareSeconds(t1, t2, secondsLimit):
    """t1, t2 should be datetime.datetime class \n
    t2 should be the time measured later than t1"""
    assert(type(t1) == type(t2) == datetime.datetime and t2 > t1)
    assert(secondsLimit > 0)

    retval = False
    if (t2-t1).total_seconds() > secondsLimit:
        retval = True

    return retval


def videoWriterFactory(now, codec=1482049860, fps=30, width=640, height=480):
    """param(now) should be datetime.datetime class"""
    assert(type(now) == datetime.datetime)

    return cv2.VideoWriter('../resource/out_{time}.avi'.format(time=now.strftime("%Y-%m-%d_%H:%M:%S")), codec, fps, (width, height))


def gen_frames():
    cap = cv2.VideoCapture(0)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print('프레임 너비: %d, 프레임 높이: %d, 초당 프레임 수: %d' %(width, height, fps))

    codec = cv2.VideoWriter_fourcc(*'DIVX')

    t1 = datetime.datetime.now()
    out = videoWriterFactory(t1)

    while cap.isOpened():
        t2 = datetime.datetime.now()
        if compareSeconds(t1, t2, secondsForNewVideo):
            out.release()
            out = videoWriterFactory(t2)
            t1 = t2

        ret, image = cap.read()
        out.write(image)
        
        ret, buffer = cv2.imencode(".jpg", image)
        frame = buffer.tobytes()
        
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

    cap.release()
    out.release()


@bp.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
