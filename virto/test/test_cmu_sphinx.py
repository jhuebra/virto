#!/usr/bin/python
# coding: utf-8

"""
recognize speech using Google Cloud Speech
"""

import os
import sys
import time
import unittest


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "./../"))

import speech_recognition as sr
import config.settings as settings

KEYWORD_ENTRIES = [('hola virto', 1e-40),
                   ('pasa virto', 1e-40)]
print sr

class CMUSpeechTest(unittest.TestCase):

    def test_00(self):
        print("CMU Speech")
        
        recognizer = sr.Recognizer()

        t0 = time.time()
        decoder = recognizer.get_recognize_sphinx(language="es-ES", keyword_entries=KEYWORD_ENTRIES)
        t1 = time.time()
        print(t1 - t0)

        wav_file = "holavirto2.wav"
        self.search(recognizer, decoder, wav_file)
        wav_file = "traeme.wav"
        self.search(recognizer, decoder, wav_file)
        wav_file = "agua.wav"
        self.search(recognizer, decoder, wav_file)


    def search(self, recognizer, decoder, wav_file):
        print(wav_file)
        try:

            t1 = time.time()
            with sr.AudioFile(os.path.join(PROJECT_ROOT, wav_file)) as source:
                audio_data = recognizer.listen(source, phrase_time_limit=5) 
            t2 = time.time()
            print(t2 - t1)

            # print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language="es-ES"))
            print("CMU Speech thinks you said " + recognizer.recognize_sphinx_keyword(audio_data,
                                                                                        language="es-ES",
                                                                                        keyword_entries=KEYWORD_ENTRIES,
                                                                                        show_all=False))
            t3 = time.time()
            print(t3 - t2)        
        except sr.UnknownValueError:
            print("CMU Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from CMU Speech: {0}".format(e))
        except Exception, e:
            print(e)


if __name__ == '__main__':
    unittest.main()
