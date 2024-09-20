import socket
import threading
import time
import os
import json
import jieba
import math
import random
import logging
from logging.handlers import TimedRotatingFileHandler


import Sql


# 记录操作日志
log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

log_file = os.path.join(log_folder, "server.log")
handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("ServerLogger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# 存储所有客户端套接字的列表
clients = []

requestTimeList = {}
usernames = {}


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
                logger.info(message[4:].split(" ")[0] + " login")

            # 注册请求
            elif message[:3] == "002":
                result = Sql.Register(
                    message[4:].split(" ")[0], message[4:].split(" ")[1]
                )
                sendMessage("002|" + str(result), client_socket)
                logger.info(message[4:].split(" ")[0] + " requests registration")

            # 获取仓库列表请求
            elif message[:3] == "003":
                print(message[:3])
                result = Sql.Warehouse_list()
                sendMessage("003|" + str(result), client_socket)
                pass
            # # 添加仓库
            # elif message[:3] == "013":
            #     result = Sql.add_warehouse(message[4:])
            #     sendMessage("013|", client_socket)
            #     logger.info("The " + str(message[4:]) + " warehouse has been added")

            #     pass
            # # 删除仓库
            # elif message[:3] == "023":
            #     result = Sql.del_warehouse(message[4:])
            #     sendMessage("023|", client_socket)
            #     logger.info("The " + str(message[4:]) + " warehouse has been deleted")

            #     pass
            # 获取仓库物品
            elif message[:3] == "033":
                result = Sql.item_in_warehouse(message[4:])
                sendMessage("033|" + str(result), client_socket)
                pass
            # 入库
            elif message[:3] == "043":
                result = Sql.add_item(message[4:].split(" "))
                sendMessage("043|", client_socket)
                logger.info(
                    "Added "
                    + str(message[4:].split(" ")[2])
                    + " items of "
                    + str(message[4:].split(" ")[1])
                    + " to the "
                    + str(message[4:].split(" ")[0])
                    + " warehouse, with a remark of "
                    + str(message[4:].split(" ")[3])
                    + "."
                )

                pass
            # 出库
            elif message[:3] == "053":
                result = Sql.del_item(message[4:].split(" "))
                sendMessage("053|", client_socket)
                logger.info(
                    "Deleted "
                    + str(message[4:].split(" ")[2])
                    + " items of "
                    + str(message[4:].split(" ")[1])
                    + " to the "
                    + str(message[4:].split(" ")[0])
                    + " warehouse, with a remark of "
                    + str(message[4:].split(" ")[3])
                    + "."
                )
                pass
            # 查询历史记录
            elif message[:3] == "063":
                result = Sql.get_histroy(message[4:])
                sendMessage("063|" + result, client_socket)
                pass
            # 用户
            elif message[:3] == "004":
                result = Sql.user_list()
                sendMessage("004|" + result, client_socket)
                pass
            # 修改权限
            elif message[:3] == "014":
                result = Sql.change_role(message[4:].split(" "))
                sendMessage("014|", client_socket)
                logger.info(
                    "User "
                    + str(message[4:].split(" ")[0])
                    + "'s permissions have been changed to "
                    + str(message[4:].split(" ")[1])
                )
                pass
            # 获取权限
            elif message[:3] == "024":
                result = Sql.get_role(message[4:])
                sendMessage("024|" + str(result), client_socket)
                pass

            # 查看当前仓库
            elif message[:3] == "005":
                result = Sql.get_directory(message[4:])
                print("result")
                print(result)
                sendMessage("005|" + str(result), client_socket)
                pass
            # 新建分类
            elif message[:3] == "015":
                result = Sql.create_directory(message[4:], 0, 0, message[4:])
                print("result")
                print(result)
                sendMessage("015|" + str(result), client_socket)
                pass
            # 新建仓库
            elif message[:3] == "025":
                result = Sql.create_directory(message[4:], 0, 1, message[4:])
                sendMessage("025|" + str(result), client_socket)
                logger.info("The " + str(message[4:]) + " warehouse has been added")
                # result = Sql.create_directory(message[4:], 0)
                # print("result")
                # print(result)
                pass
            # 删除分类
            elif message[:3] == "035":
                result = Sql.delete_directory(message[4:], 0, 0, message[4:])
                print("result")
                print(result)
                sendMessage("035|" + str(result), client_socket)
                pass
            # 删除仓库
            elif message[:3] == "045":
                result = Sql.delete_directory(message[4:], 0, 1, message[4:])
                sendMessage("045|" + str(result), client_socket)
                logger.info("The " + str(message[4:]) + " warehouse has been deleted")
                # result = Sql.create_directory(message[4:], 0)
                # print("result")
                # print(result)
                pass
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
