#First crude socket interface to FG
from threading import Thread
from pylab import *
from string import strip, split
from time import sleep
from socket import *
import csv
class storedata(Thread):
    def run(self):
        host = "localhost"
        port = 5500
        buf = 1048576
        addr = (host,port)
        UDPSock = socket(AF_INET,SOCK_DGRAM)
        UDPSock.bind(addr)
        alldata = open('alldata.csv','w')
        alldata.write(str("elapsedtime(sec) altitude(ft) heading(deg) roll(deg) pitch(deg) yaw(deg),sideslip(deg) rollrate(degps) pitchrate(degps) yawrate(degps) alpha(deg) airspeed(kt) mach verticalspeed(fps)"))
        alldata.write(str('\n'))
        while 1:
            alldata = open('alldata.csv','a')
	    data,addr = UDPSock.recvfrom(buf)
            data = data.replace('"',' ')
            alldata.write(str(data))
        UDPSock.close()
elapsedtime = []
altitude = []
heading = []
roll = []
pitch = []
yaw = []
sideslip = []
rollrate = []
pitchrate = []
yawrate = []
alpha = []
airspeed = []
mach = []
verticalspeed = []
class retrive(Thread):
    def run(self):
        getdata = open('alldata.csv','r')
        line = str(getdata.readline())
        while(1):
                line = str(getdata.readline())
                if(len(line) > 5):
                    fields = line.split()
                    elapsedtime.append(float(fields[0]))
                    altitude.append(float(fields[1]))
                    heading.append(float(fields[2]))
                    roll.append(float(fields[3]))
                    pitch.append(float(fields[4]))
                    yaw.append(float(fields[5]))
                    sideslip.append(float(fields[6]))
                    rollrate.append(float(fields[7]))
                    pitchrate.append(float(fields[8]))
                    yawrate.append(float(fields[9]))
                    alpha.append(float(fields[10]))
                    airspeed.append(float(fields[11]))
                    mach.append(float(fields[12]))
                    verticalspeed.append(float(fields[13]))
class graph(Thread):
    def run(self):
        while(1):
            sleep(0.5)
            plot(elapsedtime,altitude)
            show()
            draw()
store_data = storedata()
store_data.start()
retrive = retrive()
retrive.start()
graph = graph()
graph.start()
