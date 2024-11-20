import sys
import socket
from functools import partial
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from login import Login
from register import Register
from warning import WarningWindow
from tips import Tips
from profile import Profile

ip = "127.0.0.1"
port = 12345
client = socket.socket()
client.connect((ip, port))
# 0 : id, 1 :username, 2 : gender, 3 : birthday, 4 : picture
user_info = None
profile_picture_path = "../static/profile_picture01.jpg"


def login_refresh():
    login.login_usr.clear()
    login.login_pwd.clear()


def register_refresh():
    register.username.clear()
    register.email.clear()
    register.birthday.clear()
    register.password.clear()
    register.confirm_password.clear()


def login_to_register():
    register_refresh()
    register.show()
    login_refresh()
    login.close()


def user_login():
    userid = login.login_usr.text()
    password = login.login_pwd.text()
    msg = "0001" + ";" + str(userid) + ";" + str(password)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    print(response)
    if response[0] == "1":
        print("登录成功")
        global user_info
        user_info = response[1:]
        login.close()
        profile.set_user_info(user_info)
        profile.show()

    else:
        warn_page.warn_label.setText(response[0])
        warn_window.show()


def user_register():
    username = register.username.text()
    email = register.email.text()
    birthday = register.birthday.text()
    password = register.password.text()
    conform_password = register.confirm_password.text()
    gender = register.gender.currentText()
    if password != conform_password:
        register.password.clear()
        register.confirm_password.clear()
        warn_page.warn_label.setText("密码与确认密码不一致！")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
        warn_window.show()
    else:
        msg = "0000" + ";" + username + ";" + password + ";" + email + ";" + gender + ";"\
              + birthday + ";" + profile_picture_path + ";"
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        if response[0] == "1":
            tip_page.label.setText("注册成功")
            tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶
            tip_window.show()
            register.close()
            login.show()
        else:
            warn_page.warn_label.setText(response[0])
            register_refresh()
            warn_window.show()
        print(response)


def register_cancel():
    register.close()
    register_refresh()
    login.show()


def warn_cancel():
    warn_window.close()


def tip_cancel():
    tip_window.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    login = Login()
    register = Register()

    warn_window = QDialog()
    warn_page = WarningWindow()
    warn_page.setup_ui(warn_window)

    tip_window = QDialog()
    tip_page = Tips()
    tip_page.setup_ui(tip_window)

    profile = Profile()

    login.show()

    login.login_signBtn.clicked.connect(login_to_register)
    login.login_loginBtn.clicked.connect(user_login)

    register.register_conBtn.clicked.connect(partial(user_register, ))
    register.register_canBtn.clicked.connect(partial(register_cancel, ))

    warn_page.warn_conBtn.clicked.connect(partial(warn_cancel, ))
    tip_page.conBtn.clicked.connect(partial(tip_cancel, ))

    sys.exit(app.exec_())
