#!/usr/bin/python3
import threading
import socket


n = input("Enter username: ")
c = socket.socket()
c.connect(('0.0.0.0', 9999))


def send():
    while True:
        message = '{}: {}'.format(n, input(''))
        c.send(message.encode('utf-8'))


def recieve():
    while True:
        try:
            data = c.recv(1024).decode('utf-8')
            if "NICK" == data:
                c.send(n.encode('utf-8'))
            else:
                print(data)
        except Exception as e:
            print("error occured {}".format(e))
            c.close()
            break


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
send_thread = threading.Thread(target=send)
send_thread.start()
