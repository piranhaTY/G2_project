####################################
# 列出辨識結果 MySQL：detection_test #
###################################

import mysql.connector
import datetime
import time


def sql_order():
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
    mycursor.close()
    connection.close()
    return order_list

def caculate():
    total_price = 0
    for i in sql_order():
        total_price += i[5]
        result = "".join(f"{i[-1].ljust(10,'－')}{str(i[4]).rjust(2)}個 ${str(i[5]).rjust(3)}\n" for i in sql_order())
        print(f"{i[-1].ljust(10,'－')}{str(i[4]).rjust(2)}個 ${str(i[5]).rjust(3)}")
    #####   總金額欄位   #####
    print(f"總金額:{total_price}")
    return total_price, result

if __name__ == "__main__":
    print(sql_order())
    now = datetime.datetime.today()         ## 間隔1秒，預留辨識及寫入資料時間
    print(f"---------{now}按下 (結帳) 鍵")    ## 間隔1秒，預留辨識及寫入資料時間
    #####   辨識結果欄位   #####
    print(f"購買清單:")
    time.sleep(1)
    now = datetime.datetime.today()         ## 間隔1秒，預留辨識及寫入資料時間
    print(f"---------{now}")                ## 間隔1秒，預留辨識及寫入資料時間
    caculate()



"""sql_order()
orders_id, users_id, products_id, date, qty, total_price, total_heat, products_name
[(5001, '6', 3, 20220200000000.0, 2, Decimal('60'), 404.0, '鴨珍')]
"""