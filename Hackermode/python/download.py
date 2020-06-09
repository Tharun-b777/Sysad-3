#!/usr/bin/python3
import mysql.connector as mysql
#import getpass
db = mysql.connect(
    host="db",
    user="root",
    passwd="my_secret_pw_shh",
    database="Chat_history"
)

cursor = db.cursor()
usr = input("Enter username: ")
# usr=getpass.getuser()

sql = "SELECT username,chat,sent_date from history WHERE sent_date >= curdate() - INTERVAL DAYOFWEEK(curdate())+6 DAY AND sent_date < curdate() - INTERVAL DAYOFWEEK(curdate())-1 DAY and username = '{}'".format(usr)
cursor.execute(sql)
records = cursor.fetchall()
if records:
    f = open("Chat_history.txt", "a+")
    for record in records:
        a, b, c = record
        f.write(a+"(me):"+b+" "+str(c)+"\n")
    f.close()

else:
    print("NO RECORDS FOUND FOR THE PAST 1 WEEK")
