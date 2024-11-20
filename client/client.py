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
        profile.show()
    #     globalmanager.flag_tx = eval(back_info[2])
    #     infor1 = infor()
    #     infor1.group_btn.clicked.connect(infor2ag)  # 通讯录跳转到拉取群聊
    #     infor1.deli.clicked.connect(partial(delTreeNodeBtn, infor1))
    #     infor1.tree.doubleClicked.connect(item_click)
    #     infor1.addi.clicked.connect(partial(delgroup, infor1))
    #     infor1.game.clicked.connect(lambda: gp1.show())
    #     # #infor1.game.clicked.connect(lambda: infor1.close())
    #     infor1.txti.clicked.connect(lambda: bot1.show())
    #     tempid = userid
    #     log1.close()
    #     global temp_constuser
    #     x = "A00110;" + userid
    #     new_socket.sendall(x.encode())
    #     back_str = new_socket.recv(4096).decode()
    #     back_info = back_str.split(";")
    #     if back_info[1] == "1":
    #         print(back_info)
    #         frequent_Contacts = eval(back_info[2])
    #         # temp_constuser = frequent_Contacts
    #         for i in frequent_Contacts:
    #             item = QTreeWidgetItem(infor1.root1)
    #             item.setText(0, str(i))  # 工号
    #             item.setText(1, str(frequent_Contacts[i]))  # 部门-名字
    #             item.setToolTip(0, '双击用户发起群聊')
    #             item.setToolTip(1, '双击用户发起群聊')
    #             infor1.tree.addTopLevelItem(infor1.root1)
    #     else:
    #         warn_page.warn_label.setText(back_info[1])
    #         warnWindow.show()
    #     x = "A00111;" + userid
    #     new_socket.sendall(x.encode())
    #     back_str = new_socket.recv(4096).decode()
    #     back_info = back_str.split(";")
    #     print("back_infor", back_info)
    #     if back_info[1] == "1":
    #         frequent_group = eval(back_info[2])
    #         for i in frequent_group:
    #             item = QTreeWidgetItem(infor1.root2)
    #             item.setText(0, str(i[0]))  # 群聊ID
    #             item.setText(1, str(i[1]))  # 群聊名称
    #             item.setToolTip(0, '双击用户发起群聊')
    #             item.setToolTip(1, '双击用户发起群聊')
    #             infor1.tree.addTopLevelItem(infor1.root2)
    #         infor1.show()
    #     else:
    #         warn_page.warn_label.setText(back_info[1])
    #         warnWindow.show()
    #
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    login = Login()
    register = Register()

    warn_window = QDialog()
    warn_page = WarningWindow()
    warn_page.setup_ui(warn_window)

    profile = Profile()

    login.show()

    login.login_signBtn.clicked.connect(login_to_register)
    login.login_loginBtn.clicked.connect(user_login)

    register.register_conBtn.clicked.connect(partial(user_register, ))
    register.register_canBtn.clicked.connect(partial(register_cancel, ))

    warn_page.warn_conBtn.clicked.connect(partial(warn_cancel, ))

    sys.exit(app.exec_())
