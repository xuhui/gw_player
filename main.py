#-*-coding:utf8;-*-
#qpy:2
#qpy:console

'''
2015-09-25 : video play works, picture not work, music not implemented yet. so, clear the code for more readable
'''

import site
import time
import os, json
import sys
from subprocess import Popen
import ibmiotf.application

client = None
currentVideo = -1
videoFiles = []

def walkFiles():
    for root, dirs, files in os.walk('/storage'):
        for filename in files:
            if filename.endswith(('.mov', '.mp4', '.3gp')):
                videoFiles.append(os.path.join(root,filename))

def sysPlayVideoFile(theVideo):
    cmd = []
    cmd.append('am')
    cmd.append('start')
    cmd.append('-n')
    cmd.append('com.android.gallery3d/.app.MovieActivity')
    cmd.append('-d')
    cmd.append(theVideo)
    Popen(cmd)
    return

def stopVideo(fake):
    cmd = []
    cmd.append('am')
    cmd.append('force-stop')
    cmd.append('com.android.gallery3d')
    Popen(cmd)
    return

def cntVideo(fake):
    return

def playVideoByIndex(idx):
    if (len(videoFiles) > idx):
        video = videoFiles[idx]
        sysPlayVideoFile(video)
    else:
        video = "N/A"
    print("fake %s %d %s" % (sys._getframe().f_code.co_name, idx, video))

cases = {
    "playVideo"     : playVideoByIndex,
    "stopVideo"        : stopVideo,
    "cntVideo"      : cntVideo,
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

def player():
    walkFiles()
    print 'FOUND VIDEO>>'
    print videoFiles

    try:
        options = ibmiotf.application.ParseConfigFile("/storage/ext/usb1/blue/device.cfg")
        options["deviceId"] = options["id"]
        options["id"] = "aaa" + options["id"]
        client = ibmiotf.application.Client(options)
        client.connect()
        client.deviceEventCallback = myCommandCallback
        client.subscribeToDeviceEvents()

        i = 1
        while True:
            time.sleep(5)
            print "waiting.. %d" % i
            i = i + 1

    except ibmiotf.ConnectionException  as e:
        print e

if __name__ == '__main__':
    player()
