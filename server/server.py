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
    try:
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
    except Exception as message_e:
        print(f"信息接收错误 : {message_e}")
        return "", ""


def register(info, conn):
    user_info = info.split(';')
    user_name = user_info[1]
    user_password = user_info[2]
    user_email = user_info[3]
    user_gender = user_info[4]
    user_birthday = user_info[5]
    user_picture = user_info[6]
    try:
        sql = "select * from user_info where email = ?"
        cursor = conn.excute(sql, user_email).fetchall()
        if len(cursor) >= 1:
            return "该邮箱已被注册"
        snowflake = Snowflake(data_center_id=1, machine_id=1)
        user_id = snowflake.next_id()
        user_password = encryption.hash_password(user_password)
        sql = "insert into user_info (id, name, password, email, gender, birthday, picture)\
                                values (?, ?, ?, ?, ?, ?, ?)"
        conn.excute(sql, (user_id, user_name, user_password, user_gender, user_birthday, user_picture))
        return "注册成功"
    except Exception as register_e:
        print(f"注册时错误 : {register_e}")
    finally:
        return "注册失败"


def handle_client(client_socket):
    try:
        conn = sqlite3.connect('server.db')
        print("成功连接到数据库")
        cursor = conn.cursor()
        while True:
            [info, type_] = get_message(client_socket)
            if type_ == "0000":
                pass
            conn.commit()
    except Exception as e:
        print(f"{client_socket} 连接异常: {e}")
        clients.remove(client_socket)
        # sql = "update login_info set is_online = 0 where ip = ?"
        # cursor.execute(sql, (addr[0], ))
        # conn.commit()
        # cursor.close()
        # conn.close()
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


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"服务器启动异常 : {e}")
