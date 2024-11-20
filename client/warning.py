from PyQt5 import QtCore
from PyQt5 import QtWidgets


class WarningWindow(object):
    def __init__(self):
        self.warn_conBtn = None
        self.warn_label = None

    def setup_ui(self, dialog):
        dialog.setObjectName("Dialog")
        dialog.resize(400, 300)
        
        self.warn_label = QtWidgets.QLabel(dialog)
        self.warn_label.setGeometry(QtCore.QRect(70, 50, 331, 131))
        self.warn_label.setObjectName("warn_label")
        self.warn_conBtn = QtWidgets.QPushButton(dialog)
        self.warn_conBtn.setGeometry(QtCore.QRect(230, 230, 93, 28))
        self.warn_conBtn.setObjectName("warn_conBtn")

        self.get_page(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def get_page(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Dialog", "Warning"))
        self.warn_label.setText(_translate("Dialog", """
        Warning:\n     
        The password does not match the \n 
        confirmation password
        """))
        self.warn_conBtn.setText(_translate("Dialog", "确认"))
