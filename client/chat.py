import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel


n = 6
m = 12
return_id = 0
path = None
background_path = "../static/chat.jpg"
emo_path = "../static/emotions/"
suffix = ".jpg"
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
        pixmap8 = QPixmap(background_path)
        painter8.drawPixmap(self.rect(), pixmap8)

    def __init__(self, parent=None):
        super(Chat, self).__init__(parent)
        group = self
        group.setObjectName("group")
        group.setFixedSize(1300, 920)
        self.id = 72

        # 输入框
        self.textEdit = QtWidgets.QTextEdit(group)
        self.textEdit.setGeometry(QtCore.QRect(10, 700, 950, 180))
        self.textEdit.setStyleSheet(text_css)
        self.textEdit.setObjectName("text_edit")

        # 发送按钮
        self.send = QtWidgets.QPushButton(group)
        self.send.setGeometry(QtCore.QRect(850, 885, 93, 28))
        self.send.setStyleSheet(button_css)
        self.send.setObjectName("send")
        self.send.setToolTip('Enter')
        self.send.setText("发送")

        # 退出按钮
        self.close_button = QtWidgets.QPushButton(group)
        self.close_button.setGeometry(QtCore.QRect(740, 885, 93, 28))
        self.close_button.setStyleSheet(text_css)
        self.close_button.setObjectName('close_button')
        self.close_button.setText("退出")
        self.close_button.raise_()
        self.close_button.clicked.connect(self.close)

        # 竖线
        self.line = QtWidgets.QFrame(group)
        self.line.setGeometry(QtCore.QRect(610, 0, 750, 900))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        # 横线
        self.line_2 = QtWidgets.QFrame(group)
        self.line_2.setGeometry(QtCore.QRect(200, 680, 785, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # 聊天窗口
        self.textBrowser = QtWidgets.QTextBrowser(group)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 950, 670))
        self.textBrowser.setStyleSheet(chat_css)
        self.textBrowser.setObjectName("content")

        # 表情按钮
        self.emo = QtWidgets.QPushButton(group)
        self.emo.setGeometry(QtCore.QRect(15, 670, 40, 25))
        self.emo.setStyleSheet(emo_css)
        self.emo.setObjectName("emo")
        self.emo.setText("表情")

        self.group_info = QtWidgets.QLabel(group)
        self.group_info.setGeometry(QtCore.QRect(1000, 10, 121, 25))
        self.group_info.setStyleSheet(group_info_css)
        self.group_info.setObjectName("group_info")
        self.group_info.setText("成员")

        init_ui(group)
        QtCore.QMetaObject.connectSlotsByName(group)


class Emotion(QWidget):

    def __init__(self):
        super().__init__()

        self.setFixedSize(540, 182)
        self.setWindowTitle('表情')
        self.table = QTableWidget(self)
        self.table.resize(540, 182)

        self.table.setRowCount(n)
        self.table.setColumnCount(m)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        QTableWidget.resizeRowsToContents(self.table)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        for i in range(n):
            for j in range(m):
                label = QLabel(self)
                label.setPixmap(QtGui.QPixmap(emo_path + str(i * m + j) + suffix))
                self.table.setCellWidget(i, j, label)

        self.table.cellPressed.connect(self.get_pos_content)

    def get_pos_content(self, row, col):
        global return_id
        global path
        return_id = int(row) * m + int(col)

        path = emo_path + str(return_id) + suffix
        path = "<img src=" + path + ">"
        print(path)
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    chat = Chat()
    emotion = Emotion()

    chat.show()

    chat.emo.clicked.connect(lambda: emotion.show())
    emotion.table.cellPressed.connect(lambda: chat.textEdit.append(path))

    sys.exit(app.exec_())
