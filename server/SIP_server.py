import socket
import threading
import time

# 存储注册用户的字典，用户名作为键，值为用户的地址（IP和端口）
registered_users = {}
call_sessions = {}
client_list = {}


def handle_client(client_socket, client_address):
    print(client_socket)
    try:
        while True:
            # 等待客户端发来消息
            msg = client_socket.recv(1024).decode("utf-8")
            if not msg:
                break

            print(msg)
            # 注册请求
            if msg.startswith("REGISTER"):
                username = msg.split()[1]
                registered_users[username] = client_address
                client_list[username] = client_socket
                client_socket.send(f"OK {username} registered".encode("utf-8"))
                if username not in registered_users:
                    pass
                else:
                    # client_socket.send(f"ERROR {username} already registered".encode("utf-8"))
                    pass

            # 呼叫请求
            elif msg.startswith("CALL"):
                caller = msg.split()[1]
                callee = msg.split()[2]
                if callee in registered_users:
                    callee_address = registered_users[callee]
                    call_sessions[caller] = callee
                    call_sessions[callee] = caller

                    # 通知被叫方响铃
                    call_socket = client_list[callee]
                    call_socket.\
                        send(f"RINGING {callee_address[0]}".encode("utf-8"))
                else:
                    client_socket.send(f"ERROR {callee} not registered".encode("utf-8"))

            # 处理呼叫响应
            elif msg.startswith("ANSWER"):
                callee = msg.split()[1]
                call_response = msg.split()[2]

                if callee in call_sessions:
                    caller = call_sessions[callee]
                    caller_address = registered_users[caller]
                    caller_socket = client_list[caller]
                    if call_response == "ACCEPT":
                        caller_socket.send(f"CALL ACCEPTED {caller_address[0]}".encode("utf-8"))
                        client_socket.send(f"CALL ACCEPTED {client_address[0]}".encode("utf-8"))
                        print(f"{callee} accepted the call")
                        start_video_call(caller_socket, client_socket)
                    else:
                        caller_socket.send("CALL REJECTED".encode("utf-8"))
                        client_socket.send("CALL REJECTED".encode("utf-8"))
                        print(f"{callee} rejected the call")
                        # 清理呼叫会话
                        del call_sessions[callee]
                        del call_sessions[caller]
                else:
                    client_socket.send("ERROR No such call session".encode("utf-8"))

            elif msg.startswith("STOP"):
                callee = msg.split()[1]
                if callee in call_sessions:
                    caller = call_sessions[callee]
                    caller_socket = client_list[caller]
                    caller_socket.send("CALL STOPPED".encode("utf-8"))
                    client_socket.send("CALL STOPPED".encode("utf-8"))
                    print(f"{callee} rejected the call")
                    # 清理呼叫会话
                    stop_video_call(caller_socket, client_socket)
                    del call_sessions[callee]
                else:
                    client_socket.send("ERROR No such call session".encode("utf-8"))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def start_video_call(caller_socket, callee_socket):
    caller_socket.send("VIDEO CALL STARTED".encode("utf-8"))
    callee_socket.send("VIDEO CALL STARTED".encode("utf-8"))


def stop_video_call(caller_socket, callee_socket):
    caller_socket.send("VIDEO CALL STOPPED".encode("utf-8"))
    callee_socket.send("VIDEO CALL STOPPED".encode("utf-8"))


def start_sip_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"SIP Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_sip_server("127.0.0.1", 5060)
