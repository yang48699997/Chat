import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRect


background_path = "../static/login.png"
font_size = "12pt"
font_name = "微软雅黑"
font = "font: " + font_size + "\"" + font_name + "\";"
login_css = font\
        + "border-radius: 10px;"\
        + "background-color:rgba(255,255,255,180);"


class Login(QWidget):
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = QPixmap(background_path)
        painter.drawPixmap(self.rect(), pixmap)

    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setWindowTitle('登录')

        self.setGeometry(700, 470, 800, 500)
        self.setFixedWidth(800)
        self.setFixedHeight(500)

        self.login_usr = QLineEdit(self)
        self.login_usr.setGeometry(QRect(220, 100, 380, 50))
        self.login_usr.setInputMask("")
        self.login_usr.setText("")
        self.login_usr.setObjectName("login_usr")
        self.login_usr.setStyleSheet(login_css)
        self.login_pwd = QLineEdit(self)

        self.login_pwd.setGeometry(QRect(220, 200, 380, 50))
        self.login_pwd.setObjectName("login_pwd")
        self.login_pwd.setEchoMode(QLineEdit.Password)
        self.login_pwd.setStyleSheet(login_css)

        self.login_loginBtn = QtWidgets.QPushButton(self)
        self.login_loginBtn.setGeometry(QRect(240, 310, 150, 50))
        self.login_loginBtn.setStyleSheet("QPushButton{color:white}"
                                          "QPushButton:hover{background-color:rgb(20, 114, 208)}"
                                          "QPushButton{background-color:rgb(0, 102, 204)}"
                                          "QPushButton{border:0px}"
                                          "QPushButton{border-radius:10px}"
                                          "QPushButton{padding:2px 4px}"
                                          "QPushButton{font:15pt\"幼圆\"}")
        self.login_loginBtn.setObjectName("login_loginBtn")

        self.login_signBtn = QtWidgets.QPushButton(self)
        self.login_signBtn.setGeometry(QtCore.QRect(430, 310, 150, 50))
        self.login_signBtn.setStyleSheet("QPushButton{color:white}"
                                         "QPushButton:hover{background-color:rgb(20, 114, 208)}"
                                         "QPushButton{background-color:rgb(0, 102, 204)}"
                                         "QPushButton{border:0px}"
                                         "QPushButton{border-radius:10px}"
                                         "QPushButton{padding:2px 4px}"
                                         "QPushButton{font:15pt\"幼圆\"}")
        self.login_signBtn.setObjectName("login_signBtn")

        self.login_forgetBtn = QtWidgets.QPushButton(self)
        self.login_forgetBtn.setGeometry(QtCore.QRect(600, 400, 100, 30))
        self.login_forgetBtn.setStyleSheet("QPushButton{color:white}"
                                           "QPushButton:hover{color:blue}"
                                           "QPushButton{background-color:None}"
                                           "QPushButton{border:0px}"
                                           "QPushButton{padding:2px 4px}"
                                           "QPushButton{font:10pt\"幼圆\"}")
        self.login_forgetBtn.setAutoFillBackground(True)
        self.login_forgetBtn.setObjectName("login_forgetBtn")

        _translate = QtCore.QCoreApplication.translate
        self.login_usr.setPlaceholderText(_translate("Dialog", "ID或邮箱"))
        self.login_pwd.setPlaceholderText(_translate("Dialog", "密码"))
        self.login_loginBtn.setText(_translate("Dialog", "登录"))
        self.login_signBtn.setText(_translate("Dialog", "注册"))
        self.login_forgetBtn.setText(_translate("Dialog", "忘记密码?"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    log = Login()
    log.show()
    sys.exit(app.exec_())
