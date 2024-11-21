import sys
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtCore import QDate
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel

form_css = """
QWidget {
    background-color: rgb(38, 38, 38); /* 深色背景 */
    color: rgb(205, 205, 205);           /* 字体颜色 */
    font: 14pt "Microsoft YaHei"; /* 字体及大小 */
}

QLabel {
    color: rgb(164, 164, 164); /* 标签文字颜色 */
    font-weight: bold; /* 粗体 */
    margin-bottom: 5px; /* 标签和输入框之间间距 */
}

QLineEdit, QComboBox, QDateEdit {
    background-color: rgb(51, 51, 51); /* 输入框背景 */
    border: 1px solid;  /* 边框颜色 */
    border-radius: 5px; /* 圆角边框 */
    padding: 5px 10px; /* 内边距 */
    color: rgb(205, 205, 205); /* 字体颜色 */
}

QPushButton {
    background-color: rgb(0, 102, 204); /* 按钮背景色 */
    color: #EEEEEE; /* 按钮字体颜色 */
    border: none;
    border-radius: 5px; /* 圆角 */
    padding: 8px 15px; /* 内边距 */
}

QPushButton:pressed {
    background-color: #005E61; /* 按下时颜色 */
}

QComboBox::drop-down {
    border: none; /* 移除下拉箭头的边框 */
}

QComboBox::down-arrow {
    image: url(dropdown.png); /* 可自定义下拉箭头图标 */
}
"""

picture_path = "../static/profile_picture01.jpg"
picture_root_path = "../static/profile_picture0"
suffix = ".jpg"
n = 3
m = 3
uid = None
username = None
gender = None
birthday = None
user_profile_picture_path = None
picture_id = "../static/profile_picture01.jpg"


def init_user_info(user_info):
    global uid, username, gender, birthday, user_profile_picture_path
    uid = user_info[0]
    username = user_info[1]
    gender = user_info[2]
    birthday = user_info[3]
    user_profile_picture_path = user_info[4]


class ProfileEditor(QWidget):
    clicked = pyqtSignal()

    def __init__(self, user_info):
        super().__init__()
        init_user_info(user_info)

        global uid, username, gender, birthday, user_profile_picture_path

        self.setWindowTitle("编辑资料")
        self.setFixedSize(500, 460)
        self.setStyleSheet(form_css)

        # 主布局
        main_layout = QVBoxLayout(self)

        # 用户头像部分
        self.avatar_label = QLabel(self)
        self.avatar_label.setFixedSize(100, 100)
        self.avatar_label.setStyleSheet("border-radius: 50px; background-color: rgba(255, 255, 255, 170)")
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setCursor(Qt.PointingHandCursor)
        self.pixmap = QPixmap(user_profile_picture_path)
        self.avatar_label.setPixmap(self.pixmap.scaled(
            self.avatar_label.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))
        self.avatar_label.mousePressEvent = self.click_event

        avatar_layout = QVBoxLayout()
        avatar_layout.setAlignment(Qt.AlignCenter)
        avatar_layout.addWidget(self.avatar_label)
        main_layout.addLayout(avatar_layout)

        # 表单部分
        form_layout = QGridLayout()

        # ID
        form_layout.addWidget(QLabel("uid"), 0, 0)
        self.user_id = QLabel()
        self.user_id.setText(uid)
        form_layout.addWidget(self.user_id, 0, 1)

        # 昵称
        form_layout.addWidget(QLabel("用户名"), 1, 0)
        self.nickname_input = QLineEdit()
        self.nickname_input.setText(username)
        self.nickname_input.setPlaceholderText("请输入昵称")
        form_layout.addWidget(self.nickname_input, 1, 1)

        # 性别
        form_layout.addWidget(QLabel("性别"), 2, 0)
        self.gender_input = QComboBox()
        self.gender_input.setCurrentText(gender)
        self.gender_input.addItems(["男", "女", "保密"])
        form_layout.addWidget(self.gender_input, 2, 1)

        # 生日
        form_layout.addWidget(QLabel("生日"), 3, 0)
        self.birthday_input = QDateEdit()
        self.birthday_input.setDate(QDate.fromString(birthday, "yyyy-MM-dd"))
        self.birthday_input.setDisplayFormat("yyyy-MM-dd")
        self.birthday_input.setCalendarPopup(True)
        self.birthday_input.setDateRange(QDate(1900, 1, 1), QDate.currentDate())
        form_layout.addWidget(self.birthday_input, 3, 1)

        main_layout.addLayout(form_layout)

        # 按钮部分
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        def update_user_info():
            global uid, username, gender, birthday, user_profile_picture_path
            uid = str(self.user_id.text())
            username = str(self.nickname_input.text())
            gender = str(self.gender_input.currentText())
            birthday = str(self.birthday_input.text())
            user_profile_picture_path = picture_id
            self.close()
            return [uid, username, gender, birthday, user_profile_picture_path]

        self.save_button.clicked.connect(lambda: update_user_info())
        self.cancel_button.clicked.connect(lambda: self.close())

    def click_event(self, event: QMouseEvent):
        print(1)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # 触发信号

    def update_info(self, user_info):
        init_user_info(user_info)
        self.pixmap = QPixmap(user_profile_picture_path)
        self.avatar_label.setPixmap(self.pixmap.scaled(
            self.avatar_label.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        ))
        print(user_profile_picture_path)


class Picture(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedSize(900, 900)
        self.setWindowTitle('头像')

        self.table = QTableWidget(self)
        self.table.setGeometry(0, 0, 900, 900)

        # 设置行和列
        self.table.setRowCount(n)
        self.table.setColumnCount(m)

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        self.table.setColumnWidth(0, 30)
        self.table.setRowHeight(0, 30)

        for i in range(n):
            for j in range(m):
                label = QLabel(self)
                pixmap = QPixmap(picture_root_path + str(i * m + j) + suffix)
                label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.table.setCellWidget(i, j, label)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table.cellPressed.connect(self.get_picture)

    def get_picture(self, row, col):
        global picture_id
        picture_id = picture_root_path + str(row * m + col) + suffix
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    sys.exit(app.exec_())
