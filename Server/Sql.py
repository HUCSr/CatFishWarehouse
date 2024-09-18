import sqlite3
import datetime
import os
import json


def connect(name):
    conn = sqlite3.connect(name)
    print("数据库" + name + "打开成功")
    return conn


def _init():
    conn = connect("userdata.db")
    c = conn.cursor()

    c.execute(
        """CREATE TABLE IF NOT EXISTS PASSWORD
        (username TEXT PRIMARY KEY NOT NULL,
        password  TEXT NOT NULL,
        role    INT NOT NULL);"""
    )

    conn.commit()
    conn.close()

    print("数据表创建成功")


def Login(username, password, type):
    conn = connect("userdata.db")
    c = conn.cursor()

    result = c.execute(
        "SELECT username, password, role FROM PASSWORD WHERE username = '"
        + username
        + "'"
    )

    for user in result:
        print(user)
        if user[1] == password:
            if type == 1 and user[2] != 0:
                return 3
            else:
                return user[2]
        return 4
    return 5


def Register(username, password):
    conn = connect("userdata.db")
    c = conn.cursor()

    result = c.execute(
        "SELECT username FROM PASSWORD WHERE username = '" + username + "'"
    )

    for user in result:
        if (user) == "":
            continue
        print(user)
        return 1
    if username == "Bbaka":
        c.execute(
            "INSERT INTO PASSWORD (username,password,role) \
      VALUES ('"
            + username
            + "','"
            + password
            + "',0)"
        )

    else:
        c.execute(
            "INSERT INTO PASSWORD (username,password,role) \
        VALUES ('"
            + username
            + "','"
            + password
            + "',2)"
        )
    conn.commit()
    conn.close()
    return 0


def user_list():
    conn = connect("userdata.db")
    c = conn.cursor()
    result = c.execute("SELECT username FROM PASSWORD")

    user_list = []
    for user in result:
        print(user)
        user_list.append(user[0])

    print(str(user_list)[1:-1])
    return str(user_list)[1:-1]


def change_role(lists):
    user = lists[0]
    role = lists[1]
    conn = connect("userdata.db")
    c = conn.cursor()
    result = c.execute(
        "update PASSWORD set role = " + str(role) + " where username = " + user
    )
    conn.commit()
    conn.close()
    return 0


def get_role(user):
    conn = connect("userdata.db")
    c = conn.cursor()
    result = c.execute("SELECT role FROM PASSWORD where username = '" + user + "'")
    for user in result:
        return user[0]


def Warehouse_list():
    conn = connect("warehouse.db")

    c = conn.cursor()

    result = c.execute("SELECT name FROM sqlite_master WHERE type='table';")

    warehouses = []
    for warehouse in result:
        if warehouse[0] == "inventory_history":
            continue
        warehouses.append(warehouse[0])

    print(str(warehouses)[1:-1])
    return str(warehouses)[1:-1]


def add_warehouse(name):
    conn = connect("warehouse.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS """
        + str(name)
        + """
        (item_name TEXT PRIMARY KEY NOT NULL,
        item_quantity  INT NOT NULL,
        item_remark    TEXT NOT NULL);"""
    )
    conn.commit()
    conn.close()
    return 0


def del_warehouse(name):
    conn = connect("warehouse.db")
    c = conn.cursor()
    c.execute("""drop table if EXISTS """ + name + ";")
    conn.commit()
    conn.close()
    return 0


def item_in_warehouse(name):
    conn = connect("warehouse.db")
    c = conn.cursor()
    result = c.execute("SELECT item_name, item_quantity, item_remark FROM " + name)
    item_list = []
    for item in result:
        item_list.append([item[0], item[1], item[2]])
    print(str(item_list)[1:-1])
    return str(item_list)[1:-1]


def add_item(lists):
    print(lists)
    name = lists[0]
    item_name = lists[1]
    item_quantity = int(lists[2])
    item_remark = lists[3]
    print(lists)
    conn = connect("warehouse.db")
    c = conn.cursor()

    c.execute(
        """ INSERT INTO """
        + name
        + """ (item_name, item_quantity, item_remark)
    VALUES (\'"""
        + item_name
        + "',"
        + str(item_quantity)
        + ",'"
        + item_remark
        + """\')
    ON CONFLICT(item_name) DO UPDATE SET item_quantity = item_quantity + excluded.item_quantity,item_remark = excluded.item_remark;"""
    )

    conn.commit()
    conn.close()

    file_path = "inventory_history.json"

    if not os.path.exists(file_path):
        history_data = {}
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            history_data = json.load(file)

    print(history_data)

    if history_data.get(item_name) == None:
        history_data[item_name] = []
    print(history_data)

    now = datetime.datetime.now()
    time_str = now.strftime("%Y-%m-%d %H:%M:%S")

    history_data[item_name].append(
        {
            "quantity": item_quantity,
            "operation_type": "入库",
            "timestamp": time_str,
            "remark": item_remark,
        }
    )
    print(history_data)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(history_data, file)


def del_item(lists):
    print(lists)
    name = lists[0]
    item_name = lists[1]
    item_quantity = int(lists[2])
    item_remark = lists[3]
    print(lists)
    conn = connect("warehouse.db")
    c = conn.cursor()

    c.execute(
        """ INSERT INTO """
        + name
        + """ (item_name, item_quantity, item_remark)
    VALUES (\'"""
        + item_name
        + "',"
        + str(item_quantity)
        + ",'"
        + item_remark
        + """\')
    ON CONFLICT(item_name) DO UPDATE SET item_quantity = item_quantity - excluded.item_quantity,item_remark = excluded.item_remark;"""
    )
    conn.commit()
    conn.close()

    file_path = "inventory_history.json"

    if not os.path.exists(file_path):
        history_data = {}
    else:
        with open(file_path, "r", encoding="utf-8") as file:
            history_data = json.load(file)

    if history_data.get(item_name) == None:
        history_data[item_name] = []
    history_data[item_name].append(
        {
            "quantity": item_quantity,
            "operation_type": "出库",
            "timestamp": datetime.now().isoformat(),
            "remark": item_remark,
        }
    )
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(history_data, file)


def get_histroy(item):

    file_path = "inventory_history.json"

    with open(file_path, "r", encoding="utf-8") as file:
        history_data = json.load(file)[item]

    print(str(history_data))
    return str(history_data)

    pass
