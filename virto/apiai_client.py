#!/usr/bin/python
# coding: utf-8

import json
import time
import apiai

class ApiAiResponseError(Exception): pass

class ApiAiResultData(object):
    """
    api.ai responses
    """
    def __init__(self):
        self.session_id = None
        self.action_incomplete = False
        self.action = None
        self.speech = None
        self.contexts = []

    def __unicode__(self):
        return u"action: {}\n\rincomplete: {}\n\rspeech: {}\n\r\n\r{}\n\r".format(self.action,
                                                                                  self.action_incomplete,
                                                                                  self.speech,
                                                                                  self.contexts)

class ApiAiClient(object):
    """
    api.ai wrapper
    """

    def __init__(self, client_id, lang='es'):
        self.client_id = client_id
        self.lang = lang
        self.ai = apiai.ApiAI(client_id)

    def send_query(self, query, session_id, context=None):
        """
        Send query to api.api
        return ApiAiResultData
        may raise ApiAiResponseError, Exception
        """

        result_data = ApiAiResultData()

        request = self.ai.text_request()
        request.lang = self.lang
        request.session_id = session_id # "<SESSION ID, UNIQUE FOR EACH USER>"
        request.query = query

        # api call
        time1 = time.time()
        response = request.getresponse()
        response_str = response.read().decode('utf-8')
        time2 = time.time()
        print("api call time {:0.3f} ms".format((time2-time1)*1000.0))
        response_data = json.loads(response_str)

        # data
        status = response_data.get('status')
        if status and status["errorType"] == "success":
            session_id = response_data.get('sessionId')
            result = response_data.get('result')
            action = response_data.get('action')
            fulfillment = result.get("fulfillment")

            result_data.session_id = session_id
            result_data.action_incomplete = result.get("actionIncomplete") # continue if action_incomplete=True
            result_data.action = action
            result_data.speech = fulfillment.get("speech") if fulfillment else None
            result_data.contexts = result.get("contexts")
        else:
            raise ApiAiResponseError("api.ai status ERROR")

        return result_data
