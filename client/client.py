import sys
import socket
from functools import partial
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox
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
from profile import GroupItem
from profile import MessageItem
from edit import Picture
from edit import ProfileEditor
from chat import Chat
from group import CreateGroupChatPage

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
    init_group_list()
    init_message_list()
    profile.show()
    profile.notice_button.clicked.connect(lambda: init_notice_list)
    profile.message_button.clicked.connect(lambda: init_message_list)

    global profile_editor
    profile_editor = ProfileEditor(user_info)
    profile_editor.clicked.connect(click_user_edit_picture)
    profile_editor.save_button.clicked.connect(update_user_info)

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


def init_message_list():
    profile.message_list.clear()
    msg = "0021" + ";" + user_info[0]
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";;")

    if response[0] != "1":
        return

    response = response[1:]
    p = 6
    for i in range((len(response) + 1) // p):
        flag = response[i * 6]
        iden = response[i * 6 + 1]
        name = response[i * 6 + 2]
        picture_ = response[i * 6 + 3]
        message = response[i * 6 + 4]
        send_time = response[i * 6 + 5]
        if flag == "0":
            item = MessageItem(name, picture_, message, send_time)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小
            list_item.setData(QtCore.Qt.UserRole, iden)
            list_item.setData(QtCore.Qt.UserRole + 1, name)
            list_item.setData(QtCore.Qt.UserRole + 2, picture_)

            profile.message_list.addItem(list_item)
            profile.message_list.setItemWidget(list_item, item)
        else:
            pass
    profile.message_list.itemDoubleClicked.connect(item_double_click)


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
                item.user_id = response[1]
                list_item = QListWidgetItem()
                list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小
                list_item.setData(QtCore.Qt.UserRole, response[1])
                list_item.setData(QtCore.Qt.UserRole + 1, response[2])
                list_item.setData(QtCore.Qt.UserRole + 2, response[5])

                profile.friends_list.addItem(list_item)
                profile.friends_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容
        # 绑定事件
        profile.friends_list.itemDoubleClicked.connect(item_double_click)


def click_group_search():
    gid = profile.search_input.text()
    msg = "0012" + ";" + str(gid)
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    profile.groups_list.clear()
    profile.search_button_2.setText("取消")
    profile.search_button_2.clicked.disconnect()
    profile.search_button_2.clicked.connect(init_group_list)
    if response[0] == "1":
        group_name = response[2]
        group_picture = response[3]
        msg = "0019" + ";" + str(user_info[0]) + ";" + gid
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        if response[0] == "1":
            status = response[1]
            print(status)
            item = GroupItem(group_name, group_picture, status)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小

            if status == "0":
                item.action_widget.clicked.connect(lambda: add_group(user_info[0], gid))

            # 添加到QListWidget
            profile.friends_list.addItem(list_item)
            profile.friends_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容


def init_group_list():
    profile.search_button_2.clicked.connect(click_group_search)
    profile.search_button_2.clicked.disconnect()
    profile.search_button_2.clicked.connect(click_group_search)
    profile.search_button_3.clicked.connect(create_group)
    profile.search_button_3.clicked.disconnect()
    profile.search_button_3.clicked.connect(create_group)
    profile.search_button_2.setText("搜索")
    profile.search_input_2.clear()
    profile.groups_list.clear()

    msg = "0017" + ";" + user_info[0] + ";" + "3"
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    print(response)

    if response[0] == "1":
        response = response[1:]
        for group_id in response:
            msg = "0012" + ";" + str(group_id)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")
            if response[0] == "1":
                item = GroupItem(response[2], response[4])
                list_item = QListWidgetItem()
                list_item.setSizeHint(item.sizeHint())  # 设置列表项的大小
                list_item.setData(QtCore.Qt.UserRole, response[1])
                list_item.setData(QtCore.Qt.UserRole + 1, response[2])
                list_item.setData(QtCore.Qt.UserRole + 2, response[3])
                list_item.setData(QtCore.Qt.UserRole + 3, response[4])

                profile.groups_list.addItem(list_item)
                profile.groups_list.setItemWidget(list_item, item)
        # 绑定事件
        profile.groups_list.itemDoubleClicked.connect(group_item_double_click)


def create_group():
    msg = "0004" + ";" + user_info[0] + ";" + "3"
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    if response[0] == "1":
        print(1)
        response = response[1:]
        users = []
        for friend_id in response:
            msg = "0003" + ";" + friend_id
            print(msg)
            client.sendall(msg.encode())
            friend_info = client.recv(4096).decode()
            friend_info = friend_info.split(";")
            user = dict()
            user["uid"] = friend_info[1]
            user["username"] = friend_info[2]
            user["avatar"] = friend_info[5]
            users.append(user)
        global create_group_window
        create_group_window = CreateGroupChatPage(users)
        create_group_window.cancel_button.clicked.connect(lambda: create_group_window.close())
        create_group_window.create_button.clicked.connect(lambda: send_create_group_msg(create_group_window))
        create_group_window.show()

        def send_create_group_msg(group_window):
            group_name = group_window.search_input.text()
            if group_name == "":
                group_name = "默认群聊"
            selected_users = [
                item.data(QtCore.Qt.UserRole) for item in group_window.user_list.findItems("", Qt.MatchContains)
                if item.checkState() == Qt.Checked
            ]

            send_msg = "0015" + ";" + user_info[0] + ";" + group_name + ";" + user_info[4]
            print(send_msg)
            client.sendall(send_msg.encode())
            result = client.recv(4096).decode()
            result = result.split(";")

            if result[0] != "1":
                QMessageBox.information(
                    group_window, "失败", f"群聊 '{group_name}' 创建失败"
                )
                return
            group_id = result[1]

            for invite_user in selected_users:
                send_msg = "0016" + ";" + group_id + ";" + user_info[0] + ";" + invite_user
                print(send_msg)
                client.sendall(send_msg.encode())
                result = client.recv(4096).decode()
                result.split(";")

            QMessageBox.information(
                group_window, "成功", f"群聊 '{group_name}' 创建成功！"
            )

            for index in range(group_window.user_list.count()):
                group_window.user_list.item(index).setCheckState(Qt.Unchecked)

            group_window.close()
            init_group_list()

    else:
        print("创建群聊失败")


def group_item_double_click(selected_item):
    user_id = user_info[0]
    group_id = selected_item.data(QtCore.Qt.UserRole)
    user_name = user_info[1]
    group_name = selected_item.data(QtCore.Qt.UserRole + 1)
    user_picture = user_info[4]
    group_picture = selected_item.data(QtCore.Qt.UserRole + 3)

    msg = "0013" + ";" + group_id + ";" + "3"
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    if response.split(";")[0] != "1":
        return

    group_member = response.split(";")[1:]
    print(response)
    group_member_info = []
    for member_id in group_member:
        msg = "0003" + ";" + member_id
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        if response[0] != "1":
            return
        group_member_info.append([response[5], response[1], response[2]])

    chat_window = Chat([user_id, group_id, user_name, group_name], group_member_info)

    group_user_info = dict()
    group_user_name_info = dict()
    for user in group_member:
        msg = "0003" + ";" + user_id
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";")
        group_user_info[user] = str(response[5])
        group_user_name_info[user] = str(response[2])

    msg = "0014" + ";" + group_id
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";;")
    print(response)

    if response[0] == "1":
        response = response[1:]
        chat_window.fill_group_message(response, group_user_info, group_user_name_info)
        chat_window.msg_len = len(response)

        def send_message(chat):
            send_msg = "0020" + ";;" + user_id + ";;" + group_id + ";;" + chat.textEdit.toHtml() + " "
            chat.textEdit.clear()
            print(send_msg)
            client.sendall(send_msg.encode())
            send_response = client.recv(4096).decode()
            send_response.split(";;")

        chat_window.send.clicked.connect(lambda: send_message(chat_window))

        chat_window.show()

        chat_window.timer.timeout.\
            connect(lambda: group_auto_update(chat_window, user_id, group_id, group_user_info, group_user_name_info))
        chat_window.timer.start(1000)
    else:
        print("群聊窗口打开失败")


def item_double_click(selected_item):
    user_id = user_info[0]
    friend_id = selected_item.data(QtCore.Qt.UserRole)
    user_name = user_info[1]
    friend_name = selected_item.data(QtCore.Qt.UserRole + 1)
    user_picture = user_info[4]
    friend_picture = selected_item.data(QtCore.Qt.UserRole + 2)
    # chat_window.show()
    chat_window = Chat([user_id, friend_id, user_name, friend_name])

    msg = "0010" + ";;" + user_id + ";;" + friend_id
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";;")

    if response[0] == "1":
        response = response[1:]
        chat_window.fill_message(response)
        chat_window.msg_len = len(response)

        def send_message(chat):
            send_msg = "0011" + ";;" + user_id + ";;" + friend_id + ";;" + chat.textEdit.toHtml() + " "
            chat.textEdit.clear()
            print(send_msg)
            client.sendall(send_msg.encode())
            send_response = client.recv(4096).decode()
            send_response.split(";;")

        chat_window.send.clicked.connect(lambda: send_message(chat_window))

        chat_window.show()

        chat_window.fill_message(response, user_picture, friend_picture)

        auto_update(chat_window, user_id, friend_id, user_picture, friend_picture)
        chat_window.timer.timeout.\
            connect(lambda: auto_update(chat_window, user_id, friend_id, user_picture, friend_picture))
        chat_window.timer.start(1000)
    else:
        print("聊天窗口打开失败")


def auto_update(chat, uid, fid, up, fp):
    if chat.isVisible():
        msg = "0010" + ";;" + uid + ";;" + fid
        print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";;")
        response = response[1:]
        if len(response) != chat.msg_len:
            chat.fill_message(response, up, fp)
            chat.msg_len = len(response)
    else:
        chat.timer.timeout.disconnect()


def group_auto_update(chat, uid, gid, info, name_info):
    if chat.isVisible():
        msg = "0014" + ";" + gid
        # print(msg)
        client.sendall(msg.encode())
        response = client.recv(4096).decode()
        response = response.split(";;")
        response = response[1:]
        if len(response) != chat.msg_len:
            chat_window.fill_group_message(response, info, name_info)
            chat.msg_len = len(response)
    else:
        chat.timer.timeout.disconnect()


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

            item = NoticeItem(friend_name, friend_picture, " 请求添加好友")
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())

            item.action_widget.clicked.connect(lambda: handel_add_friend(user_info[0], friend_uid, "1"))
            item.action_widget2.clicked.connect(lambda: handel_add_friend(user_info[0], friend_uid, "0"))
            profile.notice_list.addItem(list_item)
            profile.notice_list.setItemWidget(list_item, item)  # 将自定义的FriendItem作为列表项的内容

    msg = "0017" + ";" + user_info[0] + ";" + "2"
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")

    if response[0] == "1":
        response = response[1:]
        for group_id in response:
            msg = "0012" + ";" + str(group_id)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")

            if response[0] != "1":
                continue

            group_name = response[2]
            owner_id = response[3]
            group_picture = response[4]

            msg = "0003" + ";" + str(owner_id)
            print(msg)
            client.sendall(msg.encode())
            response = client.recv(4096).decode()
            response = response.split(";")

            if response[0] != "1":
                continue

            owner_name = response[2]

            item = NoticeItem(owner_name, group_picture, f" 邀请你加入群聊 {group_name} !")
            list_item = QListWidgetItem()
            list_item.setSizeHint(item.sizeHint())

            item.action_widget.clicked.connect(lambda: handel_add_group(user_info[0], group_id, "1"))
            item.action_widget2.clicked.connect(lambda: handel_add_group(user_info[0], group_id, "2"))
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


def add_group(user_id, group_id):
    msg = "0018" + ";" + user_id + ";" + group_id + ";" + "4"
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
    click_group_search()


def get_picture(row, col):
    global user_info
    user_info[4] = picture_root_path + str(row * 3 + col) + suffix
    profile.update_info(user_info)
    profile_editor.update_info(user_info)
    picture.close()


def update_user_info():
    new_username = profile_editor.nickname_input.text()
    new_gender = profile_editor.gender_input.currentText()
    new_birthday = profile_editor.birthday_input.text()
    new_picture = user_info[4]

    msg = "0009" + ";" + user_info[0] + ";" + new_username + ";"\
        + new_gender + ";" + new_birthday + ";" + new_picture
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    if response[0] == "1":
        tip_page.label.setText("修改成功")
        tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        tip_window.show()
    else:
        warn_page.warn_label.setText("修改失败")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    profile.update_info(user_info)


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
        global profile_editor
        profile_editor = ProfileEditor(user_info)
    else:
        warn_page.warn_label.setText("添加失败")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    profile_refresh()


def handel_add_group(user_id, group_id, op="0"):
    msg = "0018" + ";" + user_id + ";" + group_id + ";" + op
    print(msg)
    client.sendall(msg.encode())
    response = client.recv(4096).decode()
    response = response.split(";")
    if response[0] == "1":
        tip_page.label.setText("添加成功")
        tip_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        tip_window.show()
        global profile_editor
        profile_editor = ProfileEditor(user_info)
    else:
        warn_page.warn_label.setText("添加失败")
        warn_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        warn_window.show()
    profile_refresh()


def profile_refresh():
    init_notice_list()
    init_friend_list()
    init_group_list()


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

    # chat_window = Chat()

    create_group_window = CreateGroupChatPage({})

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
