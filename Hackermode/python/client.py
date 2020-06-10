#!/usr/bin/python3
import mysql.connector as mysql
import threading
import socket

db = mysql.connect(
    host="db",
    user="root",
    passwd="my_secret_pw_shh",
    database="Chat_history"
)

n = input("Enter username: ")
#n = "ArmyGeneral"
c = socket.socket()
c.connect(('0.0.0.0', 9999))
cursor = db.cursor(buffered=True)

sql_2 = "Insert into history (id,username,chat,sent_date) values (NULL,%s,%s,CURDATE())"


def send():
    while True:
        try:
            message = input()
            values = (n, message)
            cursor.execute(sql_2, values)
            db.commit()
            print(n+"(me):"+message)
            if 'Exit' not in message:
                message = n+":"+message
                c.send(message.encode('utf-8'))
            else:
                message = n+":"+message
                c.send(message.encode('utf-8'))
                c.close()
                break
        except:
            c.close()
            break


def recieve():
    while True:
        try:
            data = c.recv(1024).decode('utf-8')
            if "NICK" == data:
                c.send(n.encode('utf-8'))
            else:
                print(data)
        except:
            print("Exited ")
            c.close()
            break


def querry(sql):
    if "AirForce" in n:
        if "Chief" in n:
            sql = sql + \
                "and (username like '%Air%' or username = 'ArmyGeneral' or username ='NavyMarshall' or username ='ChiefCommander')"
            return sql
        sql += "and ( username like '%Air%')"
    elif "Army" in n:
        if "General" in n:
            sql = sql + \
                "and (username like '%Army%' or username = 'AirForce' or username ='AirForceChief' or username ='ChiefCommander')"
            return sql
        sql += "and( username like '%Army%')"
    elif "Navy" in n:
        if "Marshall" in n:
            sql = sql + \
                "and ( username like '%Navy%' or username = 'AirForceChief' or username ='ArmyGeneral' or username ='ChiefCommander')"
            return sql
        sql += "and (username like '%Navy%')"
    return sql


def Missed_Message():
    sql = "Select username,chat from history where id > (select id from history where username='{}' order by id desc limit 1)"
    sql = querry(sql)
    cursor.execute(sql.format(n))
    records = cursor.fetchall()
    if records:
        print("Messages Missed")
        for record in records:
            a, b = record
            print(a+":"+b)
    else:
        sql = "select id from history where username='{}' order by id desc limit 1".format(n)
        # print(sql)
        cursor.execute(sql)
        d = cursor.fetchall()
        if "Army" in n:
            if d:
                print("NO MESSAGE MISSED")
            else:
                cursor.execute("select username,chat from history where username like '%Army%'")
                for a, b in cursor.fetchall():
                    print(a+":"+b)
        elif "Navy" in n:
            if d:
                print("NO MESSAGE MISSED")
            else:
                cursor.execute("select username,Chat from history where username like '%Navy%'")
                for a, b in cursor.fetchall():
                    print(a+":"+b)
        elif "Air" in n:
            if d:
                print("NO MESSAGE MISSED")
            else:
                cursor.execute("select username,chat from history where username like '%Air%'")
                for a, b in cursor.fetchall():
                    print(a+":"+b)
        else:
            if d:
                print("NO MESSAGE MISSED")
            else:
                cursor.execute('select username,chat from history')
                for a, b in cursor.fetchall():
                    print(a+":"+b)
    return


Missed_Message()

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
send_thread = threading.Thread(target=send)
send_thread.start()
