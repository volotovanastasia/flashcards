from PyQt5.QtWidgets import *
import sys
import sqlite3

from mainWindow import Ui_MainWindow
from functional_newNoteWindow import NewNoteWindow
from functional_flashcardWindow import FlashcardWindow
from functional_noteWindow import NoteWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.newNotePushButton.clicked.connect(self.openNewNoteWindow)
        self.createNotesAndButtons()

    def openNewNoteWindow(self):
        self.window_crete_new_note_dialog = NewNoteWindow()
        self.window_crete_new_note_dialog.show()

    def createNotesAndButtons(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        notes = cur.execute("""select name_of_note from main_information""").fetchall()
        self.layout = QVBoxLayout()
        for i in range(len(notes)):
            self.note = QLabel(self.scrollAreaWidgetContents)
            self.note.setText(notes[i][0])
            self.note.setGeometry(10, 20 + 50 * i, 521, 40)
            self.studyButton = QPushButton(self.scrollAreaWidgetContents)
            self.studyButton.setText("Study")
            self.studyButton.setGeometry(560, 20 + 50 * i, 113, 32)
            self.studyButton.clicked.connect(lambda checked, name=notes[i][0]: self.openFlashcard(name))
            self.editButton = QPushButton(self.scrollAreaWidgetContents)
            self.editButton.setText("Edit")
            self.editButton.setGeometry(670, 20 + 50 * i, 113, 32)
            self.editButton.clicked.connect(lambda checked, name=notes[i][0]: self.openNote(name))
            self.layout.addWidget(self.note)
            self.layout.addWidget(self.studyButton)
            self.layout.addWidget(self.editButton)
            self.scrollAreaWidgetContents.setLayout(self.layout)

    def openNote(self, name):
        self.noteWindow = NoteWindow()
        self.noteWindow.notesName.setText(name)
        self.noteWindow.initUI()
        self.noteWindow.show()

    def openFlashcard(self, name):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        if cur.execute("""select count_of_questions from main_information where name_of_note = ?""",
                       (name,)).fetchone()[0] == 0:
            self.error_dialog = QErrorMessage()
            self.error_dialog.showMessage('This note is empty.\nPlease, add some questions.')
        else:
            self.flashcardWindow = FlashcardWindow()
            self.flashcardWindow.notesName.setText(name)
            self.flashcardWindow.initUI()
            self.flashcardWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
