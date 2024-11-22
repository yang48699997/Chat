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
from profile import FriendItem
from profile import NoticeItem
from edit import Picture
from edit import ProfileEditor

ip = "127.0.0.1"
port = 12345
client = socket.socket()
client.connect((ip, port))
# 0 : id, 1 :username, 2 : gender, 3 : birthday, 4 : picture 5 : status
user_info = []
profile_picture_path = "../static/profile_picture01.jpg"
picture_root_path = "../static/profile_picture0"
suffix = ".jpg"


def client_handle():
    global profile
    profile = Profile(user_info)
    # 绑定编辑个人资料页面
    profile.clicked.connect(click_user_profile_picture)
    init_friend_list()
    init_notice_list()
    profile.show()

    global profile_editor
    profile_editor = ProfileEditor(user_info)
    profile_editor.clicked.connect(click_user_edit_picture)

    global picture
    picture.table.cellPressed.connect(get_picture)


def update_profile():
    global profile
    profile = Profile(user_info)
    # 绑定编辑个人资料页面
    profile.clicked.connect(click_user_profile_picture)
    profile.show()


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
        login_refresh()
        login.close()

        client_handle()

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
    elif len(password) < 6 or len(password) > 15:
        register.password.clear()
        register.confirm_password.clear()
        warn_page.warn_label.setText("密码不符合规则")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    else:
        msg = "0000" + ";" + username + ";" + password + ";" + email + ";" + gender + ";"\
              + birthday + ";" + profile_picture_path
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        if response[0] == "1":
            tip_page.label.setText("注册成功")
            tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            tip_window.show()
            register.close()
            login.show()
        else:
            warn_page.warn_label.setText(response[0])
            warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            warn_window.show()
            register_refresh()
        print(response)


def register_cancel():
    register.close()
    register_refresh()
    login.show()


def warn_cancel():
    warn_window.close()


def tip_cancel():
    tip_window.close()


def click_user_profile_picture():
    print("click_user_profile_picture")
    global profile_editor
    profile_editor.show()


def click_user_edit_picture():
    print("click_user_edit_picture")
    global picture
    picture.show()


def click_user_search():
    uid = profile.search_input.text()
    msg = "0003" + ";" + str(uid)
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    profile.friends_list.clear()
    profile.search_button.setText("取消")
    profile.search_button.clicked.disconnect()
    profile.search_button.clicked.connect(init_friend_list)
    if response[0] == "1":
        friend_name = response[2]
        friend_picture = response[5]
        msg = "0008" + ";" + str(user_info[0]) + ";" + str(uid)
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        if response[0] == "1":
            status = response[1]
            print(status)
            item = FriendItem(friend_name, friend_picture, status)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小

            if status == "0":
                item.action_widget.clicked.connect(lambda: add_friend(user_info[0], uid))

            # 添加到QListWidget
            profile.friends_list.addItem(list_item)
            profile.friends_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容


def init_friend_list():
    profile.search_button.clicked.connect(click_user_search)
    profile.search_button.clicked.disconnect()
    profile.search_button.clicked.connect(click_user_search)
    profile.search_button.setText("搜索")
    profile.search_input.clear()
    profile.friends_list.clear()

    msg = "0004" + ";" + user_info[0] + ";" + "3"
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    if response[0] == "1":
        response = response[1:]
        for friend_uid in response:
            msg = "0003" + ";" + str(friend_uid)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")
            if response[0] == "1":
                item = FriendItem(response[2], response[5])
                list_item = QListWidgetItem()
                list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小

                profile.friends_list.addItem(list_item)
                profile.friends_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容


def init_notice_list():
    profile.notice_list.clear()
    msg = "0004" + ";" + user_info[0] + ";" + "2"
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    if response[0] == "1":
        response = response[1:]
        for friend_uid in response:
            msg = "0003" + ";" + str(friend_uid)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")

            if response[0] != "1":
                continue

            friend_name = response[2]
            friend_picture = response[5]
            msg = "0008" + ";" + user_info[0] + ";" + str(friend_uid)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")
            print(response)

            if response[0] != "1":
                continue

            item = NoticeItem(friend_name, friend_picture, "请求添加好友")
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())

            item.action_widget.clicked.connect(lambda: handel_add_friend(user_info[0], friend_uid, "1"))
            item.action_widget2.clicked.connect(lambda: handel_add_friend(user_info[0], friend_uid, "0"))
            profile.notice_list.addItem(list_item)
            profile.notice_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容


def add_friend(user_id, friend_id):
    msg = "0005" + ";" + user_id + ";" + friend_id
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    if response[0] == "1":
        tip_page.label.setText("添加成功")
        tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        tip_window.show()
    else:
        warn_page.warn_label.setText("添加失败")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    click_user_search()


def get_picture(row, col):
    global user_info
    user_info[4] = picture_root_path + str(row * 3 + col) + suffix
    profile.update_info(user_info)
    profile_editor.update_info(user_info)
    picture.close()


def handel_add_friend(user_id, friend_id, op="0"):
    msg = "0006" + ";" + user_id + ";" + friend_id + ";" + op
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    if response[0] == "1":
        tip_page.label.setText("添加成功")
        tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        tip_window.show()
    else:
        warn_page.warn_label.setText("添加失败")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    profile_refresh()


def profile_refresh():
    init_notice_list()
    init_friend_list()


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

    profile_editor = ProfileEditor([""] * 5)
    picture = Picture()

    profile = Profile([""] * 5)

    login.show()

    login.login_signBtn.clicked.connect(login_to_register)

    login.login_loginBtn.clicked.connect(user_login)

    register.register_conBtn.clicked.connect(partial(user_register, ))
    register.register_canBtn.clicked.connect(partial(register_cancel, ))

    warn_page.warn_conBtn.clicked.connect(partial(warn_cancel, ))
    tip_page.conBtn.clicked.connect(partial(tip_cancel, ))

    sys.exit(app.exec_())
