#!/usr/bin/python
# coding: utf-8

import os
import argparse
import importlib
import threading
import logging
import time
import zmq
import json
import uuid
from datetime import datetime

import speech_recognition as sr
from apiai_client import ApiAiClient, ApiAiResultData, ApiAiResponseError

PROJECT_ROOT = os.path.dirname(__file__)

# LOG ----------------------------------------------------
logger = logging.getLogger('virto_sound')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages --> RotatingFileHandler('virto_sound.log', maxBytes=1024*1000, backupCount=5)
fh = logging.FileHandler('virto_sound.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# [LOG] ----------------------------------------------------


class VirtoSignals(object):
    """
    VirtoSound signals
    """
    STARTED = 1
    STOPPED = 2
    END_OF_KEYWORD = 3
    END_OF_UTTERANCE = 4

class VirtoActions(object):
    """
    VirtoSound action
    """
    START = 1
    STOP = 2  
    PAUSE = 2  


class VirtoSound(object):
    """
    Manage speech entry
    """
    STOPPED = 0
    WAITTING = 1   # <-- STOP ACTION
    KEYWAITING = 2 # <-- START_KEYWAITING ACTION
    KEYLISTENING = 3
    UTTERANCEWAITING = 4
    UTTERANCELISTENING = 5

    def __init__(self, subscribe_port="5556", language="es-ES"):
        """
        Constructor
        """
        self.ID = uuid.uuid4()
        self.language = language

        self.old_state = None
        self.state = VirtoSound.STOPPED
        self.start_time = datetime.utcnow()
        self.state_start_time = None

        # manage sound and recognition
        self.recognizer = sr.Recognizer()

        # Microphone settings. TODO: en settings
        self.command_timeout = 15  # max command retry time
        self.phrase_time_limit = 7
        self.speech_start_timeout = 5

        # keywords [(keyword, sensitivity),...]
        self.keyword_entries = settings.KEYWORD_ENTRIES

        # PUB/SUB - REQ/REP. TODO: linux socket
        self.subscribe_port = subscribe_port

        # recognize speech using Google Cloud Speech
        try:
            os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', os.path.dirname(os.path.abspath(
                __file__)) + os.path.sep + settings.GOOGLE_APPLICATION_CREDENTIALS)
            print os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        except:
            logger.error('GOOGLE_APPLICATION_CREDENTIALS not found: %s', settings.GOOGLE_APPLICATION_CREDENTIALS)

        self.ai_client = ApiAiClient(settings.API_AI_CLIENT_ACCESS_TOKEN)



    def set_state(self, state):
        """
        Change and track states changes
        """
        self.old_state = self.state
        self.state = state
        self.state_start_time = datetime.utcnow()

        logger.info(80*"-")
        logger.info("State change: %s --> %s", self.old_state, self.state)

        # STOP state. TODO: finish sound thread + control channel --> zmq.NOBLOCK


    def run(self):
        """
        Main control loop.
        Start sound daemon and 0MQ control channel.
        """

        self.set_state(VirtoSound.WAITTING)

        # 1. start sound thread
        d = threading.Thread(target=self._sound_run)
        d.setDaemon(True)
        d.start()

        # 2. Control loop. IPC loop
        self._control_channel()


    def _sound_run(self):
        """
        Main sound loop.
        """

        logger.info('Running sound thread ...')

        # recognizer = sr.Recognizer()
        recognizer = self.recognizer
        recognizer.phrase_threshold = 0.3  # tiempo minimo para que se considere como una frase
        recognizer.energy_threshold = self.calibrate()

        while True:
            try:
                if self.state in [VirtoSound.KEYWAITING, VirtoSound.UTTERANCEWAITING]:
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        logger.info("energy_threshold: %s", recognizer.energy_threshold)

                        # wait for phrase
                        try:
                            audio_data = recognizer.listen(source,
                                                           phrase_time_limit=self.phrase_time_limit,
                                                           timeout=self.speech_start_timeout)
                            logger.info(40*"*")
                            logger.info("audio captured !!!!! %s", len(audio_data.frame_data)/1024)
                        except sr.WaitTimeoutError:
                            logger.info("Start sound WaitTimeoutError: %s", self.speech_start_timeout)
                            audio_data = None

                    if audio_data:
                        if self.state == VirtoSound.KEYWAITING:
                            # try CMU Sphinx
                            try:
                                keyword = recognizer.recognize_sphinx(audio_data,
                                                                      language=self.language,
                                                                      keyword_entries=self.keyword_entries,
                                                                      show_all=False)
                                self._keyword_found(keyword)
                            except sr.UnknownValueError:
                                logger.info("keyword UnknownValueError")
                            
                        elif self.state == VirtoSound.UTTERANCEWAITING:
                            # try Google speech
                            # 
                            try:
                                transcript = recognizer.recognize_google_cloud(audio_data,
                                                                               language=self.language,
                                                                               preferred_phrases=None)
                            except sr.RequestError, e:
                                logger.info("google_cloud RequestError %s", e)
                            except sr.UnknownValueError:
                                logger.info("google_cloud UnknownValueError")
                            else:
                                # command_do
                                pass

                    else:
                        # check global timeout
                        elapsed_time = datetime.utcnow() - self.state_start_time
                        if elapsed_time.total_seconds() > self.command_timeout:
                            logger.info("Stop sound Waitting (%s)", self.command_timeout)
                            self.set_state(VirtoSound.WAITTING)


                time.sleep(0.2)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception, ex:
                logger.info("Exit sound Unexpected error: %s", ex)        
        logger.info("Exit sound thread ...")

    def _keyword_found(self, keyword):
        """
        Found keyword. change to next state
        """
        logger.info("Keyword found: {}".format(keyword))
        self.set_state(VirtoSound.UTTERANCEWAITING)


    def command_do(self, transcript):
        """
        Send transcript to api.ai
        """
        logger.info("command_do: %s", transcript)

        time.sleep(2) # api.ai call
        response = "api.ai json response"
        logger.info("command done: %s", response)

        # command finished
        # --> state = VirtoSound.KEY_WAITTING

        # command prompt
        # store api.ai response

        # output sound ???

    def query_api_ai(self, transcript):
        """
        api.ai call
        """
        session_id = self.ID
        try:
            result = self.ai_client.send_query(transcript, session_id)

            if result.speech:
                logger.info("Hablamos: %s", result.speech)
                # send event --> result.speech

            if not result.action_incomplete:
                logger.info("Action completed: %s", result.action)
                # finish 
                # send event --> finish action

                # change status. Back to KEYWAITING
                self.set_state(VirtoSound.KEYWAITING)
            else:
                logger.info("Action incompleted: %s", result.action)


        except ApiAiResponseError, ex:
            logger.error(ex.message)
        


    def _control_channel(self):
        """
        Control and change application status.

        Wait for json request: 'action':'START_KEYWAITING/STOP', 'data':'{}'
        return json response : 'status':'OK/ERROR', 'data':'{}'
        """
        # Lazy Pirate server
        context = zmq.Context(1)
        server = context.socket(zmq.REP)
        server.bind("tcp://127.0.0.1:%s" % self.subscribe_port)

        logger.info('Control channel started...')

        while True:
            try:
                request = server.recv_json()  # JSON

                action = None
                try:
                    logger.info(request)
                    request = json.loads(request)
                    action = request['action'] 
                except Exception,ex:
                    logger.error('Control channel request error: {} - {}'.format(request, ex))

                response = {"status":"ERROR",
                            "data":""}
                
                # Actions
                if action == "START_KEYWAITING":
                    self.set_state(VirtoSound.KEYWAITING)
                    response['status'] = 'OK'
                elif action == "STOP":
                    self.set_state(VirtoSound.WAITTING)
                    response['status'] = 'OK'

                # send response
                server.send(json.dumps(response))

            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception, ex:
                logger.info("Control channel Unexpected error: %s", ex)     

        server.close()
        context.term()



    def audio_info(self):
        """
        Listado de los audio devices
        sistema: sudo cat /proc/asound/cards
        """
        os.system("cat /proc/asound/cards") 
        import pyaudio
        audio=pyaudio.PyAudio()
        devices = [audio.get_device_info_by_index(i) for i in range(audio.get_device_count())]
        for d in devices:
            logger.info(d)
            logger.info("")

    def calibrate(self):
        """
        Adjust ambient sound level
        """
        logger.info("Calibrating ...")
        recognizer = self.recognizer
        recognizer.dynamic_energy_adjustment_damping = 0.15
        recognizer.dynamic_energy_ratio = 2.5  # 1.5 
      
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=4)
        logger.info("energy_threshold: %s", recognizer.energy_threshold)
        return recognizer.energy_threshold




if __name__ == "__main__":

    """
    Select another settings: python app.py --settings=config.debug_settings
    """
    parser = argparse.ArgumentParser(description='VirtoSound parameters')
    parser.add_argument('--settings', help='settings module')
    args = parser.parse_args()
    if args.settings:
        settings = importlib.import_module(args.settings)
    else:
        import config.settings as settings

    if settings.DEBUG == False:
        # quitamos el log a consola
        logger.removeHandler(ch)
    else:
        # quitamos el log a fichero
        logger.removeHandler(fh)

    logger.info("Started ...")

    # Launch app.
    virto_sound = VirtoSound()
    if settings.DEBUG:
        virto_sound.audio_info()
    virto_sound.run()


