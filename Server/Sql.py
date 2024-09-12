import sqlite3

import tkinter


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


# add_item("test", "测试", 1, "测试")
# add_item("test", "测试2", 1, "测试")
# add_item("test", "测试3", 1, "测试")
