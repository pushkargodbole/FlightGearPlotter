#This file uses threading to save multiple data elements simultaneously
from threading import Thread
from time import sleep
from FlightGear import FlightGear
from pylab import *
fg = FlightGear('localhost', 5500)
class timevsaltitude(Thread):
    def run(self):
        timealtitude = open('time-altitude.csv','w')
        timealtitude.write(str("time,altitude"))
        timealtitude.write('\n')
        while 1:
            timealtitude = open('time-altitude.csv','a')
            timealtitude.write(str(fg['/sim/time/elapsed-sec']))
            timealtitude.write(',')
            timealtitude.write(str(fg['/position/altitude-agl-ft']))
            timealtitude.write('\n')
            sleep(1)
class timevspitch(Thread):
    def run(self):
        timepitch = open('time-pitch.csv','w')
        timepitch.write(str("time,pitch"))
        timepitch.write('\n')
        while 1:
            timepitch = open('time-pitch.csv','a')
            timepitch.write(str(fg['/sim/time/elapsed-sec']))
            timepitch.write(',')
            timepitch.write(str(fg['/orientation/pitch-deg']))
            timepitch.write('\n')
            sleep(1)
class timevsroll(Thread):
    def run(self):
        timeroll = open('time-roll.csv','w')
        timeroll.write(str("time,roll"))
        timeroll.write('\n')
        while 1:
            timeroll = open('time-roll.csv','a')
            timeroll.write(str(fg['/sim/time/elapsed-sec']))
            timeroll.write(',')
            timeroll.write(str(fg['/orientation/roll-deg']))
            timeroll.write('\n')
            sleep(1)
class timevsyaw(Thread):
    def run(self):
        timeyaw = open('time-yaw.csv','w')
        timeyaw.write(str("time,yaw"))
        timeyaw.write('\n')
        while 1:
            timeyaw = open('time-yaw.csv','a')
            timeyaw.write(str(fg['/sim/time/elapsed-sec']))
            timeyaw.write(',')
            timeyaw.write(str(fg['/orientation/yaw-deg']))
            timeyaw.write('\n')
            sleep(1)
class timevssideslip(Thread):
    def run(self):
        timesideslip = open('time-sideslip.csv','w')
        timesideslip.write(str("time,sideslip"))
        timesideslip.write('\n')
        while 1:
            timesideslip = open('time-sideslip.csv','a')
            timesideslip.write(str(fg['/sim/time/elapsed-sec']))
            timesideslip.write(',')
            timesideslip.write(str(fg['/orientation/side-slip-deg']))
            timesideslip.write('\n')
            sleep(1)
class timevspitchrate(Thread):
    def run(self):
        timepitchrate = open('time-pitchrate.csv','w')
        timepitchrate.write(str("time,pitchrate"))
        timepitchrate.write('\n')
        while 1:
            timepitchrate = open('time-pitchrate.csv','a')
            timepitchrate.write(str(fg['/sim/time/elapsed-sec']))
            timepitchrate.write(',')
            timepitchrate.write(str(fg['/orientation/pitch-rate-degps']))
            timepitchrate.write('\n')
            sleep(1)
class timevsrollrate(Thread):
    def run(self):
        timerollrate = open('time-rollrate.csv','w')
        timerollrate.write(str("time,rollrate"))
        timerollrate.write('\n')
        while 1:
            timerollrate = open('time-rollrate.csv','a')
            timerollrate.write(str(fg['/sim/time/elapsed-sec']))
            timerollrate.write(',')
            timerollrate.write(str(fg['/orientation/roll-rate-degps']))
            timerollrate.write('\n')
            sleep(1)
time_altitude = timevsaltitude()
time_pitch = timevspitch()
time_roll = timevsroll()
time_yaw = timevsyaw()
time_sideslip = timevssideslip()
time_pitchrate = timevspitchrate()
time_rollrate = timevsrollrate()
time_altitude.start()
time_pitch.start()
time_roll.start()
time_yaw.start()
time_sideslip.start()
time_pitchrate.start()
time_rollrate.start()
