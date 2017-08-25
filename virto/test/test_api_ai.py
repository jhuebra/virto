#!/usr/bin/python
# coding: utf-8

import unittest
import apiai
import json
import time

import config.settings as settings
from apiai_client import ApiAiClient, ApiAiResultData, ApiAiResponseError

settings.API_AI_CLIENT_ACCESS_TOKEN = 'd72a432429cf428cb066ee98bbe583d9'

class ApiAiTest(unittest.TestCase):

    def test_00(self):
        ai_client = ApiAiClient(settings.API_AI_CLIENT_ACCESS_TOKEN)

        query = u"traeme"
        session_id = "cliente_1"
        try:
            result = ai_client.send_query(query, session_id)

            self.assertIsNotNone(result.session_id)

            print u'%s' % result

            query = u"leche"
            result = ai_client.send_query(query, session_id)
            print u'%s' % result

        except ApiAiResponseError, ex:
            print(ex.message)


if __name__ == '__main__':
    unittest.main()
