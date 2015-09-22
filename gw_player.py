#qpy:2
#qpy:console

'''
hi there
'''

import site
import time
import os, json
import sys
import ibmiotf.application

currentVideo = -1
currentMusic = -1
currentPicture = -1

client = None

def playVideo(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def playMusic(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def showPicture(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def nextVideo(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def nextMusic(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def nextPicture(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def cntVideo(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def cntMusic(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def cntPicture(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

cases = {
    "playVideo"     : playVideo,
    "playMusic"     : playMusic,
    "showPicture"   : showPicture,
    "nextVideo"     : nextVideo,
    "nextMusic"     : nextMusic,
    "nextPicture"   : nextPicture,
    "cntVideo"      : cntVideo,
    "cntMusic"      : cntMusic,
    "cntPicture"    : cntPicture,
}

def handle(cmd, idx = 0):
    if cmd in cases.keys():
        return cases[cmd](idx)
    else:
        print "boom!"
        return

def myCommandCallback(cmd):
    if "idx" in cmd.data.keys():
        idx = cmd.data["idx"]
    else:
        idx = 0
    handle(cmd.event, idx)

try:
    options = ibmiotf.application.ParseConfigFile("device.cfg")
    options["deviceId"] = options["id"]
    options["id"] = "aaa" + options["id"]
    client = ibmiotf.application.Client(options)
    client.connect()
    client.deviceEventCallback = myCommandCallback
    client.subscribeToDeviceEvents()

    while True:
        # myData = {'cntVideo' : 12}
        # client.publishEvent("gowarrior", options["deviceId"], "input", "json", myData)
        time.sleep(5)

except ibmiotf.ConnectionException  as e:
    print e

