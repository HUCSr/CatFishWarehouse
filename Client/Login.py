import tkinter as tk
import json
import os
import SocketManager
import hashlib

import warehouse
import management
import threading


# 保存账号密码的文件路径
CREDENTIALS_FILE = "credentials.json"


# 加密
def encode(password):
    hash = hashlib.md5(password.encode())
    return hash.hexdigest()


# 加载账号和密码
def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {"username": "", "password": "", "remember": 0}


# 保存账号和密码
def save_credentials(username, password, remember):
    print(CREDENTIALS_FILE)
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(
            {"username": username, "password": password, "remember": remember}, file
        )


# 提示信息
def tip(message):
    tip_label.config(text=message)


# 新的窗口
def open_warehouse_thread(group):
    warehouse.open_warehouse(group)


def open_management_thread():
    management.open_user_management()


# 登录功能
def login(login_type):
    username = username_entry.get()
    password = password_entry.get()

    if not username:
        tip("账号不能为空")
        return
    if not password:
        tip("密码不能为空")
        return
    if " " in password:
        tip("密码中不能含有空格")
        return

    save_credentials(username, password, save_credentials_var.get())

    password = encode(password)

    print("username:", username)
    print("password:", password)

    result = SocketManager.sendLogin(username, password, login_type)

    if result == "100|":
        tip("操作过于频繁,请稍后再进行操作")
    elif result == "001|3":
        tip("权限不足")
    elif result == "001|4":
        tip("账号或密码错误")
    elif result == "001|5":
        tip("不存在的账号")
    else:
        group = result[-1]
        tip("登录成功")

        # GlobalVar.set_value("username", username)
        if login_type == 0:
            threading.Thread(target=open_warehouse_thread, args=(int(group),)).start()
            root.after(100, root.destroy)
        else:
            threading.Thread(target=open_management_thread).start()
            root.after(100, root.destroy)
    pass


# 注册功能
def register():
    username = username_entry.get()
    password = password_entry.get()

    if not username:
        tip("账号不能为空")
        return
    if not password:
        tip("密码不能为空")
        return
    if " " in password:
        tip("密码中不能含有空格")
        return

    save_credentials(username, password, save_credentials_var.get())

    password = encode(password)

    print("username:", username)
    print("password:", password)

    result = SocketManager.sendRegister(username, password)

    if result == "100|":
        tip("操作过于频繁,请稍后再进行操作")
    elif result != "002|0":
        tip("账号已存在")
    else:
        tip("注册成功")


def open_login():
    global root, tip_label, save_credentials_var
    global username_entry, password_entry
    # 创建主窗口
    root = tk.Tk()
    root.title("Login")
    root.geometry("240x250")

    # 加载之前保存的账号和密码
    credentials = load_credentials()

    # 账号
    username_label = tk.Label(root, text="账号:")
    username_label.place(x=10, y=20)
    username_entry = tk.Entry(root, fg="black", bg="white", justify=tk.CENTER)
    username_entry.place(x=50, y=20)

    if credentials["remember"] == 1:
        username_entry.insert(0, credentials["username"])  # 自动填充

    # 密码
    password_label = tk.Label(root, text="密码:")
    password_label.place(x=10, y=60)
    password_entry = tk.Entry(root, fg="black", bg="white", show="*", justify=tk.CENTER)
    password_entry.place(x=50, y=60)
    if credentials["remember"] == 1:
        password_entry.insert(0, credentials["password"])  # 自动填充

    # 选择是否保存账号密码
    save_credentials_var = tk.BooleanVar()
    save_credentials_checkbox = tk.Checkbutton(
        root, text="记住账号密码", variable=save_credentials_var
    )
    save_credentials_checkbox.place(x=70, y=100)

    # 登录按钮
    warehouse_button = tk.Button(root, text="进入仓库", command=lambda: login(0))
    warehouse_button.place(x=30, y=130, width=80, height=40)

    management_button = tk.Button(root, text="进入管理", command=lambda: login(1))
    management_button.place(x=130, y=130, width=80, height=40)

    # 注册按钮
    register_button = tk.Button(root, text="注册", command=register)
    register_button.place(x=90, y=190, width=60, height=30)

    # 提示信息
    tip_label = tk.Label(root, text="", anchor="center", fg="red")
    tip_label.place(x=20, y=220, width=200, height=30)

    root.mainloop()
