import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap


class CreateGroupChatPage(QWidget):
    def __init__(self, users=None, parent=None):
        super(CreateGroupChatPage, self).__init__(parent)
        self.setWindowTitle("创建群聊")
        self.setGeometry(100, 100, 400, 600)

        # 模拟用户数据：包含名称和头像路径
        self.users = users or []

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 搜索框
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("群名称")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #FFFFFF;
                border-radius: 4px;
                font-size: 14px;
                color: #FFFFFF;
            }
        """)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # 分类标题
        category_label = QLabel("选择好友创建")
        category_label.setFont(QFont("Arial", 12, QFont.Bold))
        category_label.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(category_label)

        # 用户选择列表
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                background-color: #2c2c2c;
                border: none;
                padding: 5px;
                font-size: 14px;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #3d85c6;
                color: #ffffff;
            }
        """)

        for user in self.users:
            item = QListWidgetItem(user["username"])
            item.setIcon(QIcon(QPixmap(user["avatar"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            item.setCheckState(Qt.Unchecked)
            item.setData(QtCore.Qt.UserRole, user["uid"])
            self.user_list.addItem(item)
        main_layout.addWidget(self.user_list)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.create_button = QPushButton("确定")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        button_layout.addWidget(self.create_button)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        self.setLayout(main_layout)


class CreateGroupInvitePage(QWidget):
    def __init__(self, users=None, parent=None):
        super(CreateGroupInvitePage, self).__init__(parent)
        self.setWindowTitle("邀请好友")
        self.setGeometry(100, 100, 400, 600)

        # 模拟用户数据：包含名称和头像路径
        self.users = users or []

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 分类标题
        category_label = QLabel("选择好友")
        category_label.setFont(QFont("Arial", 12, QFont.Bold))
        category_label.setStyleSheet("color: #ffffff;")
        main_layout.addWidget(category_label)

        # 用户选择列表
        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                background-color: #2c2c2c;
                border: none;
                padding: 5px;
                font-size: 14px;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #3d85c6;
                color: #ffffff;
            }
        """)

        for user in self.users:
            item = QListWidgetItem(user["username"])
            item.setIcon(QIcon(QPixmap(user["avatar"]).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
            item.setCheckState(Qt.Unchecked)
            item.setData(QtCore.Qt.UserRole, user["uid"])
            self.user_list.addItem(item)
        main_layout.addWidget(self.user_list)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.create_button = QPushButton("确定")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        button_layout.addWidget(self.create_button)

        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        # 设置整体样式
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateGroupChatPage()
    window.show()
    sys.exit(app.exec_())
