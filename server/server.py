import socket
import threading
import sqlite3
import base64
from snowflake import Snowflake
import encryption

clients = []
is_file = 0


def get_message(client_socket) -> [str, str]:
    global is_file
    if is_file == 1:
        infor = client_socket.recv(102400)
        if not infor:
            raise ValueError("No data received")
        infor = base64.b64decode(infor)
        type_ = "file"
        is_file = 0
    else:
        infor = client_socket.recv(1024)
        if not infor:
            raise ValueError("No data received")
        infor = str(infor, "utf-8")
        type_ = infor.split(";")[0]
    return infor, type_


def register(info, cursor):
    user_info = info.split(';')
    user_name = user_info[1]
    user_password = user_info[2]
    user_email = user_info[3]
    user_gender = user_info[4]
    user_birthday = user_info[5]
    user_picture = user_info[6]
    print(info)
    try:
        sql = "select * from user_info where email = ?"
        result = cursor.execute(sql, (user_email, )).fetchall()
        if len(result) >= 1:
            return "该邮箱已被注册"
        snowflake = Snowflake(data_center_id=1, machine_id=1)
        user_id = snowflake.next_id()
        user_password = encryption.hash_password_fixed(user_password)
        sql = "insert into user_info (id, username, password, email, gender, birthday, picture)\
                                values (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, (user_id, user_name, user_password, user_email, user_gender, user_birthday, user_picture))
        return "1"
    except Exception as register_e:
        print(f"注册时错误 : {register_e}")
        return "注册失败"


def login(info, cursor):
    user_info = info.split(';')
    user_password = user_info[2]
    print(user_password)
    user_password = encryption.hash_password_fixed(user_password)
    try:
        if '@' in user_info[1]:
            user_email = user_info[1]
            result = cursor.execute("select * from user_info where email = ?", (user_email, )).fetchall()
            if len(result) == 0:
                return "该邮箱不存在"
            sql = "select * from user_info where email = ? and password = ?"
            result = cursor.execute(sql, (user_email, user_password)).fetchall()
            if len(result) == 0:
                return "密码错误"
            print(result)
            result = result[0]
            print(result)
            return "1" + ";" + str(result[0]) + ";" + str(result[1]) + ";" + str(result[4]) \
                + ";" + str(result[5]) + ";" + str(result[6])
        else:
            user_id = user_info[1]
            result = cursor.execute("select * from user_info where id = ?", (user_id, )).fetchall()
            if len(result) == 0:
                return "该ID不存在"
            sql = "select * from user_info where id = ? and password = ?"
            result = cursor.execute(sql, (user_id, user_password)).fetchall()
            if len(result) == 0:
                return "密码错误"
            result = result[0]
            return "1" + ";" + str(result[0]) + ";" + str(result[1]) + ";" + str(result[4])\
                   + ";" + str(result[5]) + ";" + str(result[6])
    except Exception as login_e:
        print(f"登录失败 : {login_e}")
        return "登录失败"


def forget_password(info, cursor):
    pass


def get_userinfo(info, cursor):
    user_info = info.split(';')
    user_id = user_info[1]
    try:
        sql = "select * from user_info where id = ?"
        result = cursor.execute(sql, (user_id, )).fetchall()
        if len(result) == 0:
            return "用户不存在"
        result = result[0]
        return "1" + ";" + str(result[0]) + ";" + str(result[1]) + ";" + str(result[4])\
                   + ";" + str(result[5]) + ";" + str(result[6]) + ";" + str(result[7])
    except Exception as get_info_e:
        print(f"用户信息获取失败 : {get_info_e}")
        return "用户信息获取失败"


def get_friend(info, cursor):
    user_info = info.split(';')
    user_id = user_info[1]
    user_friends = []
    try:
        result = cursor.execute('''
        SELECT friend_id, status 
        FROM friend_info
        WHERE user_id = ?
        ''', (user_id, )).fetchall()
        for res in result:
            if str(res[1]) == "3" and str(res[0]) != user_id:
                user_friends.append(str(res[0]))
        result = cursor.execute('''
                SELECT user_id, status 
                FROM friend_info
                WHERE friend_id = ?
                ''', (user_id, )).fetchall()
        for res in result:
            if str(res[1]) == "3" and str(res[0]) != user_id:
                user_friends.append(str(res[0]))
        friend_list = ";".join(friend for friend in user_friends)
        print(friend_list)
        return "1;" + friend_list
    except Exception as get_friend_e:
        print(f"好友获取失败 : {get_friend_e}")
        return "好友获取失败"


def add_friend(info, cursor):
    user_id = info[1]
    friend_id = info[2]
    try:
        if user_id < friend_id:
            result = cursor.execute('''
                    SELECT status 
                    FROM friend_info
                    WHERE user_id = ? and friend_id = ?
                    ''', (user_id, friend_id)).fetchall()
            if len(result) == 0:
                cursor.execute("""
                                insert into friend_info (user_id, friend_id, status)
                                values(?, ?, ?)
                                """, (user_id, friend_id, "1"))
        else:
            result = cursor.execute('''
                    SELECT status 
                    FROM friend_info
                    WHERE user_id = ? and friend_id = ?
                    ''', (user_id, friend_id)).fetchall()
            if len(result) == 0:
                cursor.execute("""
                                insert into friend_info (user_id, friend_id, status)
                                values(?, ?, ?)
                                """, (friend_id, user_id, "2"))
        return "1;添加成功"
    except Exception as add_friend_e:
        print(f"添加好友异常 : {add_friend_e}")
        return "添加好友异常"


def handle_add_friend(info, cursor):
    user_id = info[1]
    friend_id = info[2]
    op = info[3]
    try:
        if op == "0":
            cursor.execute('''
                DELETE FROM friend_info
                WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
            ''', (user_id, friend_id, friend_id, user_id))
        elif user_id < friend_id:
            cursor.execute('''
                            UPDATE friend_info
                            SET status = ?
                            WHERE (user_id = ? AND friend_id = ?)
                            ''', ("3", user_id, friend_id))
        else:
            cursor.execute('''
                            UPDATE friend_info
                            SET status = ?
                            WHERE (user_id = ? AND friend_id = ?)
                            ''', ("3", friend_id, user_id))
        return "操作成功"
    except Exception as handle_add_friend_e:
        print(f"处理好友添加异常 : {handle_add_friend_e}")
        return "处理好友添加异常"


def handle_client(client_socket):
    try:
        conn = sqlite3.connect('server.db')
        print("成功连接到数据库")
        cursor = conn.cursor()
        result = ""
        while True:
            [info, type_] = get_message(client_socket)
            if type_ == "0000":
                result = register(info, cursor)
            elif type_ == "0001":
                result = login(info, cursor)
            elif type_ == "0002":
                # 待补充
                # result = forget_password(info, cursor)
                pass
            elif type_ == "0003":
                result = get_userinfo(info, cursor)
            elif type_ == "0004":
                result = get_friend(info, cursor)
            elif type_ == "0005":
                result = add_friend(info, cursor)
            elif type_ == "0006":
                result = handle_add_friend(info, cursor)
            elif type_ == "":
                pass
            client_socket.sendall(str(result).encode(encoding='utf-8'))
            print(str(result))
            conn.commit()
    except Exception as handle_e:
        print(f"{client_socket} 连接异常: {handle_e}")
        clients.remove(client_socket)
    finally:
        try:
            client_socket.close()
        except Exception as client_e:
            print(f"{client_socket} 连接关闭异常 : {client_e}")


def main():
    clients.clear()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(10)
    print("服务器已启动，等待客户端连接...")

    while True:
        client_socket, addr = server.accept()
        print(f"客户端 {addr} 已连接。")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()


def init_db():
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()

    # 备用
    # cursor.execute('DROP TABLE IF EXISTS user_info')
    # cursor.execute('DROP TABLE IF EXISTS friend_info')
    # cursor.execute('DROP TABLE IF EXISTS group_info')
    # cursor.execute('DROP TABLE IF EXISTS group_members')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        gender TEXT NOT NULL,
        birthday TEXT NOT NULL,
        picture TEXT NOT NULL,
        status INTEGER NOT NULL DEFAULT 0
    )
    ''')

    """
    status:
        0 : 双方不是好友
        1 : user_id 请求添加 friend_id 为好友
        2 : friend_id 请求添加 user_id 为好友
        3 : 双方已成为好友
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS friend_info (
        user_id TEXT,
        friend_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (user_id, friend_id),
        FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE,
        FOREIGN KEY (friend_id) REFERENCES user_info(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group_info (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        owner_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES user_info(id) ON DELETE CASCADE
    )
    ''')

    """
    status:
        0 : user_id 不是 group_id 的成员
        1 : user_id 申请加入 group_id 
        2 : group_id 邀请 user_id 加入
        3 : user_id 是 group_id 的成员
    """
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS group_members (
        group_id TEXT,
        user_id TEXT,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (group_id, user_id),
        FOREIGN KEY (group_id) REFERENCES group_info(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES user_info(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()


if __name__ == "__main__":
    try:
        init_db()
        main()
    except Exception as e:
        print(f"服务器启动异常 : {e}")
