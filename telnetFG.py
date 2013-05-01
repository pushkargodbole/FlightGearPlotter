#This file uses telnet to access FG's data and store it in a csv file
from FlightGear import FGTelnet
from threading import Thread
from pylab import *
from string import strip, split
from time import sleep
class makecsv(Thread):
    def run(self):
        csv = open('alldata.csv','w')
        csv.write(str("heading(deg),roll(deg),pitch(deg),headingmag(deg),sideslip(deg),rollrate(degps),yawrate(degps),sideslip(rad),alpha(deg),yaw(deg),pitchrate(degps),time(sec),airspeed(kt),mach,verticalspeed(fps)"))
        csv.write(str('\n'))
        global write_count
        write_count = 0
        while 1:
            csv = open('alldata.csv','a')
            orientation = (str(FGTelnet('localhost',5500).ls('/orientation/')))
            time = (str(FGTelnet('localhost',5500).get('/sim/time/elapsed-sec')))
            velocities = (str(FGTelnet('localhost',5500).ls('/velocities/')))
            orientation = orientation.replace(']','')
            orientation = orientation.replace('=\\t\'\'\\t(none)\\r",','=\\t\'0.0\'\\t(double)\\r",')
            o_fields = orientation.split()
            velocities = velocities.replace(']','')
            velocities = velocities.replace('=\\t\'\'\\t(none)\\r",','=\\t\'0.0\'\\t(double)\\r",')
            v_fields = velocities.split()
            for n in range(0,11):
                o_fields[2*n+1] = o_fields[2*n+1][4:]
                csv.write(str(o_fields[2*n+1].rstrip('\'\\t(double)\\r",')))
                csv.write(str(","))
            temp = time.split()[2]
            k = len(temp)-1
            csv.write(str(temp[1:k]))
            for n in range(6,9):
                v_fields[2*n+1] = v_fields[2*n+1][4:]
                csv.write(str(","))
                csv.write(str(v_fields[2*n+1].rstrip('\'\\t(double)\\r",')))
            csv.write(str('\n'))
            write_count = write_count + 1
make_csv = makecsv()
make_csv.start()
