from flask import Flask, render_template, Response, request
import cv2
import datetime
import time
from lineorder_qty import lineorder_qty




app = Flask(__name__)
camera = cv2.VideoCapture(0)

now = datetime.datetime.today().strftime("%Y-%m-%d_%H%M%S")

@app.route('/takeimage', methods = ['POST'])
def takeimage():
    global  users_id
    users_id = request.form['name']    #從Flask帶入users_id
    print(f"{users_id}({now})")
    _, frame = camera.read()
    h, w, c = frame.shape
    frame = frame[0:h, int(w / 2 - h / 2):int(w / 2 + h / 2)]
    cv2.imwrite(f"./image/{users_id}({now}.jpg", frame)
    # cv2.imshow(f"./image/{c_id}({now}.jpg", frame)
    # camera.release()
    return Response(status = 200)

def gen_frames():
    while True:
        ret, frame = camera.read()
        h, w, c = frame.shape
        frame = frame[0:h, int(w/2-h/2):int(w/2+h/2)]
        # cv2.imwrite(f'./image/frame{now}.jpg', frame)  # save frame as JPEG file
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=["GET", "POST"])
def index():
    lineorder_qty()
    return render_template('index.html', show_qty = lineorder_qty())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')