#!/usr/bin/python3
import socket
import threading

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 9999))
s.listen()
Leader_clients = []
Army_clients = []
AirForce_clients = []
Navy_clients = []
Chief_client = []


def handle(connection):
    while True:
        try:
            msg = connection.recv(1024)
            for c in Chief_client:
                c.send(msg)
            if connection in Army_clients:
                if connection in Leader_clients:
                    for l in Leader_clients:
                        if l != connection:
                            l.send(msg)
                for a in Army_clients:
                    a.send(msg)

            elif connection in Navy_clients:
                if connection in Leader_clients:
                    for l in Leader_clients:
                        if l != connection:
                            l.send(msg)
                for a in Navy_clients:
                    a.send(msg)

            elif connection in AirForce_clients:
                if connection in Leader_clients:
                    for l in Leader_clients:
                        if l != connection:
                            l.send(msg)
                for a in AirForce_clients:
                    a.send(msg)
            else:
                for l in Leader_clients:
                    l.send(msg)

        except:
            if connection in Army_clients:
                if connection in Leader_clients:
                    Leader_clients.remove(connection)
                Army_clients.remove(connection)
                connection.close()
                break
            elif connection in Navy_clients:
                if connection in Leader_clients:
                    Leader_clients.remove(connection)
                Navy_clients.remove(connection)
                connection.close()
                break
            elif connection in AirForce_clients:
                if connection in Leader_clients:
                    Leader_clients.remove(connection)
                AirForce_clients.remove(connection)
                connection.close()
                break
            else:
                Chief_client.remove(connection)
                connection.close()
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

    print(f"{addr[0]} connected")
    con.send("Welcome to chat room".encode('utf-8'))
    Thread1 = threading.Thread(target=handle, args=(con,))
    Thread1.start()
