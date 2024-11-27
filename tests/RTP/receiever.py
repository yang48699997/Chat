import cv2
import socket
import struct
import numpy as np
import pyaudio

RTP_HEADER_SIZE = 12
RTP_VIDEO_PORT = 5003
RTP_AUDIO_PORT = 5004

AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 10240

def parse_rtp_header(data):
    header = struct.unpack('!BBHII', data[:RTP_HEADER_SIZE])
    version = header[0] >> 6
    payload_type = header[1] & 0x7F
    sequence_number = header[2]
    timestamp = header[3]
    ssrc = header[4]
    return version, payload_type, sequence_number, timestamp, ssrc

def receive_video_stream():
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    video_socket.bind(('0.0.0.0', RTP_VIDEO_PORT))
    print(f"Listening for RTP video on port {RTP_VIDEO_PORT}...")

    try:
        while True:
            data, _ = video_socket.recvfrom(65536)
            if len(data) <= RTP_HEADER_SIZE:
                continue

            payload = data[RTP_HEADER_SIZE:]
            frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Received Video", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_socket.close()
        cv2.destroyAllWindows()

def receive_audio_stream():
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    audio_socket.bind(('0.0.0.0', RTP_AUDIO_PORT))

    audio = pyaudio.PyAudio()
    stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

    print(f"Listening for RTP audio on port {RTP_AUDIO_PORT}...")
    try:
        while True:
            data, _ = audio_socket.recvfrom(65536)
            if len(data) <= RTP_HEADER_SIZE:
                continue

            payload = data[RTP_HEADER_SIZE:]
            stream.write(payload)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_socket.close()


if __name__ == "__main__":
    from threading import Thread
    Thread(target=receive_video_stream).start()
    Thread(target=receive_audio_stream).start()
