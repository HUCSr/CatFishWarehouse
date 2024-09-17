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


def SaveAutoReply(message):
    global lastMessage

    if lastMessage != "":
        if os.path.exists("AutoReply.json") == False:
            reply = {}
            with open("AutoReply.json", "w", encoding="utf-8") as t:
                json.dump(reply, t)
        with open("AutoReply.json", "r", encoding="utf-8") as t:
            reply = json.load(t)

        if reply.get(lastMessage) == None:
            reply[lastMessage] = []

        reply[lastMessage].append(message)
        with open("AutoReply.json", "w", encoding="utf-8") as t:
            json.dump(reply, t)

    lastMessage = message


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
            if not data:
                break  # 如果客户端断开连接，退出循环

            if len(requestTimeList[userid]) < 20:
                requestTimeList[userid].append(time.time())
            else:
                firstTime = requestTimeList[userid][0]
                if time.time() - firstTime <= 10:
                    sendMessage("100|", client_socket)
                    continue
                else:
                    del requestTimeList[userid][0]
                    requestTimeList[userid].append(time.time())

            message = data.decode()

            print(f"Received from {userid}: {message}")
            # 登录请求
            if message[:3] == "001" or message[:3] == "011":
                result = Sql.Login(
                    message[4:].split(" ")[0], message[4:].split(" ")[1], message[:3][1]
                )
                print("AWA")
                sendMessage("001|" + str(result), client_socket)
            # 注册请求
            elif message[:3] == "002":
                result = Sql.Register(
                    message[4:].split(" ")[0], message[4:].split(" ")[1]
                )
                sendMessage("002|" + str(result), client_socket)
    except:
        # 关闭连接
        print(f"Connection from {userid} closed.")
        if client_socket in clients:
            clients.remove(client_socket)

        del usernames[userid]

        client_socket.close()


def broadcast(message):
    print(message)
    for client in clients:
        try:
            client.send((message).encode())
        except:
            # 如果发送失败，说明客户端已断开连接，移除该客户端
            clients.remove(client)


def sendMessage(message, client):
    try:
        client.send(message.encode())
    except:
        # 如果发送失败，说明客户端已断开连接，移除该客户端
        clients.remove(client)


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
