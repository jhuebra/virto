#!/usr/bin/python
# coding: utf-8

"""
recognize speech using Google Cloud Speech
"""

import os
import sys
import unittest
import speech_recognition as sr

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "./../"))

import config.settings as settings

settings.GOOGLE_APPLICATION_CREDENTIALS = 'VIRTO-2d075bc9bc8e.json'
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", PROJECT_ROOT + os.path.sep + settings.GOOGLE_APPLICATION_CREDENTIALS)


class GoogleSpeechTest(unittest.TestCase):

    def test_00(self):
        print("Google Cloud Speech")
        try:
            recognizer = sr.Recognizer()
            wav_file = "holavirto2.wav"
            wav_file = "traeme.wav"
            wav_file = "agua.wav"

            with sr.AudioFile(os.path.join(PROJECT_ROOT, wav_file)) as source:
                audio = recognizer.listen(source, phrase_time_limit=5) 

            # print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS, language="es-ES"))
            print("Google Cloud Speech thinks you said " + recognizer.recognize_google_cloud(audio, language="es-ES"))
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
        except Exception, e:
            print(e)

if __name__ == '__main__':
    unittest.main()
