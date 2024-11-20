import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

profile_path = "../static/profile.jpg"
profile_picture_path = "../static/profile_picture01.jpg"
msg_css = """
    QListWidget {
        background-color: rgba(245, 245, 245, 160); /* 半透明浅灰背景 */
        border: none;  /* 去掉默认边框 */
        outline: none; /* 去掉焦点虚线 */
        padding: 5px;  /* 内边距 */
    }

    /* 列表项的样式 */
    QListWidget::item {
        background-color: rgba(255,255,255,80);  /* 列表项背景色 */
        border-radius: 10px;  /* 圆角矩形 */
        margin: 5px;  /* 列表项间距 */
        padding: 10px;  /* 内容内边距 */
        color: #333333;  /* 字体颜色 */
        font-size: 14px;  /* 字体大小 */
        font-family: "Microsoft YaHei";  /* 字体 */
    }

    /* 鼠标悬停时的效果 */
    QListWidget::item:hover {
        background-color: #e6f7ff;  /* 浅蓝背景 */
        border: 1px solid #91d5ff;  /* 浅蓝边框 */
    }

    /* 鼠标点击选中时的效果 */
    QListWidget::item:selected {
        background-color: #bae7ff;  /* 浅蓝背景 */
        border: 1px solid #1890ff;  /* 深蓝边框 */
        color: #000000;  /* 改变字体颜色 */
    }

    /* 自定义滚动条样式 */
    QScrollBar:vertical {
        width: 8px;
        background: rgba(0, 0, 0, 0); /* 滚动条背景透明 */
        margin: 0px 0px 0px 0px;
        border: none;
    }
    QScrollBar::handle:vertical {
        background: #c1c1c1; /* 滚动条滑块颜色 */
        border-radius: 4px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #a6a6a6; /* 鼠标悬停时颜色 */
    }
    QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
        height: 0px;  /* 去掉滚动条上下按钮 */
    }
"""


class Profile(QWidget):
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap(profile_path)
        painter.drawPixmap(self.rect(), pixmap)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("主页")
        self.setGeometry(1400, 150, 600, 1200)
        self.setFixedWidth(600)
        self.setFixedHeight(1200)

        # 设置主布局
        main_layout = QHBoxLayout(self)

        # 左侧导航栏
        self.left_panel = QVBoxLayout()
        self.left_panel.setSpacing(20)
        self.left_panel.setAlignment(Qt.AlignTop)
        self.left_panel.setContentsMargins(10, 10, 10, 10)

        # 用户头像
        avatar = QLabel(self)
        avatar.setPixmap(QPixmap(profile_picture_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        avatar.setAlignment(Qt.AlignCenter)
        self.left_panel.addWidget(avatar)

        # 消息按钮
        self.message_button = QPushButton("消息")
        self.message_button.setStyleSheet("background-color: #5ca0d1; color: white; padding: 10px;")
        self.message_button.clicked.connect(self.show_message_list)
        self.left_panel.addWidget(self.message_button)

        # 好友按钮
        self.friends_button = QPushButton("好友")
        self.friends_button.setStyleSheet("background-color: #5ca0d1; color: white; padding: 10px;")
        self.friends_button.clicked.connect(self.show_friends_list)
        self.left_panel.addWidget(self.friends_button)

        # 群组按钮
        self.groups_button = QPushButton("群组")
        self.groups_button.setStyleSheet("background-color: #5ca0d1; color: white; padding: 10px;")
        self.groups_button.clicked.connect(self.show_groups_list)
        self.left_panel.addWidget(self.groups_button)

        # 添加左侧布局到主布局
        main_layout.addLayout(self.left_panel)

        # 右侧内容区
        self.content_stack = QStackedWidget(self)

        # 消息列表（默认展示）
        self.message_list = QListWidget()
        self.message_list.setStyleSheet(msg_css)
        self.content_stack.addWidget(self.message_list)

        # 好友列表
        self.friends_list = QListWidget()
        self.friends_list.setStyleSheet(msg_css)
        self.content_stack.addWidget(self.friends_list)

        # 群组列表
        self.groups_list = QListWidget()
        self.groups_list.setStyleSheet(msg_css)
        self.content_stack.addWidget(self.groups_list)

        # 默认显示消息列表
        self.show_message_list()

        # 添加右侧内容区到主布局
        main_layout.addWidget(self.content_stack)

        # 填充一些测试数据
        self.populate_sample_data()

    def show_message_list(self):
        """切换到消息列表"""
        self.content_stack.setCurrentWidget(self.message_list)

    def show_friends_list(self):
        """切换到好友列表"""
        self.content_stack.setCurrentWidget(self.friends_list)

    def show_groups_list(self):
        """切换到群组列表"""
        self.content_stack.setCurrentWidget(self.groups_list)

    def populate_sample_data(self):
        """填充一些测试数据"""
        # 消息列表
        for i in range(10):
            item = QListWidgetItem(f"消息 {i + 1}")
            self.message_list.addItem(item)

        # 好友列表
        for i in range(5):
            item = QListWidgetItem(f"好友 {i + 1}")
            self.friends_list.addItem(item)

        # 群组列表
        for i in range(3):
            item = QListWidgetItem(f"群组 {i + 1}")
            self.groups_list.addItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Profile()
    window.show()
    sys.exit(app.exec_())

