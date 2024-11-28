from queue import Queue
import socket
import struct
import threading
import cv2
import time
import pyaudio
import numpy as np
from threading import Thread


class RTPStream:
    def __init__(self, ip, video_port=5003, audio_port=5004):
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
        self.rtp_stream = RTPStream("127.0.0.1")

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

        self.message_queue = Queue()
        self.running = True

    def register(self):
        self.client_socket.send(f"REGISTER {self.username}".encode("utf-8"))
        print("注册信息发送成功")

    def call(self, callee):
        self.client_socket.send(f"CALL {self.username} {callee}".encode("utf-8"))
        print(f"正在呼叫 {callee}...")

    def listen_for_incoming_calls(self):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    msg = data.decode("utf-8")
                    self.message_queue.put(msg)
            except Exception as e:
                print(f"接收消息时发生错误: {e}")
                break

    def start_video_call(self):
        print("开始视频聊天...")
        self.rtp_stream.start_streaming()  # 启动 RTP 流

    def process_messages(self):
        while self.running:
            if not self.message_queue.empty():
                msg = self.message_queue.get()
                print(f"接收到消息: {msg}")

                if msg.startswith("RINGING"):
                    tip = msg.split()[1]
                    self.rtp_stream = RTPStream(tip)
                    self.client_socket.send(f"ANSWER {self.username} ACCEPT".encode("utf-8"))
                elif msg.startswith("CALL ACCEPTED"):
                    self.start_video_call()
                elif msg.startswith("CALL REJECTED"):
                    print("Call rejected.")
                elif msg.startswith("END"):
                    print("Call ended.")
                    self.running = False

    def start(self):
        self.register()

        threading.Thread(target=self.listen_for_incoming_calls, daemon=True).start()
        threading.Thread(target=self.process_messages, daemon=True).start()

        while self.running:
            user_input = input("Press 'c' to call or 'q' to quit: ")
            if user_input.lower() == 'c':
                callee = input("Enter the username to call: ")
                self.call(callee)
            elif user_input.lower() == 'q':
                self.running = False
                break

        self.close()

    def close(self):
        self.running = False
        self.client_socket.close()
        print("客户端关闭.")


if __name__ == "__main__":
    client = SIPClient("alice", "127.0.0.1", 5060)
    client.start()
