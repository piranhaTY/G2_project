import mysql.connector
import datetime
import time
from caculate_x import sql_queue

def commit_order():
    connection = mysql.connector.connect(host="35.221.178.251",
                                        database="project",
                                        user="root",
                                        password="cfi10202")
    mycursor = connection.cursor()

    add_details = ("INSERT INTO details "
                   "(users_id, date, product_name, quantity, price, detailscol) "
                   "VALUES (%s, %s, %s, %s, %s, %s)")
    for i in sql_queue():
        mycursor.execute(add_details, i)
        delete_queue = (f"DELETE FROM queue WHERE product_name = '{i[2]}'")
        mycursor.execute(delete_queue)
    connection.commit()
    mycursor.close()
    connection.close()


print("---")
print(sql_queue())
print(len(sql_queue()))
print("********")
commit_order()