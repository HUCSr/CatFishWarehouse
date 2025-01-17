import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
import SocketManager
import ast
import matplotlib.pyplot as plt
import warehouseDirectory
import GlobalVar


GlobalVar._init()
# def update_warehouse():
#     global warehouses
#     result = SocketManager.sendWarehouse(0, None)
#     result = result[4:]
#     if result == "":
#         warehouses = []
#         return
#     result = ast.literal_eval(result)
#     warehouses = result
#     if type(warehouses) == type("a"):
#         warehouses = [warehouses]
#     pass


def on_item_select(event):
    selected_item = item_list.selection()
    if selected_item:
        item_values = item_list.item(selected_item[0], "values")
        if item_values:
            item_name_entry.delete(0, tk.END)
            item_name_entry.insert(0, item_values[0])
            item_quantity_entry.delete(0, tk.END)
            item_remark_entry.delete(0, tk.END)
            item_remark_entry.insert(0, item_values[2])


# # 添加仓库
# def add_warehouse(entry):
#     if Type == 0:
#         new_warehouse = entry.get().strip()
#         if not new_warehouse:
#             messagebox.showwarning("警告", "仓库名不能为空。")
#             return
#         if new_warehouse in warehouses or new_warehouse == "inventory_history":
#             messagebox.showwarning("警告", "仓库已存在。")
#             return
#         if (new_warehouse[0]).isdigit():
#             messagebox.showwarning("警告", "仓库名不能以数字开头")
#             return

#         result = SocketManager.sendWarehouse(1, [new_warehouse])
#         update_warehouse()
#         # 清空
#         entry.delete(0, tk.END)


# # 删除仓库
# def delete_warehouse():
#     if Type == 0:
#         if selected_warehouse in warehouses:
#             result = SocketManager.sendWarehouse(2, [selected_warehouse])
#             update_warehouse()
#             # 清空
#             now_warehouse = ""
#         else:
#             messagebox.showwarning("警告", "请选择一个有效的仓库。")


# 更新物品列表
def update_item_list(event):
    for item in item_list.get_children():
        item_list.delete(item)

    print("selected_warehouse")
    print(selected_warehouse)
    result = SocketManager.sendWarehouse(3, [selected_warehouse])
    if result == "033|":
        return
    result = result[4:]
    result = ast.literal_eval(result)
    print("AWA")
    print(type(type(result[0])))
    if type((result[0])) == type("a"):
        item_list.insert("", "end", values=result)
    else:
        for item in result:
            item_list.insert("", "end", values=item)


# 添加物品
def add_item():
    if Type <= 1:
        item_name = item_name_entry.get().strip()
        item_quantity = item_quantity_entry.get().strip()
        item_remark = item_remark_entry.get().strip()

        if not item_name:
            messagebox.showwarning("警告", "物品名称不能为空。")
            return
        if not item_quantity.isdigit() or int(item_quantity) <= 0:
            messagebox.showwarning("警告", "物品数量必须是大于0的数字。")
            return

        # if selected_warehouse not in warehouses:
        #     messagebox.showwarning("警告", "请选择一个有效的仓库。")
        #     return

        result = SocketManager.sendWarehouse(
            4, [selected_warehouse, item_name, item_quantity, item_remark]
        )

        update_item_list(None)  # 更新物品列表
        # 清空输入框
        item_name_entry.delete(0, tk.END)
        item_quantity_entry.delete(0, tk.END)
        item_remark_entry.delete(0, tk.END)


# 出库
def delete_item():
    if Type <= 1:
        item_name = item_name_entry.get().strip()
        item_quantity = item_quantity_entry.get().strip()
        item_remark = item_remark_entry.get().strip()

        if not item_name:
            messagebox.showwarning("警告", "物品名称不能为空。")
            return
        if not item_quantity.isdigit() or int(item_quantity) <= 0:
            messagebox.showwarning("警告", "物品数量必须是大于0的数字。")
            return

        # if selected_warehouse not in warehouses:
        #     messagebox.showwarning("警告", "请选择一个有效的仓库。")
        #     return

        result = SocketManager.sendWarehouse(
            5, [selected_warehouse, item_name, item_quantity, item_remark]
        )

        # 更新物品列表
        update_item_list(None)
        # 清空输入框
        item_name_entry.delete(0, tk.END)
        item_quantity_entry.delete(0, tk.END)
        item_remark_entry.delete(0, tk.END)


# 导出物品


def export_item():
    warehouseDirectory.open_warehouse_directory(Type, update_export_item, "导出至")
    pass


def update_export_item(new_warehouse):
    item_name = item_name_entry.get().strip()
    item_quantity = item_quantity_entry.get().strip()
    item_remark = item_remark_entry.get().strip()
    if not item_name:
        messagebox.showwarning("警告", "物品名称不能为空。")
        return
    if not item_quantity.isdigit() or int(item_quantity) <= 0:
        messagebox.showwarning("警告", "物品数量必须是大于0的数字。")
        return

    result = SocketManager.sendWarehouse(
        4, [new_warehouse, item_name, item_quantity, item_remark]
    )
    result = SocketManager.sendWarehouse(
        5, [selected_warehouse, item_name, item_quantity, item_remark]
    )

    update_item_list(None)  # 更新物品列表
    # 清空输入框
    item_name_entry.delete(0, tk.END)
    item_quantity_entry.delete(0, tk.END)
    item_remark_entry.delete(0, tk.END)


# 搜索物品
def search_item():
    search_name = search_entry.get().strip().lower()
    search_number_lower = search_entry_1.get().strip().lower()
    if search_number_lower == "":
        search_number_lower = "0"
    search_number_upper = search_entry_2.get().strip().lower()
    if search_number_upper == "":
        search_number_upper = "2147483647"
    for item in item_list.get_children():
        item_list.delete(item)

    result = SocketManager.sendWarehouse(
        7, [search_name, search_number_lower, search_number_upper]
    )

    print("===")
    print(result)
    result = result[4:]
    result = ast.literal_eval(result)
    print(result)
    if (result) == []:
        return
    if type(result[0]) != type([]):
        result = [result]
    for item in result:
        item_list.insert(
            "",
            "end",
            values=(
                item[0],
                item[1],
                "所在仓库: " + item[2].replace("_", "/"),
            ),
        )


#     for selected_warehouse in warehouses:
#         result = SocketManager.sendWarehouse(3, [selected_warehouse])
#         if result == "033|":
#             return
#         result = result[4:]
#         result = ast.literal_eval(result)
#         for item in result:
#             if item[0].lower() != search_term and item[0].lower() in search_term:
#                 item_list.insert(
#                     "",
#                     "end",
#                     values=(item[0], item[1], "所在仓库: " + selected_warehouse),
#                 )

#     for selected_warehouse in warehouses:
#         result = SocketManager.sendWarehouse(3, [selected_warehouse])
#         if result == "033|":
#             return
#         result = result[4:]
#         result = ast.literal_eval(result)
#         for item in result:
#             if item[0].lower() != search_term and search_term in item[0].lower():
#                 item_list.insert(
#                     "",
#                     "end",
#                     values=(item[0], item[1], "所在仓库: " + selected_warehouse),
#                 )


def show_inventory_chart():
    # if selected_warehouse not in warehouses:
    #     messagebox.showwarning("警告", "请选择一个有效的仓库。")
    #     return

    item_names = []
    item_quantities = []

    result = SocketManager.sendWarehouse(3, [selected_warehouse])
    if result == "033|":
        return
    print("===")
    print(result)
    result = result[4:]
    result = ast.literal_eval(result)
    for item in result:
        item_names.append(item[0])
        item_quantities.append(int(item[1]))

    # 解决中文显示问题
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    plt.figure(figsize=(8, 8))
    plt.pie(item_quantities, labels=item_names, autopct="%1.1f%%", startangle=140)
    plt.title(f"{selected_warehouse} 仓库库存分布")
    plt.axis("equal")
    plt.show()
    pass


# 历史记录
def show_inventory_history():
    selected_item = item_name_entry.get().strip()
    if not selected_item:
        messagebox.showwarning("警告", "请先选择物品。")
        return

    result = SocketManager.sendWarehouse(6, selected_item)

    result = result[4:]
    result = ast.literal_eval(result)
    print(result)
    history_window = tk.Toplevel()
    history_window.title(f"{selected_item} 的入库和出库历史")

    history_list = ttk.Treeview(
        history_window, columns=("库存", "状态", "操作时间", "备注"), show="headings"
    )
    history_list.heading("库存", text="库存")
    history_list.heading("状态", text="状态")
    history_list.heading("操作时间", text="操作时间")
    history_list.heading("备注", text="备注")
    history_list.pack(padx=10, pady=10)

    for record in result:
        history_list.insert(
            "",
            "end",
            values=(
                record["quantity"],
                record["operation_type"],
                record["timestamp"],
                record["remark"],
            ),
        )


def select_warehouse():
    print("AWA")
    warehouseDirectory.open_warehouse_directory(Type, update_directory, "打开仓库")
    print("AWA")
    pass


def merge_warehouse():
    warehouseDirectory.open_warehouse_directory(Type, update_merge_warehouse, "合并至")


def update_merge_warehouse(new_warehouse):
    print("合并:" + selected_warehouse + " " + new_warehouse)
    result = SocketManager.sendWarehouse(8, [selected_warehouse, new_warehouse])
    update_directory(new_warehouse)
    pass


def update_directory(new_directory):
    global selected_warehouse
    global warehouse_root
    global export_button, merge_warehouse_button, chart_button, history_button
    global add_item_button, delete_item_button, export_item_button
    selected_warehouse = new_directory
    print(selected_warehouse)
    warehouse_root.title("当前仓库: " + selected_warehouse.split("/")[-1])
    update_item_list(None)
    export_button.config(state=tk.NORMAL)
    merge_warehouse_button.config(state=tk.NORMAL)
    chart_button.config(state=tk.NORMAL)
    history_button.config(state=tk.NORMAL)

    add_item_button.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
    delete_item_button.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
    export_item_button.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)


# 打开仓库界面
def open_warehouse(group):

    global Type
    Type = group

    global warehouse_root

    warehouse_root = tk.Toplevel()
    warehouse_root.title("当前仓库: 无")

    global selected_warehouse, item_list, item_name_entry, item_quantity_entry, item_remark_entry

    global add_item_button, delete_item_button, export_item_button

    global search_entry
    global search_entry_1
    global search_entry_2

    global export_button, merge_warehouse_button, chart_button, history_button

    selected_warehouse = ""
    item_list = None

    select_warehouse_button = tk.Button(
        warehouse_root, text="选择仓库", command=select_warehouse
    )
    select_warehouse_button.pack(padx=10, pady=10)

    # 添加/删除仓库
    warehouse_frame = tk.Frame(warehouse_root)
    warehouse_frame.pack(padx=10, pady=10)

    # warehouse_entry = tk.Entry(warehouse_frame)
    # warehouse_entry.pack(side=tk.LEFT, padx=(0, 5))

    # add_button = tk.Button(
    #     warehouse_frame, text="添加仓库", command=lambda: add_warehouse(warehouse_entry)
    # )
    # add_button.pack(side=tk.LEFT, padx=(0, 5))

    # delete_button = tk.Button(
    #     warehouse_frame, text="删除仓库", command=delete_warehouse
    # )
    # delete_button.pack(side=tk.LEFT)

    export_button = tk.Button(
        warehouse_frame, text="导出仓库", command=export_warehouse
    )
    export_button.pack(side=tk.LEFT)
    export_button.config(state=tk.DISABLED)

    merge_warehouse_button = tk.Button(
        warehouse_frame, text="合并至", command=merge_warehouse
    )
    merge_warehouse_button.pack(side=tk.LEFT)
    merge_warehouse_button.config(state=tk.DISABLED)

    # 仓库选择
    # warehouse_label = tk.Label(warehouse_root, text="选择仓库:")
    # warehouse_label.pack(padx=10, pady=10)
    # warehouse_combobox = ttk.Combobox(warehouse_root, values=[])
    # warehouse_combobox.bind("<<ComboboxSelected>>", update_item_list)
    # warehouse_combobox.pack(padx=10, pady=10)

    # update_warehouse()

    # 搜索框和按钮
    search_frame = tk.Frame(warehouse_root)
    search_frame.pack(padx=10, pady=10)

    search_label = tk.Label(search_frame, text="物品名:")
    search_label.pack(side=tk.LEFT, padx=(0, 5))
    search_entry = tk.Entry(search_frame, width=10)
    search_entry.pack(side=tk.LEFT, padx=(0, 3))

    search_label_1 = tk.Label(search_frame, text=", ")
    search_label_1.pack(side=tk.LEFT, padx=(0, 5))
    search_entry_1 = tk.Entry(search_frame, width=10)
    search_entry_1.pack(side=tk.LEFT, padx=(0, 1))

    search_label_2 = tk.Label(search_frame, text="<= 物品数量 <=")
    search_label_2.pack(side=tk.LEFT, padx=(0, 5))
    search_entry_2 = tk.Entry(search_frame, width=10)
    search_entry_2.pack(side=tk.LEFT, padx=(0, 1))
    search_button = tk.Button(search_frame, text="搜索", command=search_item)
    search_button.pack(side=tk.LEFT)

    # 物品列表
    item_list = ttk.Treeview(
        warehouse_root, columns=("名称", "库存", "备注"), show="headings"
    )
    item_list.heading("名称", text="名称")
    item_list.heading("库存", text="库存")
    item_list.heading("备注", text="备注")
    item_list.pack(padx=10, pady=10)

    item_list.bind("<<TreeviewSelect>>", on_item_select)

    item_frame = tk.Frame(warehouse_root)
    item_frame.pack(padx=10, pady=10)

    item_name_label = tk.Label(item_frame, text="名称:")
    item_name_label.pack(side=tk.LEFT, padx=(0, 5))
    item_name_entry = tk.Entry(item_frame, width=10)
    item_name_entry.pack(side=tk.LEFT, padx=(0, 5))

    item_quantity_label = tk.Label(item_frame, text="数量:")
    item_quantity_label.pack(side=tk.LEFT, padx=(0, 5))
    item_quantity_entry = tk.Entry(item_frame, width=10)
    item_quantity_entry.pack(side=tk.LEFT, padx=(0, 5))

    item_remark_label = tk.Label(item_frame, text="备注:")
    item_remark_label.pack(side=tk.LEFT, padx=(0, 5))
    item_remark_entry = tk.Entry(item_frame)
    item_remark_entry.pack(side=tk.LEFT, padx=(0, 5))

    add_item_button = tk.Button(item_frame, text="入库", command=add_item)
    add_item_button.pack(side=tk.LEFT, padx=(0, 5))
    add_item_button.config(state=tk.DISABLED)

    delete_item_button = tk.Button(item_frame, text="出库", command=delete_item)
    delete_item_button.pack(side=tk.LEFT)
    delete_item_button.config(state=tk.DISABLED)

    export_item_button = tk.Button(item_frame, text="导出至", command=export_item)
    export_item_button.pack(side=tk.LEFT)
    export_item_button.config(state=tk.DISABLED)

    # 通过权限控制该按钮是否可用
    item_name_label.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
    item_quantity_label.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)
    item_remark_label.config(state=tk.NORMAL if Type == 0 else tk.DISABLED)

    chart_button = tk.Button(
        warehouse_frame, text="查看库存图表", command=show_inventory_chart
    )
    chart_button.pack(side=tk.LEFT)
    chart_button.config(state=tk.DISABLED)

    history_button = tk.Button(
        warehouse_frame, text="查看入库/出库历史", command=show_inventory_history
    )
    history_button.pack(side=tk.LEFT)
    history_button.config(state=tk.DISABLED)

    warehouse_root.mainloop()


# 导出仓库
def export_warehouse():
    # if selected_warehouse not in warehouses:
    #     messagebox.showwarning("警告", "请选择一个有效的仓库。")
    #     return

    wb = Workbook()
    ws = wb.active
    ws.title = selected_warehouse

    # 表头
    ws.append(["名称", "库存", "备注"])

    result = SocketManager.sendWarehouse(3, [selected_warehouse])
    if result == "033|":
        return
    result = result[4:]
    result = ast.literal_eval(result)

    # 写入数据
    for item in result:
        ws.append(item)

    # 保存
    file_path = f"{selected_warehouse}.xlsx"
    wb.save(file_path)
    messagebox.showinfo("成功", f"{selected_warehouse} 已成功导出为 {file_path}。")


if __name__ == "__main__":
    open_warehouse(0)
