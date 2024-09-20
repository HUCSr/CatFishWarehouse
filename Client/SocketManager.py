import socket

debug = 1


def sendManagement(type, user, role):
    if user == None:
        client_socket.send(("0" + str(type) + "4|").encode())
    elif role == None:
        client_socket.send(("0" + str(type) + "4|" + user).encode())
    else:
        client_socket.send(("0" + str(type) + "4|" + user + " " + str(role)).encode())
    while True:
        try:
            # 接收服务器端消息
            data = client_socket.recv(1024)
            print(data)
            if not data:
                return -1
                # 如果服务器端断开连接，退出循环
            message = data.decode()
            print(message)
            return message
        except:
            break


def sendWarehouse(type, namelist):
    if namelist == None:
        client_socket.send(("0" + str(type) + "3|").encode())
    elif type <= 3:
        client_socket.send(("0" + str(type) + "3|" + namelist[0]).encode())
    elif type != 6:
        client_socket.send(
            (
                "0"
                + str(type)
                + "3|"
                + namelist[0]
                + " "
                + namelist[1]
                + " "
                + str(namelist[2])
                + " "
                + namelist[3]
            ).encode()
        )
    else:
        client_socket.send(("063|" + namelist).encode())
    while True:
        try:
            # 接收服务器端消息
            data = client_socket.recv(1024)
            print(data)
            if not data:
                return -1
                # 如果服务器端断开连接，退出循环
            message = data.decode()
            print(message)
            return message
        except:
            break


def sendDirectory(type, namelist):
    if type <= 2:
        client_socket.send(("0" + str(type) + "5|" + namelist).encode())
    while True:
        try:
            # 接收服务器端消息
            data = client_socket.recv(1024)
            print(data)
            if not data:
                return -1
                # 如果服务器端断开连接，退出循环
            message = data.decode()
            print("message")
            print(message)
            return message
        except:
            break


def sendLogin(username, password, type):
    # 发送登录请求
    client_socket.send(
        ("0" + str(type) + "1|" + str(username) + " " + str(password)).encode()
    )
    while True:
        try:
            # 接收服务器端消息
            data = client_socket.recv(1024)
            print(data)
            if not data:
                return -1
                # 如果服务器端断开连接，退出循环
            message = data.decode()
            print(message)
            return message
        except:
            break


def sendRegister(username, password):
    # 发送注册请求
    client_socket.send(("002|" + str(username) + " " + str(password)).encode())
    while True:
        try:
            # 接收服务器端消息
            data = client_socket.recv(1024)
            if not data:
                return -1
                # 如果服务器端断开连接，退出循环
            message = data.decode()
            return message
        except:
            break


# 创建客户端套接字


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器

if debug:
    server_address = ("localhost", 8080)
else:
    server_address = ("110.42.253.171", 8080)

client_socket.connect(server_address)
