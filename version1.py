#This file uses socket communication to interface with FG and plot the data using pylab plot
from threading import Thread
from pylab import *
from string import strip, split
from time import *
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
        alldata.write(str("elapsedtime(sec) altitude(ft) heading(deg) roll(deg) pitch(deg) yaw(deg) sideslip(deg) rollrate(degps) pitchrate(degps) yawrate(degps) alpha(deg) airspeed(kt) mach verticalspeed(fps)"))
        alldata.write(str('\n'))
        while 1:
            alldata = open('alldata.csv','a')
	    data,addr = UDPSock.recvfrom(buf)
            data = data.replace('"',' ')
            alldata.write(str(data))
        UDPSock.close()
element = []
element.append([]) # elapsedtime
element.append([]) # altitude
element.append([]) # heading
element.append([]) # roll
element.append([]) # pitch
element.append([]) # yaw
element.append([]) # sideslip
element.append([]) # rollrate
element.append([]) # pitchrate
element.append([]) # yawrate
element.append([]) # alpha
element.append([]) # airspeed
element.append([]) # mach
element.append([]) # verticalspeed
class retrive(Thread):
    def run(self):
        for n in range(0,14):
            del element[n][:]
        getdata = open('alldata.csv','r')
        line = str(getdata.readline())
        while(1):
                line = str(getdata.readline())
                if(len(line) > 5):
                    fields = line.split()
                    if(len(fields) == 14):
                        for i in range(0,14):
                            element[i].append(float(fields[i]))      
class graph(Thread):
    def run(self):
        x = 0
        y = 0
        while(1):
            sleep(0.1)
            clf() # this is important because otherwise the previous plot also remains and then you dont get a dynamically shifting plot.
            plot(element[0][x:],element[1][x:])
            xmin, xmax = xlim()
            ymin, ymax = ylim()
            xlim(xmin, xmax)
            ylim(ymin, ymax)
            show()
            draw()
            x += 3
store_data = storedata()
store_data.start()
retrive = retrive()
retrive.start()
graph = graph()
graph.start()
