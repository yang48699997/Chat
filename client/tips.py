from PyQt5 import QtCore
from PyQt5 import QtWidgets


class Tips(object):
    def __init__(self):
        self.conBtn = None
        self.label = None

    def setup_ui(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(400, 300)
        dialog.setWindowTitle("")
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(70, 70, 271, 121))
        self.label.setObjectName("label")
        self.conBtn = QtWidgets.QPushButton(dialog)
        self.conBtn.setGeometry(QtCore.QRect(250, 240, 93, 28))
        self.conBtn.setObjectName("conBtn")

        self.get_page(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def get_page(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("dialog", "TextLabel"))
        self.conBtn.setText(_translate("dialog", "确认"))
