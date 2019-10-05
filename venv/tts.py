from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QTextEdit, QVBoxLayout
import sys
from PyQt5.QtGui import QFont
import speech_recognition as sr
from textblob import TextBlob, Word
import random


class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Audio to text converter"
        self.setWindowTitle(self.title)
        self.top = 100
        self.width = 400
        self.left = 100
        self.height = 300
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.InitUI()

    def InitUI(self):
        vbox = QVBoxLayout()
        self.textEdit = QTextEdit(self)
        self.textEdit.setFont(QFont("Times", 15))
        vbox.addWidget(self.textEdit)
        self.btn = QPushButton("Convert Audio")
        vbox.addWidget(self.btn)
        self.btn.clicked.connect(self.convertAudio)
        self.setLayout(vbox)

    def convertAudio(self):
        r = sr.Recognizer()
        sound = "demo.wav"

        with sr.AudioFile(sound) as source:
            r.adjust_for_ambient_noise(source)
            sound = r.listen(source)
        try:
            print("done")
            text = r.recognize_google(sound)
            self.textEdit.setText(text)
            blob = TextBlob(text)
            number_of_tokens = len(list(blob.words))
            # Extracting Main Points
            nouns = list()
            for word, tag in blob.tags:
                if tag == 'NN':
                    nouns.append(word.lemmatize())
                    len_of_words = len(nouns)
                    rand_words = random.sample(nouns, len(nouns))
                    final_word = list()
                    for item in rand_words:
                        word = Word(item).pluralize()
                        final_word.append(word)
                        summary = final_word
            print(summary)

        except Exception as e:
            print(e)


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
