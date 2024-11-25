import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QTextBlockFormat, QTextCharFormat, QColor, QTextImageFormat, QFont
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel


text_css = """
font: 12pt "幼圆";
border: none;
border-radius: 10px;
background-color:rgba(255, 255, 255, 170);
"""
button_css = """
font: 12pt "幼圆";
border: none;
border-radius: 10px;
background-color:rgba(255, 255, 255, 170);
"""
chat_css = """
QWidget {
    font: 12pt "幼圆";
    color: #333333;
    border: none;
    border-radius: 15px;
    background-color: rgba(255, 255, 255, 170);
    padding: 10px;
}
"""
emo_css = """
font: 10pt "宋体";
border: none;
border-radius: 1px;
background-color:rgba(255, 255, 255, 240);
"""
group_info_css = """
font: 12pt "幼圆";
border: none;
border-radius: 10px;
background-color:rgba(255, 255, 255, 0);
"""


def init_ui(group):
    translate_ = QtCore.QCoreApplication.translate
    group.setWindowTitle(translate_("group", "群聊"))


class Chat(QWidget):

    def paintEvent(self, a: QtGui.QPaintEvent) -> None:
        painter8 = QPainter(self)
        pixmap8 = QPixmap(self.background_path)
        painter8.drawPixmap(self.rect(), pixmap8)

    def __init__(self, userinfo=None, parent=None):
        super(Chat, self).__init__(parent)
        if userinfo is None:
            userinfo = ["uid", "fid", "user_name", "friend_name"]
        self.setObjectName("group")
        self.setFixedSize(1300, 920)

        # 初始化属性
        self.n = 6
        self.m = 12
        self.return_id = 0
        self.path = None
        self.background_path = "../static/chat.jpg"
        self.emo_path = "../static/emotions/"
        self.suffix = ".jpg"
        self.dir = dict()
        self.dir[userinfo[0]] = "我"
        self.dir[userinfo[1]] = userinfo[3]
        self.timer = QTimer(self)
        self.msg_len = 0

        # 输入框
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(QtCore.QRect(10, 700, 950, 180))
        self.textEdit.setStyleSheet(text_css)
        self.textEdit.setObjectName("text_edit")

        # 发送按钮
        self.send = QtWidgets.QPushButton(self)
        self.send.setGeometry(QtCore.QRect(850, 885, 93, 28))
        self.send.setStyleSheet(button_css)
        self.send.setObjectName("send")
        self.send.setToolTip('Enter')
        self.send.setText("发送")

        # 退出按钮
        self.close_button = QtWidgets.QPushButton(self)
        self.close_button.setGeometry(QtCore.QRect(740, 885, 93, 28))
        self.close_button.setStyleSheet(text_css)
        self.close_button.setObjectName('close_button')
        self.close_button.setText("退出")
        self.close_button.raise_()
        self.close_button.clicked.connect(self.close)

        # 竖线
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(610, 0, 750, 900))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # 横线
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(200, 680, 785, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # 聊天窗口
        self.textBrowser = QtWidgets.QTextBrowser(self)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 950, 670))
        self.textBrowser.setStyleSheet(chat_css)
        self.textBrowser.setObjectName("content")

        # 表情按钮
        self.emo_button = QtWidgets.QPushButton(self)
        self.emo_button.setGeometry(QtCore.QRect(15, 670, 40, 25))
        self.emo_button.setStyleSheet(emo_css)
        self.emo_button.setObjectName("emo")
        self.emo_button.setText("表情")

        # 现在初始化 Emotion 时传递 Chat 实例
        self.emo = self.Emotion(self)
        self.emo.setVisible(False)

        self.emo_button.clicked.connect(self.toggle_emo)

        self.group_info = QtWidgets.QLabel(self)
        self.group_info.setGeometry(QtCore.QRect(1000, 10, 121, 25))
        self.group_info.setStyleSheet(group_info_css)
        self.group_info.setObjectName("group_info")
        self.group_info.setText("成员")

        init_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def toggle_emo(self):
        if self.emo.isVisible():
            self.emo.setVisible(False)
        else:
            self.emo.move(self.emo_button.x() + self.emo_button.width(), self.emo_button.y() - 200)
            self.emo.raise_()
            self.emo.setVisible(True)

    class Emotion(QWidget):

        def __init__(self, parent=None):
            super().__init__(parent)
            # 保存父类实例
            self.chat_instance = parent
            self.setFixedSize(540, 182)
            self.setWindowTitle('表情')
            self.table = QTableWidget(self)
            self.table.resize(540, 182)

            # 使用父类实例的属性
            self.table.setRowCount(self.chat_instance.n)
            self.table.setColumnCount(self.chat_instance.m)
            self.table.setAlternatingRowColors(True)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            QTableWidget.resizeRowsToContents(self.table)
            self.table.horizontalHeader().setVisible(False)
            self.table.verticalHeader().setVisible(False)

            for i in range(self.chat_instance.n):
                for j in range(self.chat_instance.m):
                    label = QLabel(self)
                    label.setPixmap(QtGui.QPixmap(
                        self.chat_instance.emo_path + str(i * self.chat_instance.m + j) + self.chat_instance.suffix))
                    self.table.setCellWidget(i, j, label)

            self.table.cellPressed.connect(self.get_pos_content)

        def get_pos_content(self, row, col):
            self.chat_instance.return_id = int(row) * self.chat_instance.m + int(col)
            self.chat_instance.path = self.chat_instance.emo_path + str(
                self.chat_instance.return_id) + self.chat_instance.suffix
            self.chat_instance.path = "<img src=" + self.chat_instance.path + ">"
            self.insert_emoji()
            self.close()

        def insert_emoji(self):
            current_text = self.chat_instance.textEdit.toHtml()
            new_text = current_text + self.chat_instance.path
            self.chat_instance.textEdit.clear()
            self.chat_instance.textEdit.append(new_text)  # 将表情插入到文本框中

    def fill_message(self, records=None, user_picture=None, friend_picture=None):
        if records is None:
            records = []

        p = 5
        tot = len(records) // p
        self.textBrowser.clear()

        cursor = self.textBrowser.textCursor()

        for i in range(tot):
            sender = self.dir[records[p * i]]  # 消息发送者（我/朋友）
            time = records[p * i + 3]  # 时间
            content = records[p * i + 2]  # 消息内容

            # 消息块格式
            block_format = QTextBlockFormat()
            block_format.setLineHeight(150, QTextBlockFormat.ProportionalHeight)

            # 消息内容格式
            content_format = QTextCharFormat()
            content_format.setFontPointSize(12)
            content_format.setForeground(QColor("#000000"))

            # 时间格式
            time_format = QTextCharFormat()
            time_format.setFontPointSize(10)
            time_format.setForeground(QColor("#999"))
            cursor.insertText("\n")
            if sender == "我":
                block_format.setAlignment(Qt.AlignRight)

                cursor.setBlockFormat(block_format)
                cursor.setCharFormat(content_format)

                # 使用 insertHtml 来插入消息内容，支持富文本和图片
                cursor.insertHtml(content)

                if user_picture:
                    # 创建 QTextImageFormat 对象并设置图片
                    image_format = QTextImageFormat()
                    image_format.setName(user_picture)  # 设置图片路径
                    image_format.setWidth(60)  # 设置宽度
                    image_format.setHeight(60)  # 设置高度
                    cursor.insertImage(image_format)  # 插入图片

                cursor.insertText("\n")
                cursor.setCharFormat(time_format)
                cursor.insertText(time)
                cursor.insertBlock()

            else:
                block_format.setAlignment(Qt.AlignLeft)

                if friend_picture:
                    image_format = QTextImageFormat()
                    image_format.setName(friend_picture)  # 设置图片路径
                    image_format.setWidth(60)  # 设置宽度
                    image_format.setHeight(60)  # 设置高度
                    cursor.insertImage(image_format)  # 插入图片

                cursor.setBlockFormat(block_format)
                cursor.setCharFormat(content_format)

                # 使用 insertHtml 来插入消息内容，支持富文本和图片
                cursor.insertHtml(content)
                cursor.insertText("\n")
                cursor.setCharFormat(time_format)
                cursor.insertText(time)
                cursor.insertBlock()

        self.textBrowser.setTextCursor(cursor)

    def fill_group_message(self, records=None, user_info=None, user_name_info=None):
        if records is None:
            records = []

        p = 3
        tot = len(records) // p
        self.textBrowser.clear()

        cursor = self.textBrowser.textCursor()

        for i in range(tot):
            sender = records[p * i]  # 消息发送者（我/朋友）
            time = records[p * i + 2]  # 时间
            content = records[p * i + 1]  # 消息内容

            # 消息块格式
            block_format = QTextBlockFormat()
            block_format.setLineHeight(150, QTextBlockFormat.ProportionalHeight)

            # 消息内容格式
            content_format = QTextCharFormat()
            content_format.setFontPointSize(12)
            content_format.setForeground(QColor("#000000"))

            # 时间格式
            time_format = QTextCharFormat()
            time_format.setFontPointSize(10)
            time_format.setForeground(QColor("#999"))
            cursor.insertText("\n")
            print(f"-------- {self.dir} -------------")
            if self.dir.get(sender) == "我":
                block_format.setAlignment(Qt.AlignRight)

                cursor.setBlockFormat(block_format)
                cursor.setCharFormat(content_format)

                # 使用 insertHtml 来插入消息内容，支持富文本和图片
                cursor.insertHtml(content)

                # 创建 QTextImageFormat 对象并设置图片
                image_format = QTextImageFormat()
                image_format.setName(user_info[sender])  # 设置图片路径
                image_format.setWidth(60)  # 设置宽度
                image_format.setHeight(60)  # 设置高度
                cursor.insertImage(image_format)  # 插入图片

                cursor.insertText("\n")
                cursor.setCharFormat(time_format)
                cursor.insertText(time)
                cursor.insertBlock()

            else:
                block_format.setAlignment(Qt.AlignLeft)

                image_format = QTextImageFormat()
                image_format.setName(user_info[sender])  # 设置图片路径
                image_format.setWidth(60)  # 设置宽度
                image_format.setHeight(60)  # 设置高度
                cursor.insertImage(image_format)  # 插入图片

                # 插入用户名
                username_format = QTextCharFormat()  # 创建格式对象
                username_format.setFontWeight(QFont.Bold)  # 设置字体加粗
                username_format.setForeground(QColor("#0078D4"))  # 设置用户名颜色（蓝色）
                cursor.setCharFormat(username_format)  # 应用格式

                cursor.insertText(f"{user_name_info[sender]}\n")  # 插入用户名并换行

                cursor.setBlockFormat(block_format)
                cursor.setCharFormat(content_format)

                # 使用 insertHtml 来插入消息内容，支持富文本和图片
                cursor.insertHtml(content)
                cursor.insertText("\n")
                cursor.setCharFormat(time_format)
                cursor.insertText(time)
                cursor.insertBlock()

        self.textBrowser.setTextCursor(cursor)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    chat = Chat()
    chat.show()

    sys.exit(app.exec_())
