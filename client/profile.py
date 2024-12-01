import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QIcon, QMouseEvent
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
uid = None
username = None
gender = None
birthday = None
user_profile_picture_path = None
msg_css = """
    QListWidget {
        background-color: rgba(245, 245, 245, 160); /* 半透明浅灰背景 */
        border: none;  /* 去掉默认边框 */
        outline: none; /* 去掉焦点虚线 */
        padding: 1px;  /* 内边距 */
    }

    /* 列表项的样式 */
    QListWidget::item {
        background-color: rgba(255,255,255,80);  /* 列表项背景色 */
        border-radius: 10px;  /* 圆角矩形 */
        margin: 5px;  /* 列表项间距 */
        padding: 2px;  /* 内容内边距 */
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
list_css = """
    QListWidget {
        background-color: rgba(245, 245, 245, 160); /* 半透明浅灰背景 */
        border: none;  /* 去掉默认边框 */
        outline: none; /* 去掉焦点虚线 */
        padding: 2px;  /* 内边距 */
    }

    /* 列表项的样式 */
    QListWidget::item {
        background-color: rgba(255,255,255,80);  /* 列表项背景色 */
        border-radius: 10px;  /* 圆角矩形 */
        margin: 5px;  /* 列表项间距 */
        padding: 0px;  /* 内容内边距 */
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
button_css = """
background-color: #5ca0d1;
color: white; 
padding: 10px;
"""


def init_user_info(user_info):
    global uid, username, gender, birthday, user_profile_picture_path
    uid = user_info[0]
    username = user_info[1]
    gender = user_info[2]
    birthday = user_info[3]
    user_profile_picture_path = user_info[4]


class Profile(QWidget):
    clicked = pyqtSignal()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap(profile_path)
        painter.drawPixmap(self.rect(), pixmap)

    def __init__(self, user_info):
        super().__init__()
        init_user_info(user_info)

        self.setWindowTitle("欢迎回来 " + str(username) + "!")
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
        self.avatar = QLabel(self)
        self.avatar. \
            setPixmap(QPixmap(user_profile_picture_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.avatar.setAlignment(Qt.AlignCenter)
        self.left_panel.addWidget(self.avatar)
        self.avatar.mousePressEvent = self.click_event

        # 消息按钮
        self.message_button = QPushButton("主页")
        self.message_button.setStyleSheet(button_css)
        self.message_button.clicked.connect(self.show_message_list)
        self.left_panel.addWidget(self.message_button)

        # 好友按钮
        self.friends_button = QPushButton("好友")
        self.friends_button.setStyleSheet(button_css)
        self.friends_button.clicked.connect(self.show_friends_list)
        self.left_panel.addWidget(self.friends_button)

        # 群组按钮
        self.groups_button = QPushButton("群组")
        self.groups_button.setStyleSheet(button_css)
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
        self.friends_list.setStyleSheet(list_css)
        self.search_bar_layout = QHBoxLayout()  # 搜索布局
        self.search_input = QLineEdit(self)  # 搜索输入框
        self.search_input.setPlaceholderText("请输入用户ID或邮箱")
        self.search_input.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        self.search_bar_layout.addWidget(self.search_input)
        self.search_button = QPushButton("搜索", self)  # 搜索按钮
        self.search_button.setStyleSheet("padding: 5px; font-size: 14px;")
        self.search_bar_layout.addWidget(self.search_button)
        self.friends_layout = QVBoxLayout()  # 好友列表布局
        self.friends_layout.addLayout(self.search_bar_layout)  # 添加搜索布局到好友布局
        self.friends_layout.addWidget(self.friends_list)  # 添加好友列表到好友布局
        self.friends_widget = QWidget(self)  # 好友列表整体容器
        self.friends_widget.setLayout(self.friends_layout)
        self.content_stack.addWidget(self.friends_widget)  # 替换原来的好友列表

        # 群组列表
        self.groups_list = QListWidget()
        self.groups_list.setStyleSheet(msg_css)
        self.search_bar_layout_2 = QHBoxLayout()  # 搜索布局
        self.search_input_2 = QLineEdit(self)  # 搜索输入框
        self.search_input_2.setPlaceholderText("请输入用户ID或邮箱")
        self.search_input_2.setStyleSheet("padding: 5px; font-size: 14px; border-radius: 5px;")
        self.search_bar_layout_2.addWidget(self.search_input_2)
        self.search_button_2 = QPushButton("搜索", self)  # 搜索按钮
        self.search_button_2.setStyleSheet("padding: 5px; font-size: 14px;")
        self.search_bar_layout_2.addWidget(self.search_button_2)
        self.search_button_3 = QPushButton("创建群聊", self)  # 搜索按钮
        self.search_button_3.setStyleSheet("padding: 5px; font-size: 14px;")
        self.search_bar_layout_2.addWidget(self.search_button_3)
        self.groups_layout = QVBoxLayout()  # 好友列表布局
        self.groups_layout.addLayout(self.search_bar_layout_2)  # 添加搜索布局到好友布局
        self.groups_layout.addWidget(self.groups_list)  # 添加好友列表到好友布局
        self.groups_widget = QWidget(self)  # 好友列表整体容器
        self.groups_widget.setLayout(self.groups_layout)
        self.content_stack.addWidget(self.groups_widget)  # 替换原来的好友列表

        # 通知列表
        self.notice_list = QListWidget()
        self.notice_list.setStyleSheet(msg_css)
        self.content_stack.addWidget(self.notice_list)

        # 通知按钮
        self.notice_button = QPushButton("通知")
        self.notice_button.setStyleSheet(button_css)
        self.notice_button.clicked.connect(self.show_notice_list)
        self.left_panel.addWidget(self.notice_button)

        # 默认显示消息列表
        self.show_message_list()

        # 添加右侧内容区到主布局
        main_layout.addWidget(self.content_stack)

        # 填充一些测试数据
        self.populate_sample_data()

    def update_info(self, user_info):
        init_user_info(user_info)
        self.setWindowTitle("欢迎回来 " + str(username) + " !")
        self.avatar. \
            setPixmap(QPixmap(user_profile_picture_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_message_list(self):
        self.content_stack.setCurrentWidget(self.message_list)

    def show_friends_list(self):
        self.content_stack.setCurrentWidget(self.friends_widget)

    def show_groups_list(self):
        self.content_stack.setCurrentWidget(self.groups_widget)

    def show_notice_list(self):
        self.content_stack.setCurrentWidget(self.notice_list)

    def populate_sample_data(self):
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

    def click_event(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 触发信号


class FriendItem(QWidget):
    status = "0"

    def __init__(self, user_name, avatar_path, status="4", parent=None):
        super().__init__(parent)
        self.status = status
        self.action_widget = QPushButton("", self)
        self.action_widget.setVisible(False)

        # 主布局管理器（水平布局）
        main_layout = QHBoxLayout(self)

        # 用户头像部分
        avatar_label = QLabel(self)
        avatar_label.setPixmap(QPixmap(avatar_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 设置头像大小
        avatar_label.setFixedSize(80, 80)  # 确保头像大小固定
        main_layout.addWidget(avatar_label)

        # 用户信息和操作部分（垂直布局）
        info_layout = QVBoxLayout()
        username_label = QLabel(user_name, self)
        username_label.setStyleSheet("font-size: 14px; font-weight: bold;")  # 用户名样式
        info_layout.addWidget(username_label)

        # 动态决定显示按钮还是标签
        if self.status == "0":
            self.action_widget = QPushButton("添加好友", self)
            self.action_widget.setFixedSize(100, 30)  # 设置按钮大小
            info_layout.addWidget(self.action_widget)
        elif self.status == "1":
            self.action_widget = QLabel("已添加", self)
            self.action_widget.setStyleSheet("color: gray; font-size: 12px;")
            info_layout.addWidget(self.action_widget)
        elif self.status == "2":
            self.action_widget = QLabel("待确认", self)
            self.action_widget.setStyleSheet("color: orange; font-size: 12px;")
            info_layout.addWidget(self.action_widget)

        info_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 信息居中对齐
        main_layout.addLayout(info_layout)

        # 添加主布局
        self.setLayout(main_layout)


class NoticeItem(QWidget):

    def __init__(self, user_name, avatar_path, msg="", parent=None):
        super().__init__(parent)

        # 主布局管理器（水平布局）
        main_layout = QHBoxLayout(self)

        # 用户头像部分
        avatar_label = QLabel(self)
        avatar_label.setPixmap(QPixmap(avatar_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # 设置头像大小
        avatar_label.setFixedSize(80, 80)  # 确保头像大小固定
        main_layout.addWidget(avatar_label)

        # 用户信息和操作部分（垂直布局）
        info_layout = QVBoxLayout()
        username_label = QLabel(user_name + msg, self)
        username_label.setStyleSheet("font-size: 14px; font-weight: bold;")  # 用户名样式
        info_layout.addWidget(username_label)

        self.action_widget = QPushButton("同意", self)
        self.action_widget.setFixedSize(100, 30)
        self.action_widget2 = QPushButton("拒绝", self)
        self.action_widget2.setFixedSize(100, 30)

        info_layout.addWidget(self.action_widget)
        info_layout.addWidget(self.action_widget2)

        info_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 信息居中对齐
        main_layout.addLayout(info_layout)

        # 添加主布局
        self.setLayout(main_layout)


class GroupItem(QWidget):
    status = "0"

    def __init__(self, group_name, avatar_path="../static/profile_picture01.jpg", status="4", parent=None):
        super().__init__(parent)
        self.status = status
        self.action_widget = QPushButton("", self)
        self.action_widget.setVisible(False)

        # 主布局管理器（水平布局）
        main_layout = QHBoxLayout(self)

        # 用户头像部分
        avatar_label = QLabel(self)
        avatar_label.setPixmap(QPixmap(avatar_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        avatar_label.setFixedSize(80, 80)  # 确保头像大小固定
        main_layout.addWidget(avatar_label)

        # 用户信息和操作部分（垂直布局）
        info_layout = QVBoxLayout()
        group_name_label = QLabel(group_name, self)
        group_name_label.setStyleSheet("font-size: 14px; font-weight: bold;")  # 用户名样式
        info_layout.addWidget(group_name_label)

        # 动态决定显示按钮还是标签
        if self.status == "0":
            self.action_widget = QPushButton("申请入群", self)
            self.action_widget.setFixedSize(100, 30)  # 设置按钮大小
            info_layout.addWidget(self.action_widget)
        elif self.status == "3":
            self.action_widget = QLabel("已加入", self)
            self.action_widget.setStyleSheet("color: gray; font-size: 12px;")
            info_layout.addWidget(self.action_widget)
        elif self.status == "1":
            self.action_widget = QLabel("等待验证", self)
            self.action_widget.setStyleSheet("color: orange; font-size: 12px;")
            info_layout.addWidget(self.action_widget)

        info_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 信息居中对齐
        main_layout.addLayout(info_layout)

        # 添加主布局
        self.setLayout(main_layout)


class MessageItem(QWidget):
    def __init__(self, name=None, avatar_path=None, content=None, time=None, parent=None):
        super(MessageItem, self).__init__(parent)
        self.init_ui(avatar_path, name, time, content)

    def init_ui(self, avatar_path, name, time, content):
        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        avatar_label = QLabel(self)
        avatar_label.setPixmap(QPixmap(avatar_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        avatar_label.setFixedSize(80, 80)  # 确保头像大小固定
        main_layout.addWidget(avatar_label)

        # 右侧信息
        info_layout = QVBoxLayout()
        name_layout = QHBoxLayout()

        # 名称
        name_label = QLabel(name, self)
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        name_layout.addWidget(name_label)

        # 时间
        time_label = QLabel(time, self)
        time_label.setStyleSheet("font-size: 12px; color: gray;")
        time_label.setAlignment(Qt.AlignRight)
        name_layout.addWidget(time_label)

        info_layout.addLayout(name_layout)

        # 内容
        content_label = QLabel(content, self)
        content_label.setStyleSheet("font-size: 12px; color: black;")
        content_label.setWordWrap(True)
        info_layout.addWidget(content_label)

        main_layout.addLayout(info_layout)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sys.exit(app.exec_())

