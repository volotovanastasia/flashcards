from PyQt5.QtWidgets import *
import sys
import sqlite3
import csv

from newNoteWindow import Ui_NewNoteWindow
from functional_noteWindow import NoteWindow


class NewNoteWindow(QMainWindow, Ui_NewNoteWindow):
    def __init__(self):
        super().__init__()
        self.additionalInformationTextEdit = ""
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.addFilePushButton.clicked.connect(self.openAddFileDialog)
        self.saveButton.clicked.connect(self.saveNote)

    def openAddFileDialog(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('CSV files (*.csv)')
        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            self.addFilePushButton.setText(selected_file)

    def saveNote(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        if self.noteNameTextEdit.toPlainText() in [x[0] for x in cur.execute("""select name_of_note from main_information""",).fetchall()]:
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage('This name is already taken.\nPlease, enter another name.')
        elif self.noteNameTextEdit.toPlainText() == "Enter the name of the new note":
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage('Please, enter the name of the new note.')
        else:
            if self.addFilePushButton.text() == 'Add file':
                cur.execute("""insert into main_information(name_of_note, additional_info, count_of_questions) values(?, 
                ?, ?)""",
                            (self.noteNameTextEdit.toPlainText(), self.additionalInfoTextEdit.toPlainText(), 0))
            else:
                with open(self.addFilePushButton.text(), 'r') as file:
                    lines = csv.reader(file, delimiter=';')
                    for i in range(len(lines)):
                        if len(lines[i].split(',')) == 1:
                            cur.execute("""insert into notes(notes_name, number_qa, question, answer) 
                            values(?, ?, ?, ?)""",
                                        (self.noteNameTextEdit.toPlainText(), i, lines[i].split(',')[0], ""))
                        else:
                            cur.execute("""insert into notes(notes_name, number_of_string, question, answer) 
                            values(?, ?, ?, ?)""",
                                        (self.noteNameTextEdit.toPlainText(), i, lines[i].split(',')[0],
                                         lines[i].split(',')[1]))
                cur.execute("""insert into main_information(name_of_note, additional_info, count_of_questions) values(?, 
                ?, ?)""",
                            (self.noteNameTextEdit.toPlainText(), self.additionalInfoTextEdit.toPlainText(),
                             len(lines)))
                file.close()
            con.commit()
            self.window_note = NoteWindow()
            self.window_note.notesName.setText(self.noteNameTextEdit.toPlainText())
            self.window_note.additionalInfoTextEdit.setText(self.additionalInfoTextEdit.toPlainText())
            self.window_note.show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NewNoteWindow()
    win.show()
    sys.exit(app.exec_())
