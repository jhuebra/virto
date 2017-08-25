#!/usr/bin/python
# coding: utf-8

# NOTE: this example requires PyAudio because it uses the Microphone class
import os
import speech_recognition as sr

# ---------------------------------------
# audio info
# sistema: sudo cat /proc/asound/cards
os.system("cat /proc/asound/cards") 
import pyaudio
audio=pyaudio.PyAudio()
devices = [audio.get_device_info_by_index(i) for i in range(audio.get_device_count())]
for d in devices:
    print(d)
    print()
# ----------------------------------------

# obtain audio from the microphone
r = sr.Recognizer()
r.phrase_threshold = 0.3  # tiempo minimo para que se considere como una frase
with sr.Microphone() as source:
    print("Espera...")
    r.adjust_for_ambient_noise(source)
    print("Energy threshold", r.energy_threshold)
    print("Say something!")
    # timeout = tiempo para empezar a hablar --> WaitTimeoutError
    # phrase_time_limit = tiempo máximo de la frase
    audio = r.listen(source, phrase_time_limit=5, timeout=10) 

