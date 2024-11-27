import socket
import threading
import time
import cv2
import struct

# 配置 SIP 客户端
SERVER_IP = '127.0.0.1'  # SIP 服务器 IP 地址
SERVER_PORT = 5060  # SIP 默认端口
CLIENT_PORT = 5061
USER = 'user1'  # 用户名
PASSWORD = 'password'  # 密码（这里没有实现认证，仅示范注册）
CONTACT = 'sip:user1@127.0.0.1'  # 联系地址
TO_USER = 'user1'  # 呼叫目标

RTP_PORT = 5003  # 接收方视频 RTP 端口

# SIP 消息头部和常用的 SIP 请求格式
REGISTER_MSG = f"REGISTER sip:{SERVER_IP} SIP/2.0\r\n" \
               f"Via: SIP/2.0/UDP {SERVER_IP}:5060;branch=z9hG4bK-1\r\n" \
               f"Max-Forwards: 70\r\n" \
               f"From: <sip:{USER}@{SERVER_IP}>;tag={USER}\r\n" \
               f"To: <sip:{USER}@{SERVER_IP}>\r\n" \
               f"Call-ID: 1234567890\r\n" \
               f"CSeq: 1 REGISTER\r\n" \
               f"Contact: <{CONTACT}>\r\n\r\n"

INVITE_MSG = f"INVITE sip:{TO_USER}@{SERVER_IP} SIP/2.0\r\n" \
             f"Via: SIP/2.0/UDP {SERVER_IP}:5060;branch=z9hG4bK-1\r\n" \
             f"Max-Forwards: 70\r\n" \
             f"From: <sip:{USER}@{SERVER_IP}>;tag={USER}\r\n" \
             f"To: <sip:{TO_USER}@{SERVER_IP}>\r\n" \
             f"Call-ID: 1234567890\r\n" \
             f"CSeq: 1 INVITE\r\n" \
             f"Contact: <{CONTACT}>\r\n\r\n"


# 创建 UDP 套接字
def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# 发送 SIP 请求
def send_sip_request(message, server_address):
    client_socket = create_socket()
    client_socket.sendto(message.encode(), server_address)
    response, _ = client_socket.recvfrom(1024)
    print(f"Received response: {response.decode()}")
    client_socket.close()


# 注册请求
def register_to_server():
    server_address = (SERVER_IP, SERVER_PORT)
    print("Sending REGISTER request...")
    send_sip_request(REGISTER_MSG, server_address)


# 发起呼叫请求
def invite_to_user():
    server_address = (SERVER_IP, SERVER_PORT)
    print("Sending INVITE request...")
    send_sip_request(INVITE_MSG, server_address)


# 解析 SDP 信息
def parse_sdp(sdp_data):
    # 假设从 SDP 响应中解析视频端口（例如 5004）
    for line in sdp_data.split('\r\n'):
        if line.startswith('m=video'):
            port = line.split()[1]  # 获取端口号
            return int(port)
    return None


# 启动 RTP 发送视频流
def start_rtp_video():
    # 使用 OpenCV 捕获视频
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access camera.")
        return
    else:
        print("success camera")
    # 创建 UDP 套接字
    rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rtp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 目标地址是目标用户的 IP 地址和端口（5004）
    rtp_address = (SERVER_IP, RTP_PORT)
    print(rtp_address)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Video Stream", frame)
        # 压缩为 JPEG 格式
        _, buffer = cv2.imencode('.jpg', frame)
        # 发送 RTP 包
        rtp_socket.sendto(buffer.tobytes(), rtp_address)
        time.sleep(0.03)  # 控制帧率

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    rtp_socket.close()


# 客户端接收响应并解析
def listen_for_responses():
    client_socket = create_socket()
    client_socket.bind(('0.0.0.0', CLIENT_PORT))  # 监听所有接口
    print(f"Listening for responses on {SERVER_IP}:{CLIENT_PORT}...")

    while True:
        data, addr = client_socket.recvfrom(1024)
        print(f"Received SIP response: {data.decode()}")

        # 当收到 INVITE 响应时，开始视频流传输
        if "SIP/2.0 180 Ringing" in data.decode():
            sdp_start = data.decode().find("v=0")
            sdp_data = data.decode()[sdp_start:]
            port = parse_sdp(sdp_data)
            if port:
                global RTP_PORT
                RTP_PORT = port
                print(f"Received SDP, starting video stream to port {RTP_PORT}...")
                threading.Thread(target=start_rtp_video, daemon=True).start()


# 主函数
def main():
    # 启动监听线程
    threading.Thread(target=listen_for_responses).start()

    # 等待一定时间以确保客户端开始监听
    time.sleep(1)

    # 注册并发起呼叫
    register_to_server()
    time.sleep(1)  # 等待注册响应
    invite_to_user()
    # time.sleep(10)  # 等待注册响应


if __name__ == "__main__":
    main()
