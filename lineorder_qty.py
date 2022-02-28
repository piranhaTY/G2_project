########################################
# 每2秒更新 MySQL：linebot_test上的訂單量 #
#######################################

import mysql.connector
import datetime
import time


def show_num_online():
    connection = mysql.connector.connect(host="35.221.178.251",
                                        database="project",
                                        user="root",
                                        password="cfi10202")
    mycursor = connection.cursor()
    num_online = "SELECT count(DISTINCT line_id) FROM linebot_test"
    mycursor.execute(num_online)
    num_online = mycursor.fetchall()[0][0]
    now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    show_online = f"目前新增{num_online}筆線上訂餐--{now}"
    time.sleep(2)
    return show_online

if __name__ == '__main__':
    while True:
        print(show_num_online())



# mycursor.close()
# connection.close()