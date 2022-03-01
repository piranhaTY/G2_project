#################################################
# 結帳確認後將 MySQL：detection_test資料挪至details #
#################################################
import mysql.connector
import datetime
import time
from caculate import sql_order

def commit_order():
    connection = mysql.connector.connect(host="35.221.178.251",
                                        database="project",
                                        user="root",
                                        password="cfi10202")
    mycursor = connection.cursor()

    add_details = ("INSERT INTO details "
                   "(users_id, products_id, date, quantity, price, details_cal) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")

    for i in sql_order():
        now = datetime.datetime.today()
        data_details = (i[1], i[2], now, i[4], i[5], i[6])
        print(data_details)
        mycursor.execute(add_details, data_details)
        delete_detection = (f"DELETE FROM detection_test WHERE users_id = '{i[1]}'")
        print(delete_detection)
        mycursor.execute(delete_detection)
    # connection.commit()
    mycursor.close()
    connection.close()


print("---")
print(sql_order())
print(len(sql_order()))
print("********")
commit_order()