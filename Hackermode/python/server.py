#!/usr/bin/python3
import socket
import threading

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 9999))
s.listen(154)
Leader_clients = []
Army_clients = []
AirForce_clients = []
Navy_clients = []
Chief_client = []


def deleteconn(connection):
    print("{} exited".format(connection))
    if connection in Army_clients:
        if connection in Leader_clients:
            Leader_clients.remove(connection)
        Army_clients.remove(connection)
        connection.close()

    elif connection in Navy_clients:
        if connection in Leader_clients:
            Leader_clients.remove(connection)
        Navy_clients.remove(connection)
        connection.close()

    elif connection in AirForce_clients:
        if connection in Leader_clients:
            Leader_clients.remove(connection)
        AirForce_clients.remove(connection)
        connection.close()

    else:
        Chief_client.remove(connection)
        connection.close()
    return


def handle(connection):
    while True:
        try:
            msg = connection.recv(1024)

            if (connection in Leader_clients) or (connection in Chief_client):
                for p in Leader_clients:
                    if p != connection:
                        p.send(msg)

            for c in Chief_client:
                if c != connection:
                    c.send(msg)

            if connection in Army_clients:
                for a in Army_clients:
                    if a != connection:
                        a.send(msg)

            elif connection in Navy_clients:
                for a in Navy_clients:
                    if a != connection:
                        a.send(msg)

            elif connection in AirForce_clients:
                for a in AirForce_clients:
                    if a != connection:
                        a.send(msg)

            if "Exit" in msg.decode('utf-8'):
                print(":sjhv")
                deleteconn(connection)
                break
        except:
            deleteconn(connection)
            break


print("listenning..")
while True:
    con, addr = s.accept()
    con.send("NICK".encode('utf-8'))
    nickname = con.recv(1024).decode('utf-8')
    if "Army" in nickname:
        Army_clients.append(con)
        if "General" in nickname:
            Leader_clients.append(con)
    elif "Navy" in nickname:
        Navy_clients.append(con)
        if "Marshall" in nickname:
            Leader_clients.append(con)
    elif "Air" in nickname:
        AirForce_clients.append(con)
        if "Chief" in nickname:
            Leader_clients.append(con)
    else:
        Chief_client.append(con)

    print("{} connected".format(con))
    con.send("Welcome to chat room\nenter'Exit' to exit".encode('utf-8'))
    Thread1 = threading.Thread(target=handle, args=(con,))
    Thread1.start()
