from flask import Flask, render_template, Response, request, redirect
import cv2
import mysql.connector
import datetime
import time
from lineorder_qty import lineorder_qty
from calculate import sql_order


app = Flask(__name__)
camera = cv2.VideoCapture(0)


@app.route('/lineaccept', methods=["GET", "POST"])
def line_accept():
    accept_id = request.form['a_id']
    print(accept_id)
    return render_template('lineorder.html')



@app.route('/lineorder', methods=["GET", "POST"])
def line_order():
    connection = mysql.connector.connect(host="35.221.178.251",
                                        database="project",
                                        user="root",
                                        password="cfi10202")
    mycursor = connection.cursor()
    mycursor.execute("SELECT u.users_id, p.products_id, now() as date, sum(l.quantity) as QTYs, "
                    "sum(l.quantity*p.price) as total_price, sum(l.quantity*p.`heat(kcal)`) as total_heat, l.products_name, l.accept "
                    "FROM linebot_test l JOIN users u ON l.line_id = u.line_id "
                    "JOIN products p ON p.products_name = l.products_name "
                    "GROUP BY u.users_id, p.products_id, l.accept")
    line_order_list = mycursor.fetchall()
    mycursor.close()
    connection.close()
    id = set()
    for n in range(len(line_order_list)):
        id.add(line_order_list[n][0])
    id = list(id)
    order = dict()
    for U in id:
        order[U] = dict()
        text = list()
        price = 0
        accpet = 0
        for L in line_order_list:
            if L[0] == U:
                text.append(f"{L[6].ljust(6, '－')}{str(L[3]).rjust(2,'－')}個 ${str(L[4]).rjust(3,' ')}")
                price += L[4]
                accpet += L[7]
            order[U]['清單'] = text
            order[U]['總金額'] = int(price)
            order[U]['接單'] = "待接單" if accpet == 0 else "OK"


    return render_template('lineorder.html',id = id, order = order)

@app.route('/cancel_order', methods = ["GET", "POST"])
def cancel_order():
    try:
        connection = mysql.connector.connect(host="35.221.178.251",
                                             database="project",
                                             user="root",
                                             password="cfi10202")
        mycursor = connection.cursor()
        for i in sql_order():
            delete_detection = (f"DELETE FROM detection_test WHERE users_id = '{i[1]}'")
            print(delete_detection)
            mycursor.execute(delete_detection)
    except Exception as err_type :
        check_x = f"錯誤\n{err_type}"
    else:
        check_x = "取消"
    finally:
        print(check_x)
        connection.commit()
        mycursor.close()
        connection.close()
    return render_template('cancel.html', check_x=check_x)




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
            add_details = (f"INSERT INTO details "
                           f"(users_id, products_id, date, quantity, price, details_cal) "
                           f"VALUES ({i[1]}, {i[2]}, '{i[3]}', {i[4]}, {i[5]}, {i[6]})")
            print(add_details)
            mycursor.execute(add_details)
            delete_detection = (f"DELETE FROM detection_test WHERE users_id = {i[1]}  and products_id = {i[2]}")
            print(delete_detection)
            mycursor.execute(delete_detection)
    except Exception as err_type :
        check = f"錯誤\n{err_type}"
    else:
        check = "Commit!"
    finally:
        print(check)
        connection.commit()
        mycursor.close()
        connection.close()
    return render_template('commit.html', check=check)


@app.route('/calculate', methods=["GET", "POST"])
def calculate():
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
    return render_template('calculate.html', total_price0 = total_price, result=result)


@app.route('/takeimage', methods = ["GET", "POST"])
def takeimage():
    users_id = request.form['name']    #從Flask帶入users_id
    now = datetime.datetime.today().strftime("%Y-%m-%d_%H%M%S")
    print(f"{users_id}({now})")
    _, frame = camera.read()
    h, w, c = frame.shape
    frame = frame[0:h, int(w / 2 - h / 2):int(w / 2 + h / 2)]
    cv2.imwrite(f"./image/{users_id}({now}.jpg", frame)
    # cv2.imshow(f"./image/{users_id}({now}.jpg", frame)
    # camera.release()
    time.sleep(2)
    calculate()
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