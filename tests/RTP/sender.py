import cv2
import socket
import time
import struct
import pyaudio

# RTP 目标地址和端口
RTP_IP = '127.0.0.1'
RTP_VIDEO_PORT = 5003
RTP_AUDIO_PORT = 5004

# RTP 包头大小
RTP_HEADER_SIZE = 12

# 音频参数
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 10240

# 创建 UDP 套接字
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def create_rtp_header(sequence_number, timestamp, ssrc=12345):
    version = 2  # RTP 版本号
    payload_type = 26  # 假设视频为 JPEG
    marker = 0  # 标志位
    header = struct.pack('!BBHII',
                         (version << 6) | payload_type,
                         marker,
                         sequence_number,
                         timestamp,
                         ssrc)
    return header

def send_video_stream():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print(f"Sending video stream to {RTP_IP}:{RTP_VIDEO_PORT}...")
    sequence_number = 0
    timestamp = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to read frame from the camera.")
                break

            _, buffer = cv2.imencode('.jpg', frame)
            header = create_rtp_header(sequence_number, timestamp)
            video_socket.sendto(header + buffer.tobytes(), (RTP_IP, RTP_VIDEO_PORT))

            sequence_number += 1
            timestamp += 3000  # 时间戳增量

            cv2.imshow("Sending Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.03)
    finally:
        cap.release()
        video_socket.close()
        cv2.destroyAllWindows()

def send_audio_stream():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    sequence_number = 0
    timestamp = 0

    print(f"Sending audio stream to {RTP_IP}:{RTP_AUDIO_PORT}...")
    try:
        while True:
            audio_data = stream.read(CHUNK)
            header = create_rtp_header(sequence_number, timestamp)
            audio_socket.sendto(header + audio_data, (RTP_IP, RTP_AUDIO_PORT))

            sequence_number += 1
            timestamp += 160  # 对应于 10ms 音频数据

    except Exception as e:
        print(f"Audio Error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_socket.close()

if __name__ == "__main__":
    from threading import Thread
    Thread(target=send_video_stream).start()
    Thread(target=send_audio_stream).start()
