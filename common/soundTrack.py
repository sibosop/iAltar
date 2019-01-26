#!/usr/bin/env python
import os
import sys
home = os.environ['HOME']
proj = home+"GitProjects/iAltar"
sys.path.append(proj+"/iAltar")
sys.path.append(proj+"/config")
sys.path.append(proj+"/common")
sys.path.append(proj+"/server")
import random
import time
import threading
import numpy as np
import pygame

debugSoundTrack=True
eventMin=100
eventMax=10000
backgroundCount=0
eventTimeThresholdIncrement=.1
initialEventTimeThreshold=2.5
eventTimeThreshold=initialEventTimeThreshold
eventTimeMaxThreshold = 50.0
allowBackgroundThreshold=20.0
backgroundThreshold=90.0
backgroundIgnoreCount=8
speedChangeThreshold=20
speedChangeMin = 0.5
speedChangeMax = 2.0
doSpeedX=True

eventMutex=threading.Lock()
eventMaxVol=.7

def speedx(sound, factor):
  rval = None
  try:
    print("speedx factor:"+str(factor))
    sound_array = pygame.sndarray.array(sound)
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    rval = pygame.sndarray.make_sound(sound_array[ indices.astype(int) ])
  except Exception as e:
    print("speedx:"+str(e))
  return rval

def setup():
  pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
  pygame.init()

def getBusyChannels():
  count = 0
  for i in range(pygame.mixer.get_num_channels()):
    if pygame.mixer.Channel(i).get_busy():
      count +=1
  return count

def isWav(f):
  try:
    ext = f.rindex(".wav")
  except ValueError:
    if debugSoundTrack:
      print(sfile+ ":not wav file")
    return False
  flag = f[ext:]
  if debugSoundTrack:
    print("flag ext = "+flag)
  if flag != ".wav":
    return False
  return True

def makeEventChoice(filenames):
  done = False
  while not done:
    if filenames is None:
      print("eventdir ="+config.specs['eventDir'])
      filenames = next(os.walk( config.specs['eventDir']))[2]
    choice = random.choice(filenames)
    done = isWav(choice)
  return (choice,filenames)


def playSound(sound,l,r):
  eventChan = None
  eventChan=pygame.mixer.find_channel()
  if eventChan is None:
    pygame.mixer.set_num_channels(pygame.mixer.get_num_channels()+1);
    eventChan=pygame.mixer.find_channel()
  print("busy channels:"+str(getBusyChannels()))
  print("l: "+str(l) + " r:"+str(r))
  eventChan.set_volume(l,r)
  eventChan.play(sound)
  eventChan.set_endevent()
  

class playEvent(threading.Thread):
  def run(self):
    global backgroundCount
    global backgroundCount
    global eventTimeThreshold
    global allowBackgroundThreshold
    global backgroundThreshold
    global backgroundIgnoreCount
    global eventTimeThresholdIncrement
    global initialEventTimeThreshold
    global eventTimeMaxThreshold
    global eventMutex
    filenames=None
    print("play event thread")
    while True:
      while True:
        filenames=None
        vars = makeEventChoice(filenames)
        filenames = vars[1]
        choice = config.specs['eventDir']+vars[0]
        print("soundTrack choice:"+choice)
        try:
          sound = pygame.mixer.Sound(file=choice)
          len = sound.get_length()
          print(choice+" len:"+str(len)
                + " allowBackgroundThreshold:"+ str(allowBackgroundThreshold)
                + " eventTimeThreshold:"+str(eventTimeThreshold)
                + " backgroundCount:"+str(backgroundCount))
          if eventTimeThreshold > allowBackgroundThreshold and len > backgroundThreshold:
            if backgroundCount == 0:
              backgroundCount = backgroundIgnoreCount
              print("playing"+choice+" len:"+str(len))
              break
            else:
              print("skipping "+choice+" len:"+str(len))
          elif len < eventTimeThreshold:
            print("playing " + choice + " len:"+str(len)
                  +" threshold:"+str(eventTimeThreshold))
            break
          else:
            print("skipping "+choice+" len:"+str(len)
                  +" threshold:"+str(eventTimeThreshold))

        except Exception as e:
          print("error on Sound file:"+str(e))
      if doSpeedX:
        if sound.get_length() < speedChangeThreshold:
          factor = ((speedChangeMax-speedChangeMin) * random.random()) +speedChangeMin
          nsound = speedx(sound,factor)
          if nsound is not None:
            sound = nsound
      l = random.random() * eventMaxVol
      r = random.random() * eventMaxVol
      playSound(sound,l,r)
      eventMutex.acquire()
      eventTimeThreshold += eventTimeThresholdIncrement
      eventMutex.release()
      if  eventTimeThreshold > eventTimeMaxThreshold :
        eventMutex.acquire()
        eventTimeThreshold = initialEventTimeThreshold
        eventMutex.release()
        print("reseting eventTimeThreshold max:"+str(eventTimeMaxThreshold))

      nt = random.randint(eventMin,eventMax)/1000.0;
      print("next play:"+str(nt))
      time.sleep(nt)
      print("back from sleep")

