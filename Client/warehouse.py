import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook
import SocketManager
import ast


def update_warehouse():
    global warehouses
    result = SocketManager.sendWarehouse(0, None)
    result = result[4:]
    result = ast.literal_eval(result)
    warehouses = result
    pass


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


# 添加仓库
def add_warehouse(entry):
    if type == 0:
        new_warehouse = entry.get().strip()
        if not new_warehouse:
            messagebox.showwarning("警告", "仓库名不能为空。")
            return
        if new_warehouse in warehouses:
            messagebox.showwarning("警告", "仓库已存在。")
            return
        if (new_warehouse[0]).isdigit():
            messagebox.showwarning("警告", "仓库名不能以数字开头")
            return

        result = SocketManager.sendWarehouse(1, [new_warehouse])
        update_warehouse()
        # 清空
        entry.delete(0, tk.END)


# 删除仓库
def delete_warehouse():
    if type == 0:
        selected_warehouse = warehouse_combobox.get()
        if selected_warehouse in warehouses:
            result = SocketManager.sendWarehouse(2, [selected_warehouse])
            update_warehouse()
            # 清空
            warehouse_combobox.set("")
        else:
            messagebox.showwarning("警告", "请选择一个有效的仓库。")


# 更新物品列表
def update_item_list(event):
    for item in item_list.get_children():
        item_list.delete(item)

    selected_warehouse = warehouse_combobox.get()
    if selected_warehouse in warehouses:
        print("selected_warehouse")
        print(selected_warehouse)
        result = SocketManager.sendWarehouse(3, [selected_warehouse])
        if result == "033|":
            return
        result = result[4:]
        result = ast.literal_eval(result)
        for item in result:
            item_list.insert("", "end", values=item)


# 添加物品
def add_item():
    if type <= 1:
        item_name = item_name_entry.get().strip()
        item_quantity = item_quantity_entry.get().strip()
        item_remark = item_remark_entry.get().strip()

        if not item_name:
            messagebox.showwarning("警告", "物品名称不能为空。")
            return
        if not item_quantity.isdigit() or int(item_quantity) <= 0:
            messagebox.showwarning("警告", "物品数量必须是大于0的数字。")
            return

        selected_warehouse = warehouse_combobox.get()
        if selected_warehouse not in warehouses:
            messagebox.showwarning("警告", "请选择一个有效的仓库。")
            return

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
    if type <= 1:
        item_name = item_name_entry.get().strip()
        item_quantity = item_quantity_entry.get().strip()
        item_remark = item_remark_entry.get().strip()

        if not item_name:
            messagebox.showwarning("警告", "物品名称不能为空。")
            return
        if not item_quantity.isdigit() or int(item_quantity) <= 0:
            messagebox.showwarning("警告", "物品数量必须是大于0的数字。")
            return

        selected_warehouse = warehouse_combobox.get()
        if selected_warehouse not in warehouses:
            messagebox.showwarning("警告", "请选择一个有效的仓库。")
            return

        result = SocketManager.sendWarehouse(
            5, [selected_warehouse, item_name, item_quantity, item_remark]
        )

        # 更新物品列表
        update_item_list(None)
        # 清空输入框
        item_name_entry.delete(0, tk.END)
        item_quantity_entry.delete(0, tk.END)
        item_remark_entry.delete(0, tk.END)


# 打开仓库界面
def open_warehouse(group):

    update_warehouse()

    global type
    type = group

    warehouse_root = tk.Tk()
    warehouse_root.title("仓库管理")

    global warehouse_combobox, item_list, item_name_entry, item_quantity_entry, item_remark_entry

    global add_item_button, delete_item_button
    warehouse_combobox = None
    item_list = None

    # 添加/删除仓库
    warehouse_frame = tk.Frame(warehouse_root)
    warehouse_frame.pack(padx=10, pady=10)

    warehouse_entry = tk.Entry(warehouse_frame)
    warehouse_entry.pack(side=tk.LEFT, padx=(0, 5))

    add_button = tk.Button(
        warehouse_frame, text="添加仓库", command=lambda: add_warehouse(warehouse_entry)
    )
    add_button.pack(side=tk.LEFT, padx=(0, 5))

    delete_button = tk.Button(
        warehouse_frame, text="删除仓库", command=delete_warehouse
    )
    delete_button.pack(side=tk.LEFT)

    export_button = tk.Button(
        warehouse_frame, text="导出仓库", command=export_warehouse
    )
    export_button.pack(side=tk.LEFT)

    # 仓库选择
    warehouse_label = tk.Label(warehouse_root, text="选择仓库:")
    warehouse_label.pack(padx=10, pady=10)
    warehouse_combobox = ttk.Combobox(warehouse_root, values=warehouses)
    warehouse_combobox.bind("<<ComboboxSelected>>", update_item_list)
    warehouse_combobox.pack(padx=10, pady=10)

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
    item_name_entry = tk.Entry(item_frame)
    item_name_entry.pack(side=tk.LEFT, padx=(0, 5))

    item_quantity_label = tk.Label(item_frame, text="数量:")
    item_quantity_label.pack(side=tk.LEFT, padx=(0, 5))
    item_quantity_entry = tk.Entry(item_frame)
    item_quantity_entry.pack(side=tk.LEFT, padx=(0, 5))

    item_remark_label = tk.Label(item_frame, text="备注:")
    item_remark_label.pack(side=tk.LEFT, padx=(0, 5))
    item_remark_entry = tk.Entry(item_frame)
    item_remark_entry.pack(side=tk.LEFT, padx=(0, 5))

    add_item_button = tk.Button(item_frame, text="入库", command=add_item)
    add_item_button.pack(side=tk.LEFT, padx=(0, 5))

    delete_item_button = tk.Button(item_frame, text="出库", command=delete_item)
    delete_item_button.pack(side=tk.LEFT)

    # 通过权限控制该按钮是否可用
    item_name_label.config(state=tk.NORMAL if type == 0 else tk.DISABLED)
    item_quantity_label.config(state=tk.NORMAL if type == 0 else tk.DISABLED)
    item_remark_label.config(state=tk.NORMAL if type == 0 else tk.DISABLED)
    add_button.config(state=tk.NORMAL if type == 0 else tk.DISABLED)
    delete_button.config(state=tk.NORMAL if type == 0 else tk.DISABLED)

    warehouse_root.mainloop()


# 导出仓库
def export_warehouse():
    selected_warehouse = warehouse_combobox.get()
    if selected_warehouse not in warehouses:
        messagebox.showwarning("警告", "请选择一个有效的仓库。")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = selected_warehouse

    # 表头
    ws.append(["名称", "库存", "备注"])

    # 写入数据
    for item in warehouses[selected_warehouse]:
        ws.append(item)

    # 保存
    file_path = f"{selected_warehouse}.xlsx"
    wb.save(file_path)
    messagebox.showinfo("成功", f"{selected_warehouse} 已成功导出为 {file_path}。")


if __name__ == "__main__":
    open_warehouse(0)
