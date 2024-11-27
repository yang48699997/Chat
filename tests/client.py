import socket
import struct
import threading
import cv2
import time
import pyaudio
import numpy as np
from threading import Thread


class RTPStream:
    def __init__(self, ip, video_port, audio_port):
        self.RTP_IP = ip
        self.RTP_VIDEO_PORT = video_port
        self.RTP_AUDIO_PORT = audio_port

        self.RTP_HEADER_SIZE = 12

        # 音频参数
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 10240

        # 创建 UDP 套接字
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 添加用于控制线程的标志
        self.streaming = True

    def create_rtp_header(self, sequence_number, timestamp, ssrc=12345):
        version = 2  # RTP 版本号
        payload_type = 26  # 视频类型
        marker = 0  # 标志位
        header = struct.pack('!BBHII',
                             (version << 6) | payload_type,
                             marker,
                             sequence_number,
                             timestamp,
                             ssrc)
        return header

    def send_video_stream(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("无法获取摄像头资源")
            return

        print(f"正在发送视频帧数据到 {self.RTP_IP}:{self.RTP_VIDEO_PORT}...")
        sequence_number = 0
        timestamp = 0

        try:
            while self.streaming:
                ret, frame = cap.read()
                if not ret:
                    print("无法从摄像头获取帧资源")
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                header = self.create_rtp_header(sequence_number, timestamp)
                self.video_socket.sendto(header + buffer.tobytes(), (self.RTP_IP, self.RTP_VIDEO_PORT))

                sequence_number += 1
                timestamp += 3000

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                time.sleep(0.03)
        finally:
            cap.release()
            self.video_socket.close()
            cv2.destroyAllWindows()

    def send_audio_stream(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)

        sequence_number = 0
        timestamp = 0

        print(f"正在发送音频数据到 {self.RTP_IP}:{self.RTP_AUDIO_PORT}...")
        try:
            while self.streaming:
                audio_data = stream.read(self.CHUNK)
                header = self.create_rtp_header(sequence_number, timestamp)
                self.audio_socket.sendto(header + audio_data, (self.RTP_IP, self.RTP_AUDIO_PORT))

                sequence_number += 1
                timestamp += 160
        except Exception as e:
            print(f"发送音频数据错误: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            self.audio_socket.close()

    def parse_rtp_header(self, data):
        header = struct.unpack('!BBHII', data[:self.RTP_HEADER_SIZE])
        version = header[0] >> 6
        payload_type = header[1] & 0x7F
        sequence_number = header[2]
        timestamp = header[3]
        ssrc = header[4]
        return version, payload_type, sequence_number, timestamp, ssrc

    def receive_video_stream(self):
        video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        video_socket.bind(('0.0.0.0', self.RTP_VIDEO_PORT))
        print(f"正在监听视频帧数据在端口 {self.RTP_VIDEO_PORT}...")

        try:
            while self.streaming:
                data, _ = video_socket.recvfrom(65536)
                if len(data) <= self.RTP_HEADER_SIZE:
                    continue

                payload = data[self.RTP_HEADER_SIZE:]
                frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            video_socket.close()
            cv2.destroyAllWindows()

    def receive_audio_stream(self):
        audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        audio_socket.bind(('0.0.0.0', self.RTP_AUDIO_PORT))

        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                            frames_per_buffer=self.CHUNK)

        print(f"正在监听音频数据在端口 {self.RTP_AUDIO_PORT}...")
        try:
            while self.streaming:
                data, _ = audio_socket.recvfrom(65536)
                if len(data) <= self.RTP_HEADER_SIZE:
                    continue

                payload = data[self.RTP_HEADER_SIZE:]
                stream.write(payload)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            audio_socket.close()

    def start_streaming(self):
        # 启动视频和音频的发送和接收线程
        Thread(target=self.send_video_stream).start()
        Thread(target=self.send_audio_stream).start()

        Thread(target=self.receive_video_stream).start()
        Thread(target=self.receive_audio_stream).start()

    def close(self):
        self.streaming = False
        self.video_socket.close()
        self.audio_socket.close()
        cv2.destroyAllWindows()
        print("所有资源已释放")


class SIPClient:
    def __init__(self, username, server_ip, server_port):
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

        # 初始化 RTPStream 实例
        self.rtp_stream = RTPStream('127.0.0.1', 5003, 5004)

    def register(self):
        self.client_socket.send(f"REGISTER {self.username}".encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def call(self, callee):
        self.client_socket.send(f"CALL {self.username} {callee}".encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)

    def answer_call(self, response):
        self.client_socket.send(f"ANSWER {self.username} {response}".encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(response)
        if response == "CALL ACCEPTED":
            self.start_video_call()

    def start_video_call(self):
        print("Starting video call...")
        self.rtp_stream.start_streaming()  # 启动 RTP 流

    def listen_for_incoming_calls(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('0.0.0.0', 5061))  # Listen on port 5060 for incoming calls
        print("Listening for incoming calls...")

        while True:
            data, addr = server_socket.recvfrom(1024)
            print(f"{data.decode('utf-8')} 正在呼叫")
            user_response = input("是否接听? (yes/no): ")
            if user_response.lower() == "yes":
                self.answer_call("ACCEPT")
            else:
                self.answer_call("REJECT")

    def start(self):
        # 注册
        self.register()

        # 启动接听线程
        threading.Thread(target=self.listen_for_incoming_calls, daemon=True).start()

        # 等待用户按下 c 发起呼叫
        while True:
            user_input = input("Press 'c' to call or 'q' to quit: ")
            if user_input.lower() == 'c':
                callee = input("Enter the username to call: ")
                self.call(callee)

                time.sleep(1)  # 给服务器一点时间发送信息

            elif user_input.lower() == 'q':
                break

        self.rtp_stream.close()  # 退出时停止视频流


if __name__ == "__main__":
    client = SIPClient("alice", "127.0.0.1", 5060)
    client.start()
