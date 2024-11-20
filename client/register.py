import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtGui import QPainter


background_path = "../static/login.png"
profile_picture_path = "../static/profile_picture01.jpg"
font_size = "12pt"
font_name = "微软雅黑"
font = "font: " + font_size + "\"" + font_name + "\";"
register_css = font\
        + "border-radius: 10px;"\
        + "background-color:rgba(255,255,255,180);"
x = 50
border_len = 250


class Register(QWidget):
    def paintEvent(self, a: QtGui.QPaintEvent) -> None:
        painter1 = QPainter(self)
        pixmap1 = QPixmap(background_path)
        painter1.drawPixmap(self.rect(), pixmap1)

    def __init__(self, parent=None):
        super(Register, self).__init__(parent)
        self.setWindowTitle('注册')
        self.setGeometry(700, 470, 800, 500)
        self.setFixedWidth(800)
        self.setFixedHeight(500)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(150 + x, 60, 108, 30))
        self.label.setStyleSheet(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(150 + x, 120, 54, 30))
        self.label_2.setStyleSheet(font)
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(150 + x, 180, 54, 30))
        self.label_3.setStyleSheet(font)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(150 + x, 240, 110, 30))
        self.label_4.setStyleSheet(font)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(150 + x, 300, 54, 30))
        self.label_5.setStyleSheet(font)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(150 + x, 360, 110, 30))
        self.label_6.setStyleSheet(font)
        self.label_6.setObjectName("label_6")

        self.register_conBtn = QtWidgets.QPushButton(self)
        self.register_conBtn.setGeometry(QtCore.QRect(150 + x, 420, 100, 50))
        self.register_conBtn.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton:hover{background-color:rgb(20, 114, 208)}"
                                           "QPushButton{background-color:rgb(0, 102, 204)}"
                                           "QPushButton{border:0px}"
                                           "QPushButton{border-radius:10px}"
                                           "QPushButton{padding:2px 4px}"
                                           "QPushButton{font:15pt\"幼圆\"}")
        self.register_conBtn.setObjectName("register_conBtn")

        self.register_canBtn = QtWidgets.QPushButton(self)
        self.register_canBtn.setGeometry(QtCore.QRect(400 + x, 420, 100, 50))
        self.register_canBtn.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton:hover{background-color:rgb(20, 114, 208)}"
                                           "QPushButton{background-color:rgb(0, 102, 204)}"
                                           "QPushButton{border:0px}"
                                           "QPushButton{border-radius:10px}"
                                           "QPushButton{padding:2px 4px}"
                                           "QPushButton{font:15pt\"幼圆\"}")
        self.register_canBtn.setObjectName("register_canBtn")

        self.username = QtWidgets.QLineEdit(self)
        self.username.setGeometry(QtCore.QRect(270 + x, 60, 150, 30))
        self.username.setStyleSheet(register_css)
        self.username.setObjectName("username")
        self.email = QtWidgets.QLineEdit(self)
        self.email.setGeometry(QtCore.QRect(270 + x, 180, border_len, 30))
        self.email.setStyleSheet(register_css)
        self.email.setObjectName("email")
        self.birthday = QtWidgets.QLineEdit(self)
        self.birthday.setGeometry(QtCore.QRect(270 + x, 240, border_len, 30))
        self.birthday.setStyleSheet(register_css)
        self.birthday.setObjectName("birthday")
        self.password = QtWidgets.QLineEdit(self)
        self.password.setGeometry(QtCore.QRect(270 + x, 300, border_len, 30))
        self.password.setStyleSheet(register_css)
        self.password.setObjectName("password")
        self.confirm_password = QtWidgets.QLineEdit(self)
        self.confirm_password.setGeometry(QtCore.QRect(270 + x, 360, border_len, 30))
        self.confirm_password.setStyleSheet(register_css)
        self.confirm_password.setObjectName("confirm_password")

        self.gender = QtWidgets.QComboBox(self)
        self.gender.setGeometry(QtCore.QRect(270 + x, 120, 100, 30))
        self.gender.setStyleSheet(register_css)
        self.gender.setObjectName("gender")
        self.gender.addItem("")
        self.gender.addItem("")
        self.gender.addItem("")
        self.gender.setItemText(0, "男")
        self.gender.setItemText(1, "女")
        self.gender.setItemText(2, "保密")

        self.register_picture = QtWidgets.QPushButton(self)
        self.register_picture.setGeometry(QtCore.QRect(450 + x, 40, 120, 120))
        self.register_picture.setStyleSheet("QPushButton{color:white}"
                                            "QPushButton{border-image:url(../static/profile_picture01.jpg)}"
                                            "QPushButton{border:0px}"
                                            "QPushButton{border-radius:10px}"
                                            )

        self.register_confirm = QtWidgets.QFrame(self)
        self.register_confirm.setGeometry(QtCore.QRect(480 + x, 420, 30, 30))
        self.register_confirm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.register_confirm.setFrameShadow(QtWidgets.QFrame.Raised)

        self.label.setText("用户名")
        self.label_2.setText("性别")
        self.label_3.setText("邮箱")
        self.label_4.setText("出生日期")
        self.label_5.setText("密码")
        self.label_6.setText("确认密码")
        self.register_conBtn.setText("确认")
        self.register_canBtn.setText("取消")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Register()
    ui.show()
    sys.exit(app.exec_())
