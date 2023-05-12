from PyQt5.QtWidgets import *
import sys
import sqlite3

from noteWindow import Ui_NoteWindow
from functional_flashcardWindow import FlashcardWindow


class NoteWindow(QMainWindow, Ui_NoteWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.changes = []

    def initUI(self):
        self.startStudyPushButton.clicked.connect(self.openFlashcardWindow)
        self.saveButton.clicked.connect(self.saveNote)
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        note = cur.execute("""select question, answer from notes where notes_name = ?""",
                           (self.notesName.text(),)).fetchall()
        self.qaTable.setRowCount(len(note) + 1)
        self.qaTable.setHorizontalHeaderLabels(["Question", "Answer"])
        for i in range(len(note)):
            self.qaTable.setItem(i, 0, QTableWidgetItem(note[i][0]))
            self.qaTable.setItem(i, 1, QTableWidgetItem(note[i][1]))
        self.additionalInfoTextEdit.setText(cur.execute("""select additional_info from main_information where 
        name_of_note = ?""", (self.notesName.text(),)).fetchone()[0])
        self.number_of_rows = cur.execute("""select count_of_questions from main_information where name_of_note = ?""",
                                          (self.notesName.text(),)).fetchone()[0]
        self.qaTable.cellChanged.connect(self.cellChanged)

    def openFlashcardWindow(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        if cur.execute("""select count_of_questions from main_information where name_of_note = ?""",
                       (self.notesName.text(),)).fetchone()[0] == 0:
            self.msg = QMessageBox()
            self.msg.setIcon(QMessageBox.Warning)
            self.msg.setText("There are no questions in this note. Add questions to the note or save changes.")
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
        else:
            self.window_flashcard = FlashcardWindow()
            self.window_flashcard.notesName.setText(self.notesName.text())
            self.window_flashcard.initUI()
            self.window_flashcard.show()

    def cellChanged(self, row, column):
        if row not in self.changes:
            self.changes.append(row)
        if row == self.number_of_rows:
            self.qaTable.setRowCount(self.qaTable.rowCount() + 1)
            self.number_of_rows += 1

    def saveNote(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        original_number = cur.execute("""select count_of_questions from main_information where name_of_note = ?""",
                                        (self.notesName.text(),)).fetchone()[0]
        for i in self.changes:
            if i < original_number:
                cur.execute("""update notes set question = ?, answer = ? where notes_name = ? and number_qa = ?""",
                            (self.qaTable.item(i, 0).text(), self.qaTable.item(i, 1).text(), self.notesName.text(), i))
            else:
                cur.execute("""insert into notes values (?, ?, ?, ?)""",
                            (self.notesName.text(), i, ("" if self.qaTable.item(i, 0) is None else self.qaTable.item(i, 0).text()),
                             ("" if self.qaTable.item(i, 1) is None else self.qaTable.item(i, 1).text())))
            cur.execute("""update main_information set additional_info = ?, count_of_questions = ? where name_of_note = ?""",
                        (self.additionalInfoTextEdit.toPlainText(), self.number_of_rows, self.notesName.text()))
        con.commit()
        self.changes = []

    def closeEvent(self, event):
        event.ignore()
        self.closeReminder(event)

    def closeReminder(self, event):
        self.msg_close = QMessageBox()
        self.msg_close.setIcon(QMessageBox.Warning)
        self.msg_close.setText("Do you want to save changes to the note before closing?")
        self.msg_close.setWindowTitle("Save changes")
        self.msg_close.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        self.result = self.msg_close.exec_()
        if self.result == QMessageBox.Save:
            self.saveNote()
            event.accept()
        elif self.result == QMessageBox.Discard:
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NoteWindow()
    win.show()
    sys.exit(app.exec_())
