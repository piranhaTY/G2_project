from flask import Flask, render_template, Response, request, redirect
import cv2
import mysql.connector
import datetime
import time
from lineorder_qty import lineorder_qty
from caculate import sql_order


app = Flask(__name__)
camera = cv2.VideoCapture(0)




@app.route('/commit_order', methods = ["GET", "POST"])
def commit_order():
    try:
        connection = mysql.connector.connect(host="35.221.178.251",
                                             database="project",
                                             user="root",
                                             password="cfi10202")
        mycursor = connection.cursor()

        add_details = ("INSERT INTO details "
                       "(users_id, products_id, date, quantity, price, details_cal) "
                       "VALUES (%s, %s, %s, %s, %s, %s)")

        for i in sql_order():
            # data_details = i[1:-1]  #MySQL detection_test的date格式有誤
            now = datetime.datetime.today()
            data_details = (i[1:-1])
            print(data_details)
            mycursor.execute(add_details, data_details)
            delete_detection = (f"DELETE FROM detection_test WHERE users_id = '{i[1]}'")
            print(delete_detection)
            mycursor.execute(delete_detection)
    except mysql.connector.errors as er_name:
        check = f"錯誤\n{er_name}"
    else:
        check = "Commit!"
    finally:
        print(check)
        connection.commit()
        mycursor.close()
        connection.close()
    return render_template('commit.html', check = check)


@app.route('/caculate', methods=["GET", "POST"])
def caculate():
    order_list = sql_order()
    total_price = 0
    result = list()
    for i in order_list:
        total_price += i[5]
        result.append(f"{i[-1].ljust(10,'－')}{str(i[4]).rjust(2)}個 ${str(i[5]).rjust(3)}")
    print("============")
    print(result)
    #####   總金額欄位   #####
    print(f"總金額:{total_price}")
    return render_template('caculate.html', total_price0 = total_price, result=result)


@app.route('/takeimage', methods = ["GET", "POST"])
def takeimage():
    users_id = request.form['name']    #從Flask帶入users_id
    now = datetime.datetime.today().strftime("%Y-%m-%d_%H%M%S")
    print(f"{users_id}({now})")
    _, frame = camera.read()
    h, w, c = frame.shape
    frame = frame[0:h, int(w / 2 - h / 2):int(w / 2 + h / 2)]
    cv2.imwrite(f"./image/{users_id}({now}.jpg", frame)
    # cv2.imshow(f"./image/{c_id}({now}.jpg", frame)
    # camera.release()
    time.sleep(2)
    caculate()
    return render_template('index.html')


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
    return render_template('index.html', show_qty=lineorder_qty())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')