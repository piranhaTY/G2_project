from flask import Flask, render_template, Response, request, redirect
import cv2
import datetime
import time
from lineorder_qty import lineorder_qty


app = Flask(__name__)
camera = cv2.VideoCapture(0)

now = datetime.datetime.today().strftime("%Y-%m-%d_%H%M%S")



import mysql.connector
import datetime
import time



@app.route('/caculate', methods=["GET", "POST"])
def caculate():
    connection = mysql.connector.connect(host="35.221.178.251",
                                         database="project",
                                         user="root",
                                         password="cfi10202")
    mycursor = connection.cursor()

    mycursor.execute("SELECT d.orders_id, d.users_id, d.products_id, d.date, count(*) as qty, "
                     "sum(p.price) as total_price, sum(p.`heat(kcal)`) as total_heat, p.products_name "
                     "FROM project.detection_test d "
                     "JOIN project.products p on d.products_id = p.products_id "
                     "GROUP BY orders_id, d.users_id, d.date, products_id")
    order_list = mycursor.fetchall()
    print(order_list)
    mycursor.close()
    connection.close()
    # total_price = 0
    # for i in order_list:
    #     total_price += i[5]
    #     result = "".join(f"{i[-1].ljust(10,'－')}{str(i[4]).rjust(2)}個 ${str(i[5]).rjust(3)}\n" for i in order_list)
    #     print(f"{i[-1].ljust(10,'－')}{str(i[4]).rjust(2)}個 ${str(i[5]).rjust(3)}")
    # #####   總金額欄位   #####
    # print(f"總金額:{total_price}")
    # return render_template('index.html', total_price = total_price, result = result)
    return render_template('index.html', order_list=order_list)


@app.route('/takeimage', methods = ['POST'])
def takeimage():
    users_id = request.form['name']    #從Flask帶入users_id
    print(f"{users_id}({now})")
    _, frame = camera.read()
    h, w, c = frame.shape
    frame = frame[0:h, int(w / 2 - h / 2):int(w / 2 + h / 2)]
    cv2.imwrite(f"./image/{users_id}({now}.jpg", frame)
    # cv2.imshow(f"./image/{c_id}({now}.jpg", frame)
    # camera.release()
    time.sleep(2)
    caculate()
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