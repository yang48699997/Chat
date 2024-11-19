# chat_client.py
import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget


class ChatClient(QMainWindow):
    def __init__(self, host, port):
        super().__init__()
        self.setWindowTitle("聊天室客户端")
        self.setGeometry(300, 300, 400, 500)
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.message_input = QLineEdit(self)
        self.send_button = QPushButton("发送", self)

        layout = QVBoxLayout()
        layout.addWidget(self.chat_display)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.message_input.text()
        if message:
            self.client_socket.send(message.encode())
            self.message_input.clear()

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_display.append(message)
            except:
                self.running = False
                break

    def closeEvent(self, event):
        self.running = False
        self.client_socket.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = ChatClient("127.0.0.1", 12345)
    client.show()
    sys.exit(app.exec_())
