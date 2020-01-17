from __future__ import division

import re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests as req
from opening import Ui_DocAid
from homepage import Ui_MainWindow
from waste import Ui_Prescription
from report import Ui_Report
import json
from flask import jsonify
import webbrowser
from datetime import date

import random
import time
import socket
import pickle

from keyword_search import feature_search
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue
from textblob import TextBlob, Word


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


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
                # break

            num_chars_printed = 0



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.docAid = Ui_DocAid()
        self.homepage = Ui_MainWindow()
        self.prescription=Ui_Prescription()
        self.prescribed=set()
        self.patient={}
        self.report=Ui_Report()
        self.startUIWindow()

    def QR_check(self):
        host = "34.93.231.96"
        port = 5500
        client = socket.socket()
        client.connect((host, port))

        while True:
            client.send(pickle.dumps({"Hello": "World"}))
            data = pickle.loads(client.recv(2048))
            print("TEST")
            if data:
                 print(data)
                 client.close()
                 break
        return data

    def startUIWindow(self):
        self.docAid.setupUi(self)
        self.docAid.pushButton.clicked.connect(self.goHomepage)
        # self.goHomepage()        
        self.show()


    def goHomepage(self):
        self.docAid.pushButton.setText("Waiting for scan")
        self.docAid.pushButton.setIcon(QIcon("./images/blue-loader.gif"))
        QtWidgets.qApp.processEvents()
        data="POC0012"
        data=self.QR_check()
        print(data)
        params1 = {
            "pid":data
        }
        details=req.get(url='http://34.93.231.96:5000/patient_details', json=params1)
        print(details.text)
        details=json.loads(details.text)
        self.patient=details
        # print(details["name"], ' ',details["surname"])
        self.homepage.setupUi(self)
        self.homepage.label_4.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        self.homepage.label_4.setText(details["pid"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50,240, 250,17))
        self.homepage.label_5.setObjectName("age")
        self.homepage.label_5.setText("Age: "+details["age"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50,260, 250,17))
        self.homepage.label_5.setObjectName("gender")
        self.homepage.label_5.setText("Gender: "+details["gender"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50,280, 250,17))
        self.homepage.label_5.setObjectName("bmi")
        self.homepage.label_5.setText("BMI: "+details["bmi"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50,300, 250,17))
        self.homepage.label_5.setObjectName("address")
        self.homepage.label_5.setText("Address: "+details["address"])
        self.homepage.label_5 = QtWidgets.QLabel(self.homepage.widget_2)
        self.homepage.label_5.setGeometry(QtCore.QRect(50,320, 250,17))
        self.homepage.label_5.setObjectName("phone")
        self.homepage.label_5.setText("Phone: "+details["phone"])
        history=req.get("http://34.93.231.96:5000/diagonized_medicines", json=params1)
        arr=[]
        
        if history is None:
            print("No history")
        else:
            history=history.json()
            # print(history)
            for a in history.keys():
                arr.append({'date':a,'medicine':history[a]['medicines']})
            print(arr)
            for dosage in arr[::-1]:
                print(dosage)
                str=""
                self.homepage.textBrowser_2 = QtWidgets.QTextBrowser(self.homepage.scrollAreaWidgetContents)
                self.homepage.textBrowser_2.setObjectName("textBrowser_2")
                self.homepage.verticalLayout_2.addWidget(self.homepage.textBrowser_2)
                # str="Visited on "+dosage['date'][0:8]+"\n\n"
                cursor=self.homepage.textBrowser_2.textCursor()
                cursor.insertHtml('''<div style="font-size:25px;color:#2B56BE">Visited on {}</div>'''.format(dosage['date'][0:8]))
                # cursor.insertHtml('''<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{}</p>'''.format(dosage['date'][0:8]+"\n"))
                for i in dosage['medicine']:
                    # str=str+"\t"+i['name']+"  "+i['dosage']+" mg"+"\n"
                    cursor.insertHtml('''<br></br><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">{}</p>'''.format(i['name']+" "+i['dosage']+" mg"))
                # self.homepage.textBrowser_2.setText(str)
                # self.homepage.textBrowser_2.setStyleSheet("font-size:25px")
        self.homepage.pushButton.clicked.connect(self.goPrescription)
        self.show()
    

    def work(self,_str,_str2):
        def calling():
          self.prescribed.add(_str+"  "+_str2)
          print(self.prescribed)
          str=""
          for a in self.prescribed:
              str=str+"\n"+a+" mg"
          print(str)
          self.prescription.label_5.setText(str)
        #   self.prescription.label_10 = QtWidgets.QLabel(self.prescription.centralwidget)
        #   self.prescription.label_10.setGeometry(QtCore.QRect(980,370+(20*(len(self.prescribed)-1)),210,20))
        # #   self.prescription.label_10.setMaximumSize(QtCore.QSize(293, 32))
        #   self.prescription.label_10.setObjectName("label_10")
        #   self.prescription.label_10.setText(_str+"  "+_str2)
          QtWidgets.qApp.processEvents()
        return calling

    def goPrescription(self):
        self.homepage.pushButton.setText("Listening")
        self.homepage.pushButton.setIcon(QIcon("./images/blue-loader.gif"))
        QtWidgets.qApp.processEvents()
        string=""
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
            string=listen_print_loop(responses)
        print(string)
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
        print(feature_search(string))
        data1 = feature_search(string)
        # data=[1,0,0,1,0,1,0,0,0,1]
        r=req.post("http://34.93.231.96:5000/prediction",json={"val":data1, "patient":self.patient})
        # data1=[{'Dengue': [1, {'Acetaminophen': [1, 1, 1, 650, 1, 0, 1, 7, 1], 'Aspirin': [2, 1, 1, 500, 0, 0, 1, 3, 1], 'Ostoshine': [5, 1, 1, 6000, 0, 1, 0, 4, 1], 'Platimax': [3, 1, 0, 500, 0, 1, 1, 3, 1], 'Qubinor': [4, 1, 1, 600, 0, 1, 0, 4, 1]}]}, ['skin_rash', 'fatigue', 'loss_of_appetite', 'muscle_pain']]
        data1 = pickle.loads(r.content)
        print(data1)
        data1=list(data1)
        # medicines=[r.json()[key][1] if key not 'symptoms' in for key in r.json().keys]
        medicines={}
        for a in data1[0]:
            medicines[a]=data1[0][a]
        print(medicines)
        symptoms=data1[1]
        print(symptoms)
        i=-1
        self.prescription.setupUi(self)
        for x in symptoms:
            i=i+1
            self.prescription.checkBox = QtWidgets.QCheckBox(self.prescription.centralwidget)
            self.prescription.checkBox.setGeometry(QtCore.QRect(40+(i*90), 100, 191, 21))
            self.prescription.checkBox.setObjectName("checkBox"+str(i))
            self.prescription.checkBox.setText(x)
        # med={"Calpol":[1,0,1,500], "Paracetamol":[0,1,4,0],"Calpol4":[1,0,1,500], "Pasracetam4ol":[0,1,4,0],"C4alpol":[1,0,1,500], "Paracetamo4l":[0,1,4,0],"Ca44lpol":[1,0,1,500], "Paracetamo44l":[0,1,4,0],"Calpol444":[1,0,1,500], "Paracetamo4444l":[0,1,4,0]}
        # for key in medicines.keys():
        #     print(key,med[key][-1])
        i=-1
        for key in medicines.keys():
            i=i+1
            self.prescription.textBrowser_3 = QtWidgets.QTextBrowser(self.prescription.scrollAreaWidgetContents)
            self.prescription.verticalLayout_2.addWidget(self.prescription.textBrowser_3)
            self.prescription.pushButton_10 = QtWidgets.QPushButton(self.prescription.scrollAreaWidgetContents)
            self.prescription.pushButton_10.setObjectName("pushButton"+str(i))
            self.prescription.pushButton_10.setStyleSheet("background-color:rgb(43, 86, 190);color:rgb(255, 255, 255)")
            self.prescription.verticalLayout_2.addWidget(self.prescription.pushButton_10)
            self.prescription.pushButton_10.setText("Add to prescription")
            self.prescription.pushButton_10.clicked.connect(self.work(key, str(medicines[key][3])))
            self.prescription.textBrowser_3.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.prescription.textBrowser_3.setMouseTracking(True)
            self.prescription.textBrowser_3.setTabletTracking(True)
            self.prescription.textBrowser_3.setAutoFillBackground(True)
            self.prescription.textBrowser_3.setStyleSheet("selection-background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(255, 255, 255, 255), stop:0.2 rgba(255, 176, 176, 167), stop:0.3 rgba(255, 151, 151, 92), stop:0.4 rgba(255, 125, 125, 51), stop:0.5 rgba(255, 76, 76, 205), stop:0.52 rgba(255, 76, 76, 205), stop:0.6 rgba(255, 180, 180, 84), stop:1 rgba(255, 255, 255, 0));")
            self.prescription.textBrowser_3.document().setDefaultStyleSheet('div{margin:5px 20px; margin-top: 10px} span{float:right}')
            self.prescription.textBrowser_3.setObjectName("textBrowser_"+str(i))
            cursor=self.prescription.textBrowser_3.textCursor()
            cursor.insertHtml('''<div style="color:black;font-size:23px; padding:100px">{}</div><div>{}</div>'''.format(key+"  "+str(medicines[key][3])+"mg    ",'1-0-1'))
          
        QtWidgets.qApp.processEvents()
        # self.prescription.setupUi(self)
        self.prescription.pushButton_9.clicked.connect(self.goReport)
        self.show()

    def goReport(self):
        self.report.setupUi(self)
        today=date.today()
        d2 = today.strftime("%B  %d")
        d2="Prescription  for  "+d2
        print(self.prescribed)
        str=""
        for i in self.prescribed:
            str=str+i+" mg"+"\n"
        self.report.pres.setText(str)
        self.report.label_6.setText(d2)
        self.report.label_6.setStyleSheet("color:white;font-size:30px")
        self.report.pres.setStyleSheet("font-size:20px")
        self.report.label_4.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        # self.report.label_5.setText(patient["pid"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50,240, 250,17))
        self.report.label_5.setObjectName("age")
        self.report.label_5.setText(self.patient["age"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50,270, 250,17))
        self.report.label_5.setObjectName("gender")
        self.report.label_5.setText(self.patient["gender"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50,300, 250,17))
        self.report.label_5.setObjectName("BMI")
        self.report.label_5.setText(self.patient["BMI"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)    
        self.report.label_5.setGeometry(QtCore.QRect(50,330, 250,17))
        self.report.label_5.setObjectName("address")
        self.report.label_5.setText(self.patient["address"])
        self.report.label_5 = QtWidgets.QLabel(self.report.widget_2)
        self.report.label_5.setGeometry(QtCore.QRect(50,360, 250,17))
        self.report.label_5.setObjectName("phone")
        self.report.label_5.setText(self.patient["phone"])
        self.report.label_4.setText(self.patient["pid"])
        print(self.patient["pid"],self.patient["age"],self.patient["BMI"], self.prescribed)
        self.report.pushButton.clicked.connect(self.pdf)
        self.show()
    
    def pdf(self):
        meds=[]
        for a in self.prescribed:
            meds.append({"name":a,"dosage":"1-0-1","qty":"600 mg"})
        data={
            "age":self.patient["age"],
            "pid":self.patient["pid"],
            "bmi":self.patient["BMI"],
            "dosages":meds
        }
        p=req.post("http://50269098.ngrok.io/rg",json=data)
        url = p.text
        webbrowser.open(url)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
