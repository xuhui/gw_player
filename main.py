#-*-coding:utf8;-*-
#qpy:2
#qpy:console

'''
hi there
'''

import site
import time
import os, json
import sys
from subprocess import Popen
import ibmiotf.application

client = None

currentVideo = -1
currentMusic = -1
currentPicture = -1

pictureFiles = []
videoFiles = []
audioFiles = []

def walkFiles():
    for root, dirs, files in os.walk('/storage'):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg')):
                pictureFiles.append(os.path.join(root,filename))
            if filename.endswith(('.mov', '.mp4', '.3gp')):
                videoFiles.append(os.path.join(root,filename))
            if filename.endswith(('.ogg', '.mp3')):
                audioFiles.append(os.path.join(root,filename))

def sysPlayVideFile(theVideo):
  cmd = []
  cmd.append('am')
  cmd.append('start')
  cmd.append('-n')
  cmd.append('com.android.gallery3d/.app.MovieActivity')
  cmd.append('-d')
  cmd.append(theVideo)
  Popen(cmd)
  return

def sysShowPictureFile(thePicture):
  cmd = []
  cmd.append('am')
  cmd.append('start')
  cmd.append('-n')
  cmd.append('com.android.gallery3d/PhotoView')
  cmd.append('-a')
  cmd.append('android.intent.action.VIEW')
  cmd.append('-t')
  cmd.append('image/*')
  cmd.append('-d')
  cmd.append(thePicture)
  Popen(cmd)
  return



def playVideo(idx):
    if (len(videoFiles) > idx):
        video = videoFiles[idx]
        sysPlayVideFile(video)
    else:
        video = "N/A"
    print("fake %s %d %s" % (sys._getframe().f_code.co_name, idx, video))

def playMusic(idx):
    print("fake %s %d" % (sys._getframe().f_code.co_name, idx))

def showPicture(idx):
    if (len(pictureFiles) > idx):
        pic = pictureFiles[idx]
        sysShowPictureFile(pic)
    else:
        pic = "N/A"
    print("fake %s %d %s" % (sys._getframe().f_code.co_name, idx, pic))

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

def player():
	walkFiles()
	print 'FOUND VIDEO>>'
	print videoFiles
	print 'FOUND MUSIC>>'
	print audioFiles
	print 'FOUND PICTURE>>'
	print pictureFiles


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
