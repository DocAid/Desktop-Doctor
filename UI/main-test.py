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
from prescription import Ui_Prescription
from report import Ui_Report
import json

import random

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
                # break

            num_chars_printed = 0



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.docAid = Ui_DocAid()
        self.homepage = Ui_MainWindow()
        self.prescription=Ui_Prescription()
        self.report=Ui_Report()
        self.startUIWindow()

    def startUIWindow(self):
        self.docAid.setupUi(self)
        self.docAid.pushButton.clicked.connect(self.goHomepage)
        self.show()

    def goHomepage(self):
        self.docAid.pushButton.setText("Loading")
        self.docAid.pushButton.setIcon(QIcon("./images/ajax-loader.gif"))
        QtWidgets.qApp.processEvents()
        details=req.get('https://uinames.com/api/?amount=1')
        details=json.loads(details.text)
        print(details["name"], ' ',details["surname"])
        self.homepage.setupUi(self)
        self.homepage.label_4.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        self.homepage.label_4.setText(details["name"]+details["surname"])
        self.homepage.label_5.setText(details["gender"])
        self.homepage.pushButton.clicked.connect(self.goPrescription)
        self.show()
    
    def goPrescription(self):
        self.homepage.pushButton.setText("Listening")
        self.homepage.pushButton.setIcon(QIcon("./images/ajax-loader.gif"))
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
        # r=req.post("http://ca2f4a2b.ngrok.io/prediction",json={"val":data1})
        # print(r.json())
        self.prescription.setupUi(self)
        self.prescription.pushButton_9.clicked.connect(self.goReport)
        self.show()

        

    def goReport(self):
        self.report.setupUi(self)
        details=req.get('https://uinames.com/api/?amount=1')
        details=json.loads(details.text)
        print(details["name"])
        self.report.label_4.setText(details["name"]+details["surname"])
        self.report.label_5.setText(details["gender"])
        # self.homepage.pushButton.setText("Clicked")
        # self.prescription.setupUi(self)
        self.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())