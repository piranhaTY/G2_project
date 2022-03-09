import mysql.connector
import datetime
import time



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
    print(line_order_list)
    id = set()
    for n in range(len(line_order_list)):
        id.add(line_order_list[n][0])
    id = list(id)
    print(id)
    order = dict()
    for U in id:
        order[U] = dict()
        text = list()
        price = 0
        accpet = 0
        for L in line_order_list:
            if L[0] == U:
                text.append(f"{L[6].ljust(10, '－')}{L[3]}個 ${str(L[4]).rjust(4)}")
                price += L[4]
                accpet += L[7]
            order[U]['清單'] = text
            order[U]['總金額'] = int(price)
            order[U]['接單'] = False if accpet == 0 else True
    print(order)
    print("="*20)


    print(order[1]["清單"])
    print(order[1]["總金額"])
    print(order[1]["接單"])
    print(len(order))
    for l in order:
        print(l)


    return line_order_list

line_order()