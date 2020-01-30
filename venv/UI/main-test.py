from __future__ import division

import re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests as req
from opening import Ui_DocAid
from homepage import Ui_MainWindow
from waste import Ui_Prescription
from firebase_admin import credentials, firestore, initialize_app
from report import Ui_Report
from chart import Ui_chart
import json
import webbrowser
from datetime import date

import socket
import pickle

from keyword_search import feature_search
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from textblob import TextBlob, Word

from config import socketIp, serverAddr

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    string=""
    """Iterates through server responses and prints them.
    The responses passed is a generator that will block until a response
    is provided by the server.
    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.
    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print(transcript + overwrite_chars)
            string += transcript+overwrite_chars
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print(string)
                print('Exiting..')
                return string


class Mainwindow(QMainWindow):
    def __init__(self, parent=None):
        super(Mainwindow, self).__init__(parent)
        self.docAid = Ui_DocAid()
        self.homepage = Ui_MainWindow()
        self.prescription = Ui_Prescription()
        self.charting = Ui_chart()
        self.prescribed = set()
        self.patient = {}
        self.report = Ui_Report()
        self.start_ui_window()
        self.host = socketIp
        self.port = 5500
        self.client = socket.socket()
        self.data = None

    def qr_check(self):
        self.client.connect((self.host, self.port))

        while True:
            self.client.send(pickle.dumps({"Hello": "World"}))
            self.data = pickle.loads(self.client.recv(2048))
            print("TEST")
            if self.data:
                print(self.data)
                self.client.close()
                break
        return self.data

    def start_ui_window(self):
        self.docAid.setupUi(self)
        button = QPushButton('Statistics',self)
        button.setToolTip('This is an example button')
        button.move(555,450)
        button.clicked.connect(self.on_click)
        self.docAid.pushButton.clicked.connect(self.go_homepage)
        #self.prescription.setupUi(self)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.charting.setupUi(self)
        self.show()

    def go_homepage(self):
        self.docAid.pushButton.setText("Waiting for scan")
        self.docAid.pushButton.setIcon(QIcon("./images/blue-loader.gif"))
        QtWidgets.qApp.processEvents()
        data = self.qr_check()
        print(data)
        params1 = {
            "pid": data
        }
        details = req.get(url=serverAddr + '/patient_details', json=params1)
        print(details.text)
        details = json.loads(details.text)
        self.patient = details
        # print(details["name"], ' ',details["surname"])
        self.homepage.setupUi(self)
        self.homepage.label_4.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        self.homepage.label_4.setText(details["pid"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50, 240, 250, 17))
        self.homepage.label_5.setObjectName("age")
        self.homepage.label_5.setText("Age: "+details["age"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50, 260, 250, 17))
        self.homepage.label_5.setObjectName("gender")
        self.homepage.label_5.setText("Gender: "+details["gender"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50, 280, 250, 17))
        self.homepage.label_5.setObjectName("bmi")
        self.homepage.label_5.setText("BMI: "+details["bmi"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50, 300, 250, 17))
        self.homepage.label_5.setObjectName("address")
        self.homepage.label_5.setText("Address: "+details["address"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50, 320, 250, 17))
        self.homepage.label_5.setObjectName("phone")
        self.homepage.label_5.setText("Phone: "+details["phone"])
        history = req.get(serverAddr + "/diagonized_medicines", json=params1)
        arr = []
        
        # if history is None:
        #     print("No history")
        # else:
        #     history = history.json()
        #     for a in history.keys():
        #         arr.append({'date': a, 'medicine': history[a]['medicines']})
        #     print(arr)
        #     for dosage in arr[::-1]:
        #         print(dosage)
        #         self.homepage.textBrowser_2 = QtWidgets.QTextBrowser(self.homepage.scrollAreaWidgetContents)
        #         self.homepage.textBrowser_2.setObjectName("textBrowser_2")
        #         self.homepage.verticalLayout_2.addWidget(self.homepage.textBrowser_2)
        #         cursor = self.homepage.textBrowser_2.textCursor()
        #         cursor.insertHtml('''<div style="font-size:25px;color:#2B56BE">Visited on {}</div>'''.format(
        #             dosage['date'][0:8]))
        #
        #         for i in dosage['medicine']:
        #             cursor.insertHtml('''<br></br><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px;
        #             margin-right:0px; -qt-block-indent:0; text-indent:0px;">{}</p>'''.format(
        #                 i['name']+" "+i['dosage']+" mg"))
        self.homepage.pushButton.clicked.connect(self.go_prescription)
        self.show()

    def work(self, _str, _str2):
        def calling():
            self.prescribed.add(_str+"  "+_str2)
            print(self.prescribed)
            string = ""
            for a in self.prescribed:
                string = string + "\n" + a + " mg"
            print(string)
            self.prescription.label_5.setText(string)
            QtWidgets.qApp.processEvents()
        return calling

    def go_prescription(self):
        self.homepage.pushButton.setText("Listening")
        self.homepage.pushButton.setIcon(QIcon("./images/blue-loader.gif"))
        QtWidgets.qApp.processEvents()
        language_code = 'en-US'  # a BCP-47 language tag
        client = speech.SpeechClient()
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            # Now, put the transcription responses to use.
            string = listen_print_loop(responses)
        print("FINAL STRING: ", string)
        # blob = TextBlob(string)
        # number_of_tokens = len(list(blob.words))
        # # Extracting Main Points
        # nouns = list()
        # for word, tag in blob.tags:
        #     if tag == 'NN':
        #         nouns.append(word.lemmatize())
        #         len_of_words = len(nouns)
        #         rand_words = random.sample(nouns, len(nouns))
        #         final_word = list()
        #         for item in rand_words:
        #             word = Word(item).pluralize()
        #             final_word.append(word)
        #             summary = final_word
        # print(summary)
        print("FEATURES: ", feature_search(string))
        data1 = feature_search(string)
        # data=[1,0,0,1,0,1,0,0,0,1]
        r = req.post(serverAddr + "/prediction", json={"val": data1, "patient": self.patient})

        # data1=[{'Dengue': [1, {'Acetaminophen': [1, 1, 1, 650, 1, 0, 1, 7, 1],
        # 'Aspirin': [2, 1, 1, 500, 0, 0, 1, 3, 1], 'Ostoshine': [5, 1, 1, 6000, 0, 1, 0, 4, 1],
        # 'Platimax': [3, 1, 0, 500, 0, 1, 1, 3, 1], 'Qubinor': [4, 1, 1, 600, 0, 1, 0, 4, 1]}]},
        # ['skin_rash', 'fatigue', 'loss_of_appetite', 'muscle_pain']]
        data1 = pickle.loads(r.content)
        print(data1)
        # medicines=[r.json()[key][1] if key not 'symptoms' in for key in r.json().keys]
        medicines = data1[0]
        print(medicines)
        symptoms = data1[1]
        print(symptoms)
        print("RAGHAV SIR IS GENIUS")
        db.collection("SymptomTemp").document("LatestSymptom").set({"symptoms":symptoms})

        i = -1
        self.prescription.setupUi(self)
        for x in symptoms:
            i += 1
            self.prescription.checkBox = QtWidgets.QCheckBox(self.prescription.centralwidget)
            self.prescription.checkBox.setGeometry(QtCore.QRect(40+(i*90), 100, 191, 21))
            self.prescription.checkBox.setObjectName("checkBox"+str(i))
            self.prescription.checkBox.setText(x)

        i = -1
        for key in range(len(medicines)):
            i += 1
            self.prescription.textBrowser_3 = QtWidgets.QTextBrowser(self.prescription.scrollAreaWidgetContents)
            self.prescription.verticalLayout_2.addWidget(self.prescription.textBrowser_3)
            self.prescription.pushButton_10 = QtWidgets.QPushButton(self.prescription.scrollAreaWidgetContents)
            self.prescription.pushButton_10.setObjectName("pushButton"+str(i))
            self.prescription.pushButton_10.setStyleSheet("background-color:rgb(43, 86, 190);color:rgb(255, 255, 255)")
            self.prescription.verticalLayout_2.addWidget(self.prescription.pushButton_10)
            self.prescription.pushButton_10.setText("Add to prescription")
            self.prescription.pushButton_10.clicked.connect(self.work(medicines[key][0], str(medicines[key][1][3])))
            self.prescription.textBrowser_3.viewport().setProperty("cursor",
                                                                   QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.prescription.textBrowser_3.setMouseTracking(True)
            self.prescription.textBrowser_3.setTabletTracking(True)
            self.prescription.textBrowser_3.setAutoFillBackground(True)
            self.prescription.textBrowser_3.setStyleSheet(
                "selection-background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5,"
                "fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255),"
                "stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92),"
                "stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205),"
                "stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));")

            self.prescription.textBrowser_3.document().setDefaultStyleSheet(
                'div{margin:5px 20px; margin-top: 10px} span{float:right}')

            self.prescription.textBrowser_3.setObjectName("textBrowser_"+str(i))
            cursor = self.prescription.textBrowser_3.textCursor()
            cursor.insertHtml('''<div style="color:black;font-size:23px; padding:100px">{}</div><div>{}</div>'''.format(
                medicines[key][0]+"  "+str(medicines[key][1][3])+"mg    ", '1-0-1'))
          
        QtWidgets.qApp.processEvents()
        # self.prescription.setupUi(self)
        self.prescription.pushButton_9.clicked.connect(self.go_report)
        self.show()

    def go_report(self):
        self.report.setupUi(self)
        today = date.today()
        d2 = today.strftime("%B  %d")
        d2 = "Prescription  for  " + d2
        print(self.prescribed)
        string = ""
        for i in self.prescribed:
            string = string + i + " mg" + "\n"
        self.report.pres.setText(string)
        self.report.label_6.setText(d2)
        self.report.label_6.setStyleSheet("color:white;font-size:30px")
        self.report.pres.setStyleSheet("font-size:20px")
        self.report.label_4.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        # self.report.label_5.setText(patient["pid"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50, 240, 250, 17))
        self.report.label_5.setObjectName("age")
        self.report.label_5.setText(self.patient["age"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50, 270, 250, 17))
        self.report.label_5.setObjectName("gender")
        self.report.label_5.setText(self.patient["gender"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50, 300, 250, 17))
        # self.report.label_5.setObjectName("BMI")
        # self.report.label_5.setText(self.patient["BMI"])
        # self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        # self.report.label_5.setGeometry(QtCore.QRect(50, 330, 250, 17))
        self.report.label_5.setObjectName("address")
        self.report.label_5.setText(self.patient["address"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50, 360, 250, 17))
        self.report.label_5.setObjectName("phone")
        self.report.label_5.setText(self.patient["phone"])
        self.report.label_4.setText(self.patient["pid"])
        # print(self.patient["pid"], self.patient["age"], self.patient["BMI"], self.prescribed)
        self.report.pushButton.clicked.connect(self.pdf)
        self.show()
    
    def pdf(self):
        meds = []
        for a in self.prescribed:
            meds.append({"name": a, "dosage": "1-0-1", "qty": "600 mg"})
        data = {
            "age": self.patient["age"],
            "pid": self.patient["pid"],
            # "bmi": self.patient["BMI"],
            "dosages": meds
        }
        p = req.post(serverAddr + "/rg", json=data)
        url = p.text
        webbrowser.open(url)
        self.charting.setupUi(self)
        self.show()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Mainwindow()
    sys.exit(app.exec_())
