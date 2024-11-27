import socket
import threading

# 配置 SIP 服务器
HOST = '0.0.0.0'  # 监听所有网络接口
PORT = 5060       # SIP 默认端口

# 注册的用户表
registered_users = {}


def parse_sip_message(data):
    """解析 SIP 消息"""
    lines = data.split('\r\n')
    method = lines[0].split(' ')[0]
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    return method, headers


def handle_register(headers):
    """处理 REGISTER 请求"""
    user = headers.get('From', '').split(':')[1].split('@')[0]
    contact = headers.get('Contact', '')
    if user and contact:
        registered_users[user] = contact
        print(f"User {user} registered with contact {contact}.")
        return "SIP/2.0 200 OK\r\n\r\n"
    return "SIP/2.0 400 Bad Request\r\n\r\n"


def handle_invite(headers):
    """处理 INVITE 请求并返回 SDP 协商信息"""
    to_user = headers.get('To', '').split(':')[1].split('@')[0]
    if to_user in registered_users:
        print(f"Call request to {to_user} forwarded.")

        # 假设返回的 SDP 包含视频信息
        sdp = "v=0\r\n" \
              "o=- 1234567890 1234567890 IN IP4 127.0.0.1\r\n" \
              "s=Video Call\r\n" \
              "c=IN IP4 127.0.0.1\r\n" \
              "t=0 0\r\n" \
              "m=video 5004 RTP/AVP 26\r\n"  # 使用 RTP/AVP 26（JPEG）

        response = f"SIP/2.0 180 Ringing\r\n" \
                   f"Contact: <sip:{registered_users[to_user]}>\r\n" \
                   f"Content-Type: application/sdp\r\n" \
                   f"Content-Length: {len(sdp)}\r\n" \
                   f"\r\n{sdp}"
        return response

    return "SIP/2.0 404 Not Found\r\n\r\n"


def handle_request(data, addr, server_socket):
    """处理 SIP 请求"""
    method, headers = parse_sip_message(data)
    if method == 'REGISTER':
        response = handle_register(headers)
    elif method == 'INVITE':
        response = handle_invite(headers)
        print(response)
        server_socket.sendto(response.encode(), ('127.0.0.1', 5061))
    else:
        response = "SIP/2.0 501 Not Implemented\r\n\r\n"
    print(addr)
    server_socket.sendto(response.encode(), addr)


def start_sip_server():
    """启动 SIP 服务器"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((HOST, PORT))
        print(f"SIP server running on {HOST}:{PORT}")
        while True:
            data, addr = server_socket.recvfrom(1024)
            threading.Thread(target=handle_request, args=(data.decode(), addr, server_socket)).start()


if __name__ == "__main__":
    start_sip_server()
