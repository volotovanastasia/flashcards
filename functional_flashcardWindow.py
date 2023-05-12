from PyQt5.QtWidgets import *
import sys
import sqlite3
import random

from flashcardWindow import Ui_FlashcardWindow


class FlashcardWindow(QMainWindow, Ui_FlashcardWindow):
    def __init__(self):
        super().__init__()
        self.msg = QMessageBox()
        self.msg.setText("Should I show the cards in random order?")
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.result = self.msg.exec_()
        self.random_list = []
        self.number_of_question = 0
        self.order = False
        self.setupUi(self)

    def initUI(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        n = (1 if (cur.execute("""select count_of_questions from main_information where name_of_note = ?""",
                               (self.notesName.text(),)).fetchone()) is None else cur.execute(
            """select count_of_questions from main_information where name_of_note = ?""",
            (self.notesName.text(),)).fetchone()[0] - 1)
        self.rotationPushButton.clicked.connect(self.rotateFlashcard)
        self.nextPushButton.clicked.connect(self.showNext)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(n)
        self.progressBar.setMinimum(0)
        self.order = (True if self.result == QMessageBox.Yes else False)
        if self.order:
            self.random_list = list(range(0, n + 1))
            random.shuffle(self.random_list)
            self.flashcard.setText("Question\n" + ("" if cur.execute("""select question from notes where number_qa = ?
             and notes_name = ?""", (self.random_list[self.number_of_question], self.notesName.text())).fetchone() is None
                                                   else cur.execute(
                """select question from notes where number_qa = ? and notes_name = ?""",
                (self.random_list[self.number_of_question], self.notesName.text())).fetchone()[0]))
        else:
            self.flashcard.setText("Question\n" + ("" if cur.execute("""select question from notes where number_qa = ?
                and notes_name = ?""", (self.number_of_question, self.notesName.text())).fetchone() is None else cur.
                                                         execute("""select question from notes where number_qa = ? 
                                                         and notes_name = ?""", (self.number_of_question,
                                                                                 self.notesName.text())).fetchone()[0]))

    def rotateFlashcard(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        if self.flashcard.text()[0] == 'Q':
            self.flashcard.setText(
                "Answer\n" + ("" if cur.execute("""select answer from notes where number_qa = ? and notes_name = ?""",
                                                (
                                                self.number_of_question, self.notesName.text())).fetchone() is None else
                              cur.execute(
                                  """select answer from notes where number_qa = ? and notes_name = ?""",
                                  (self.number_of_question, self.notesName.text())).fetchone()[0]))
        else:
            self.flashcard.setText("Question\n" + ("" if cur.execute("""select question from notes where number_qa = 
            ? and notes_name = ?""", (self.number_of_question, self.notesName.text())).fetchone() is None else cur.execute(
                """select question from notes where number_qa = ? and notes_name = ?""",
                (self.number_of_question, self.notesName.text())).fetchone()[0]))

    def showNext(self):
        con = sqlite3.connect('flashcards.db')
        cur = con.cursor()
        self.number_of_question += 1
        if self.number_of_question == cur.execute(
                """select count_of_questions from main_information where name_of_note = ?""",
                (self.notesName.text(),)).fetchone()[0]:
            self.progressBar.setValue(self.number_of_question)
            self.msg_finished = QMessageBox()
            self.msg_finished.setText("You have finished the flashcards!")
            self.msg_finished.setStandardButtons(QMessageBox.Ok)
            self.msg_finished.exec_()
            self.close()
        else:
            if self.order:
                self.flashcard.setText("Question\n" + ("" if cur.execute("""select question from notes where number_qa =
                ? and notes_name = ?""", (self.random_list[self.number_of_question - 1], self.notesName.text())).fetchone() is
                                                             None else cur.execute(
                    """select question from notes where number_qa = ? and notes_name = ?""",
                    (self.random_list[self.number_of_question], self.notesName.text())).fetchone()[
                    0]))
            else:
                self.flashcard.setText("Question\n" + ("" if cur.execute("""select question from notes where number_qa =
                ? and notes_name = ?""", (self.number_of_question, self.notesName.text())).fetchone() is None else cur.
                                                       execute("""select question from notes where number_qa = ? and
                                                        notes_name = ?""", (self.number_of_question,
                                                                            self.notesName.text())).fetchone()[0]))
            self.progressBar.setValue(self.number_of_question)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FlashcardWindow()
    win.show()
    sys.exit(app.exec_())
