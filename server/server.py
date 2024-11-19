import socket
import threading
import sqlite3
import base64


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


def handle_client(client_socket, addr):
    try:
        conn = sqlite3.connect('server.db')
        print("成功连接到数据库")
        cursor = conn.cursor()
        while True:
            [info, type_] = get_message(client_socket)
            if type_ == "":
                a = 1

    except Exception as e:
        print(str(addr) + " 连接异常: " + str(e))
        clients.remove((client_socket, addr))
        sql = "update login_info set is_online = 0 where ip = ?"
        cursor.execute(sql, (addr[0], ))
        conn.commit()
        cursor.close()
        conn.close()
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
        clients.append((client_socket, addr))
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"服务器启动异常 : {e}")
