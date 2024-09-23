import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
import SocketManager
import ast
import matplotlib.pyplot as plt
import GlobalVar


def on_directory_select(event):
    global delete_button
    global delete_category_button
    global open_button
    selected_directory = directory_list.selection()
    if selected_directory:
        selected_directory = directory_list.item(selected_directory[0], "values")[0]
    print(selected_directory)
    print(now_directory)
    if now_directory[selected_directory][1] == "仓库":
        print("A")
        delete_button.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
        delete_category_button.config(state=tk.DISABLED)
    else:
        print("B")
        delete_button.config(state=tk.DISABLED)
        delete_category_button.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
    open_button.config(state=tk.NORMAL)

    pass


def update_directory():

    global now_directory

    for _directory in directory_list.get_children():
        directory_list.delete(_directory)

    result = SocketManager.sendDirectory(0, directory)

    result = result[4:]

    if result == "{}":
        now_directory = {}
        return
    else:
        result = ast.literal_eval(result)
        if type(result) != type([]):
            result = [result]
        now_directory = {}
        for _directory in result:
            now_directory[_directory["name"]] = [_directory["date"], _directory["type"]]
            directory_list.insert(
                "",
                "end",
                values=(_directory["name"], _directory["date"], _directory["type"]),
            )

    pass


def submit_category():
    category_name = category_entry.get().strip()
    for category in directory_list.get_children():
        category_name = directory_list.item(category)["values"][0]
        if (
            category_name == category_name
            and directory_list.item(category)["values"][2] == "分类"
        ):
            messagebox.showwarning("警告", "分类已存在")
            return
    if category_name and "/" not in category_name:
        SocketManager.sendDirectory(1, directory + "/" + category_name)
        messagebox.showinfo("提示", f"分类 '{category_name}' 已创建。")
        category_window.destroy()
        update_directory()
    else:
        messagebox.showwarning("警告", "分类名不能为空,也不能含有'/'字符")


def create_category():

    global category_entry
    global category_window

    category_window = tk.Toplevel()
    category_window.title("新建分类")

    tk.Label(category_window, text="请输入分类名:").pack(padx=10, pady=10)
    category_entry = tk.Entry(category_window)
    category_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(category_window, text="确定", command=submit_category)
    submit_button.pack(pady=(5, 10))


def submit_warehouse():
    warehouse_name = warehouse_entry.get().strip()

    for directory_ in directory_list.get_children():
        directory_name = directory_list.item(directory_)["values"][0]
        if (
            warehouse_name == directory_name
            and directory_list.item(directory_)["values"][2] == "仓库"
        ):
            messagebox.showwarning("警告", "仓库已存在")
            return
    if warehouse_name and "/" not in warehouse_name:
        SocketManager.sendDirectory(2, directory + "/" + warehouse_name)
        messagebox.showinfo("提示", f"仓库 '{warehouse_name}' 已创建。")
        warehouse_window.destroy()
        update_directory()
    else:
        messagebox.showwarning("警告", "仓库名不能为空,也不能含有'/'字符")


def create_warehouse():

    global warehouse_entry
    global warehouse_window

    warehouse_window = tk.Toplevel()
    warehouse_window.title("新建分类")

    tk.Label(warehouse_window, text="请输入仓库名:").pack(padx=10, pady=10)
    warehouse_entry = tk.Entry(warehouse_window)
    warehouse_entry.pack(padx=10, pady=10)

    submit_button = tk.Button(warehouse_window, text="确定", command=submit_warehouse)
    submit_button.pack(pady=(5, 10))


def delete_warehouse():

    print("delete_warehouse")

    selected_directory = directory_list.selection()
    if selected_directory:
        selected_directory_name = directory_list.item(selected_directory[0], "values")[
            0
        ]
        selected_directory_type = directory_list.item(selected_directory[0], "values")[
            2
        ]
    print(selected_directory_name)
    print(selected_directory_type)
    print(now_directory)
    if selected_directory_type == "分类":
        SocketManager.sendDirectory(3, directory + "/" + selected_directory_name)
    else:
        SocketManager.sendDirectory(4, directory + "/" + selected_directory_name)

    messagebox.showinfo("提示", f"'{selected_directory_name}' 删除成功。")

    update_directory()


def open_directory():
    global directory
    global open_button, back_button
    selected_directory = directory_list.selection()
    if selected_directory:
        if directory_list.item(selected_directory[0], "values")[2] == "分类":
            selected_directory = directory_list.item(selected_directory[0], "values")[0]
            directory = directory + "/" + selected_directory
            update_directory()
            if "/" in directory:
                back_button.config(state=tk.NORMAL)
            else:
                back_button.config(state=tk.DISABLED)
            open_button.config(state=tk.DISABLED)
            pass
        else:
            selected_directory = directory_list.item(selected_directory[0], "values")[0]
            directory = directory + "/" + selected_directory
            GlobalVar.set_value("warehouse", directory)
            directory_root.destroy()
            callback_func(directory)


def back_directory():
    global directory
    global open_button, back_button
    index = directory.rfind("/")
    directory = directory[:index]
    update_directory()
    if "/" in directory:
        back_button.config(state=tk.NORMAL)
    else:
        back_button.config(state=tk.DISABLED)
    open_button.config(state=tk.DISABLED)


def open_warehouse_directory(group, callback, _title):

    global callback_func

    callback_func = callback

    global Type, directory, now_directory

    Type = group

    global directory_list

    global delete_button, delete_category_button, back_button, open_button
    global directory_root

    directory = ""

    now_directory = {}

    directory_root = tk.Toplevel()
    directory_root.title(_title)

    directory_frame = tk.Frame(directory_root)
    directory_frame.pack(padx=10, pady=10)

    top_button_frame = tk.Frame(directory_frame)
    top_button_frame.pack(side=tk.TOP, fill=tk.X)

    create_category_button = tk.Button(
        top_button_frame,
        text="新建分类",
        command=create_category,
    )
    create_category_button.pack(side=tk.LEFT, padx=(0, 5))

    delete_category_button = tk.Button(
        top_button_frame,
        text="删除分类",
        command=delete_warehouse,
    )
    delete_category_button.pack(side=tk.LEFT)

    directory_list = ttk.Treeview(
        directory_frame, columns=("名称", "创建日期", "类型"), show="headings"
    )
    directory_list.heading("名称", text="名称")
    directory_list.heading("创建日期", text="创建日期")
    directory_list.heading("类型", text="类型")
    directory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    directory_list.bind("<<TreeviewSelect>>", on_directory_select)

    button_frame = tk.Frame(directory_frame)
    button_frame.pack(side=tk.RIGHT, padx=(10, 0))

    create_button = tk.Button(button_frame, text="创建", command=create_warehouse)
    create_button.pack(pady=5)

    delete_button = tk.Button(
        button_frame,
        text="删除",
        command=delete_warehouse,
    )
    delete_button.pack(pady=5)

    create_button.config(state=tk.NORMAL if group == 0 else tk.DISABLED)
    delete_button.config(state=tk.DISABLED)
    create_category_button.config(state=tk.NORMAL if group == 0 else tk.DISABLED)
    delete_category_button.config(state=tk.DISABLED)

    open_button = tk.Button(button_frame, text="打开", command=open_directory)
    open_button.pack(pady=5)
    open_button.config(state=tk.DISABLED)

    back_button = tk.Button(button_frame, text="返回", command=back_directory)
    back_button.pack(pady=10)
    back_button.config(state=tk.DISABLED)

    update_directory()

    directory_root.mainloop()


if __name__ == "__main__":
    open_warehouse_directory(0)
