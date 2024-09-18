import tkinter as tk
from tkinter import ttk, messagebox
import SocketManager

import ast


def update_users():
    global users
    result = SocketManager.sendManagement(0, None, None)
    result = result[4:]
    result = ast.literal_eval(result)
    users = result
    pass


def get_role(user):
    result = SocketManager.sendManagement(2, user, None)
    role = int(result[4:])
    if role == 0:
        role = "超级管理员"
    elif role == 1:
        role = "仓库管理员"
    else:
        role = "用户"
    return role


# 自动填充权限
def fill_role(user_combobox, role_combobox):
    selected_user = user_combobox.get()
    if selected_user:

        role_combobox.set(get_role(selected_user))


def open_user_management():
    update_users()

    management_root = tk.Tk()
    management_root.title("用户管理")

    # 用户列表
    user_label = tk.Label(management_root, text="选择用户:")
    user_label.pack(padx=10, pady=10)

    user_combobox = ttk.Combobox(management_root, values=users)
    user_combobox.pack(padx=10, pady=10)
    user_combobox.bind(
        "<<ComboboxSelected>>", lambda event: fill_role(user_combobox, role_combobox)
    )

    # 权限
    role_label = tk.Label(management_root, text="权限")
    role_label.pack(padx=10, pady=10)

    role_combobox = ttk.Combobox(management_root, values=["仓库管理员", "用户"])
    role_combobox.pack(padx=10, pady=10)

    # 修改权限
    modify_button = tk.Button(
        management_root,
        text="修改权限",
        command=lambda: modify_user_role(user_combobox, role_combobox),
    )
    modify_button.pack(padx=10, pady=10)

    management_root.mainloop()


# 修改权限
def modify_user_role(user_combobox, role_combobox):
    selected_user = user_combobox.get()
    new_role = role_combobox.get()

    if not selected_user:
        messagebox.showwarning("警告", "请选择一个用户。")
        return
    if new_role not in ["仓库管理员", "用户"]:
        messagebox.showwarning("警告", "请选择有效的权限。")
        return
    if get_role(selected_user) == "超级管理员":
        messagebox.showwarning("警告", "你无法修改超级管理员的权限")
        return

    if new_role == "仓库管理员":
        SocketManager.sendManagement(1, selected_user, 1)
    else:
        SocketManager.sendManagement(1, selected_user, 2)

    update_users()
    messagebox.showinfo("成功", f"{selected_user} 的权限已修改为 {new_role}。")


if __name__ == "__main__":
    open_user_management()
