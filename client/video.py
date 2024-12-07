import struct
import sys
import socket
import threading
import time
from queue import Queue
import numpy as np
from threading import Thread

import cv2
import pyaudio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QDialog, QHBoxLayout
from PyQt5.QtCore import QTimer, QObject, pyqtSignal


class RTPStream:
    def __init__(self, ip, sip_client=None, flag=0, video_port=5003, audio_port=5004):
        self.RTP_IP = ip
        self.sip_client = sip_client
        self.flag = flag
        self.RTP_VIDEO_PORT = video_port
        self.RTP_AUDIO_PORT = audio_port
        self.RTP_HEADER_SIZE = 12

        # Streaming 状态
        self.streaming = False

        # 视频线程和音频线程
        self.video_thread = None
        self.audio_thread = None

        # 视频和音频套接字
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # 音频参数
        self.AUDIO_FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 10240

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
                time.sleep(0.03)

        finally:
            cap.release()
            print("视频发送线程已结束")

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
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print("音频发送线程已结束")

    def receive_video_stream(self):
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.video_socket.bind(('0.0.0.0', self.RTP_VIDEO_PORT))
        print(f"正在监听视频帧数据在端口 {self.RTP_VIDEO_PORT}...")
        try:
            while self.streaming:
                data, _ = self.video_socket.recvfrom(65536)
                if len(data) <= self.RTP_HEADER_SIZE:
                    continue

                payload = data[self.RTP_HEADER_SIZE:]
                frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("Video", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.close()
                    self.sip_client.stop()
                    break
        finally:
            self.video_socket.close()
            cv2.destroyAllWindows()
            print("视频接收线程已结束")

    def receive_audio_stream(self):
        self.audio_socket.bind(('0.0.0.0', self.RTP_AUDIO_PORT))

        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.AUDIO_FORMAT, channels=self.CHANNELS, rate=self.RATE, output=True,
                            frames_per_buffer=self.CHUNK)

        print(f"正在监听音频数据在端口 {self.RTP_AUDIO_PORT}...")
        try:
            while self.streaming:
                data, _ = self.audio_socket.recvfrom(65536)
                if len(data) <= self.RTP_HEADER_SIZE:
                    continue

                payload = data[self.RTP_HEADER_SIZE:]
                stream.write(payload)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            print("音频接收线程已结束")

    def start_streaming(self):
        self.streaming = True
        if self.flag == 1:  # 发送端
            self.video_thread = Thread(target=self.send_video_stream, daemon=True)
        else:  # 接收端
            self.video_thread = Thread(target=self.receive_video_stream, daemon=True)

        # 启动视频线程
        if self.video_thread:
            self.video_thread.start()

    def stop_threads(self):
        """确保线程正确结束"""
        self.streaming = False
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join()

        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()

    def close(self):
        """释放所有资源"""
        self.video_socket.close()
        self.audio_socket.close()
        cv2.destroyAllWindows()
        print("所有资源已释放")


class SIPClient(QObject):
    show_ringing_signal = pyqtSignal()  # 定义信号

    def __init__(self, username, server_ip, server_port):
        super().__init__()
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port
        self.rtp_stream = RTPStream("127.0.0.1", self)
        self.ringing_window = None

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))

        self.message_queue = Queue()
        self.running = True

        # 连接信号到主线程槽
        self.show_ringing_signal.connect(self.show_ringing_window)

    def register(self):
        self.client_socket.send(f"REGISTER {self.username}".encode("utf-8"))
        print("注册信息发送成功")

    def call(self, callee):
        self.client_socket.send(f"CALL {self.username} {callee}".encode("utf-8"))
        print(f"正在呼叫 {callee}...")

    def stop(self):
        self.client_socket.send(f"STOP {self.username}".encode("utf-8"))
        print(f"正在请求结束通话...")

    def listen_for_incoming_calls(self):
        while self.running:
            time.sleep(0.3)
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
        self.rtp_stream.start_streaming()

    def process_messages(self):
        while self.running:
            time.sleep(0.3)
            if not self.message_queue.empty():
                msg = self.message_queue.get()
                print(f"接收到消息: {msg}")

                if msg.startswith("RINGING"):
                    tip = msg.split()[1]
                    print(tip)
                    self.rtp_stream = RTPStream(tip, self)
                    # 通过信号通知主线程显示窗口
                    self.show_ringing_signal.emit()

                elif msg.startswith("CALL ACCEPTED"):
                    self.rtp_stream.streaming = True
                    self.start_video_call()
                elif msg.startswith("CALL REJECTED"):
                    self.rtp_stream.streaming = False
                    print("Call rejected.")
                elif msg.startswith("VIDEO CALL STOPPED"):
                    self.rtp_stream.streaming = False
                    print("Call ended.")

    def show_ringing_window(self):
        """弹出接听/拒绝窗口"""
        print("主线程显示来电窗口")
        self.ringing_window = RingingWindow(self)
        self.ringing_window.show()

    def send_answer(self, accept):
        """发送接听或拒绝的答复"""
        if accept:
            self.client_socket.send(f"ANSWER {self.username} ACCEPT".encode("utf-8"))
            self.rtp_stream.flag = 1
        else:
            self.client_socket.send(f"ANSWER {self.username} REJECT".encode("utf-8"))
            self.rtp_stream.flag = 0
        self.ringing_window.close()

    def start(self):
        self.register()

        threading.Thread(target=self.listen_for_incoming_calls, daemon=True).start()
        threading.Thread(target=self.process_messages, daemon=True).start()

    def close(self):
        self.running = False
        self.client_socket.close()
        print("客户端关闭.")


class RingingWindow(QWidget):
    def __init__(self, client_):
        super().__init__()
        self.client_ = client_
        print(client_)
        print(client_.username)
        self.init_ui()
        self.setup_timer()
        print("here")

    def init_ui(self):
        self.setWindowTitle("Incoming Call")
        self.resize(300, 150)

        # 创建控件
        self.label = QLabel("Incoming call. Do you want to accept?", self)
        self.accept_button = QPushButton("Accept", self)
        self.reject_button = QPushButton("Reject", self)

        # 布局管理
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.reject_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 信号与槽
        self.accept_button.clicked.connect(self.accept_call)
        self.reject_button.clicked.connect(self.reject_call)
        print("pppppppppppppppp")

    def setup_timer(self):
        # 设置 15 秒倒计时自动拒绝
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_reject)
        self.timer.start(15000)  # 15 秒

    def accept_call(self):
        self.timer.stop()  # 停止计时器
        self.client_.send_answer(True)
        self.close()

    def reject_call(self):
        self.timer.stop()  # 停止计时器
        self.client_.send_answer(False)
        self.close()

    def auto_reject(self):
        print("15秒未接听，自动拒绝来电")
        self.client_.send_answer(False)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = SIPClient("alice", "127.0.0.1", 5060)
    client.start()
    sys.exit(app.exec_())
