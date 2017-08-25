#!/usr/bin/python
# coding: utf-8

import zmq
import random
import sys
import time
import json

port = "5556"
message = "START_KEYWAITING"
if len(sys.argv) > 1:
    message = sys.argv[1]


REQUEST_TIMEOUT = 2500
REQUEST_RETRIES = 3
SERVER_ENDPOINT = "tcp://127.0.0.1:%s" % port

context = zmq.Context(1)

print("I: Connecting to server ...")
client = context.socket(zmq.REQ)
client.connect(SERVER_ENDPOINT)

poll = zmq.Poller()
poll.register(client, zmq.POLLIN)

retries_left = REQUEST_RETRIES
while retries_left:
    request = json.dumps({'action': str(message).encode()})
    print("I: Sending (%s)" % request)
    client.send_json(request)

    expect_reply = True
    while expect_reply:
        socks = dict(poll.poll(REQUEST_TIMEOUT))
        if socks.get(client) == zmq.POLLIN:
            reply = client.recv_json()
            if not reply:
                break
            print("I: Server replied OK (%s)" % reply)
            retries_left = 0
            expect_reply = False
        else:
            print("W: No response from server, retrying...")
            # Socket is confused. Close and remove it.
            client.setsockopt(zmq.LINGER, 0)
            client.close()
            poll.unregister(client)
            retries_left -= 1
            if retries_left == 0:
                print("E: Server seems to be offline, abandoning")
                break
            print("I: Reconnecting and resending (%s)" % request)
            # Create new connection
            client = context.socket(zmq.REQ)
            client.connect(SERVER_ENDPOINT)
            poll.register(client, zmq.POLLIN)
            client.send_json(request)

print("I: Ending...")
client.setsockopt(zmq.LINGER, 0)
client.close()
context.term()


"""
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

topic = random.randrange(9999,10005)
messagedata = random.randrange(1,215) - 80
print "%d %d" % (topic, messagedata)
socket.send("%d %d" % (topic, messagedata))
time.sleep(1)
"""