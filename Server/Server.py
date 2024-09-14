import socket
import threading
import time
import os
import json
import jieba
import math
import random

import Sql


# 存储所有客户端套接字的列表
clients = []

requestTimeList = {}
usernames = {}

lastMessage = ""


def handle_client(client_socket):
    global requestTimeList
    global usernames

    userid = client_socket.getpeername()

    print(client_socket)

    try:
        while True:
            # 接收客户端消息
            data = client_socket.recv(1024)
            print(data)
    except:
        # 关闭连接
        print(f"Connection from {userid} closed.")
        if client_socket in clients:
            clients.remove(client_socket)

        del usernames[userid]

        client_socket.close()


Sql._init()

# 创建服务器端套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# '10.0.4.16'

# localhost

# IP = '10.0.4.16'
IP = "localhost"
# 绑定地址和端口
server_address = (IP, 8080)
server_socket.bind(server_address)

# 监听连接请求
server_socket.listen(5)

print("Waiting for clients to connect...")


while True:
    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    # 存储客户端套接字到列表
    clients.append(client_socket)

    requestTimeList[client_socket.getpeername()] = []

    usernames[client_socket.getpeername()] = ""

    print(client_socket)

    # 创建一个线程来处理客户端
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
