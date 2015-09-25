#qpy:2
#qpy:console

'''
hi there
'''

import site
import time
import os, json
import ibmiotf.application
from pprint import pprint

client = None
deviceId = None

# TODO
# this method will get information from client by push event
# cntVideo, cntMusic, cntPicture, inPlayVideo, inPlayMusic, inPlayPicture
def myCommandCallback(cmd):
    pprint(vars(cmd))

try:
    options = ibmiotf.application.ParseConfigFile("device.cfg")
    deviceId = options["id"]
    client = ibmiotf.application.Client(options)
    client.connect()

    client.deviceEventCallback = myCommandCallback
    client.subscribeToDeviceEvents(event="input")

    while True:
        myData = {}
        try:
            event, idx = raw_input("[push event to control] please input an event(idx) => ").split()
            myData["idx"] = int(float(idx))
            client.publishEvent("gowarrior", deviceId, event, "json", myData)
        except ValueError as e:
            print "Error, only [playVideo N], [stopVideo N] are supported"

except ibmiotf.ConnectionException as e:
    print e

