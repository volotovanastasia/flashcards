# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newNoteWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewNoteWindow(object):
    def setupUi(self, NewNoteWindow):
        NewNoteWindow.setObjectName("NewNoteWindow")
        NewNoteWindow.setFixedSize(796, 525)
        self.centralwidget = QtWidgets.QWidget(NewNoteWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.additionalInfo = QtWidgets.QLabel(self.centralwidget)
        self.additionalInfo.setGeometry(QtCore.QRect(30, 310, 231, 31))
        self.additionalInfo.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.additionalInfo.setObjectName("additionalInfo")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(660, 413, 113, 32))
        self.saveButton.setObjectName("saveButton")
        self.additionalInfoTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.additionalInfoTextEdit.setGeometry(QtCore.QRect(30, 360, 601, 79))
        self.additionalInfoTextEdit.setObjectName("additionalInfoTextEdit")
        self.noteNameTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.noteNameTextEdit.setGeometry(QtCore.QRect(30, 50, 321, 41))
        self.noteNameTextEdit.setStyleSheet("font: 13pt \".AppleSystemUIFont\";")
        self.noteNameTextEdit.setObjectName("noteNameTextEdit")
        self.addFilePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.addFilePushButton.setGeometry(QtCore.QRect(30, 170, 193, 51))
        self.addFilePushButton.setStyleSheet("font: 18pt \".AppleSystemUIFont\";")
        self.addFilePushButton.setObjectName("addFilePushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 160, 501, 71))
        self.label.setStyleSheet("color: rgb(255, 0, 33)")
        self.label.setObjectName("label")
        NewNoteWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NewNoteWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 24))
        self.menubar.setObjectName("menubar")
        NewNoteWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NewNoteWindow)
        self.statusbar.setObjectName("statusbar")
        NewNoteWindow.setStatusBar(self.statusbar)

        self.retranslateUi(NewNoteWindow)
        QtCore.QMetaObject.connectSlotsByName(NewNoteWindow)

    def retranslateUi(self, NewNoteWindow):
        _translate = QtCore.QCoreApplication.translate
        NewNoteWindow.setWindowTitle(_translate("NewNoteWindow", "Приложение для ведения конспектов и последующего автоматического перехода записей в карточки для заучивания материала"))
        self.additionalInfo.setText(_translate("NewNoteWindow", "Additional Information"))
        self.saveButton.setText(_translate("NewNoteWindow", "Save note"))
        self.noteNameTextEdit.setPlainText(_translate("NewNoteWindow", "Enter the name of the new note"))
        self.addFilePushButton.setText(_translate("NewNoteWindow", "Add file"))
        self.label.setText(_translate("NewNoteWindow", "!!!\n"
"Remember that only the first two columns of your file will be converted into a note.\n"
"The first will be the question, and the second will be the answer\n"
"Upload the file in the format .csv"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewNoteWindow = QtWidgets.QMainWindow()
    ui = Ui_NewNoteWindow()
    ui.setupUi(NewNoteWindow)
    NewNoteWindow.show()
    sys.exit(app.exec_())
