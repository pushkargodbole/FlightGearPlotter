#This is the first version of the chaco & traits GUI. The data plotted is realtime and dynamically updated
from threading import Thread
from string import strip, split
from socket import socket, AF_INET, SOCK_DGRAM
# Enthought imports
from enthought.traits.api import Array, Enum, HasTraits, Instance, Range
from enthought.traits.ui.api import Group, HGroup, Item, View, spring, Handler
from enthought.pyface.timer.api import Timer
# Chaco imports
from enthought.chaco.chaco_plot_editor import ChacoPlotItem

class storedata(Thread):
	element = []
	element.append([]) # 1)elapsedtime
	element.append([]) # 2)altitude
	element.append([]) # 3)heading
	element.append([]) # 4)roll
	element.append([]) # 5)pitch
	element.append([]) # 6)yaw
	element.append([]) # 7)sideslip
	element.append([]) # 8)rollrate
	element.append([]) # 9)pitchrate
	element.append([]) # 10)yawrate
	element.append([]) # 11)alpha
	element.append([]) # 12)airspeed
	element.append([]) # 13)mach
	element.append([]) # 14)verticalspeed
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
		for n in range(0,14):
			del self.element[n][:]
		while 1:
			alldata = open('alldata.csv','a')
			data,addr = UDPSock.recvfrom(buf)
			data = data.replace('"',' ')
			alldata.write(str(data))
			if(len(data) > 5):
				fields = data.split()
				if(len(fields) == 14):
					for i in range(0,14):
						self.element[i].append(float(fields[i]))
		UDPSock.close()

class Viewer(HasTraits):
""" This class just contains the two data arrays that will be updated
by the Controller.  The visualization/editor for this class is a 
Chaco plot.
"""
	index = Array 
	data = Array
	plot_type = Enum("line", "scatter")
	view = View(ChacoPlotItem("index", "data",
                               type_trait="plot_type",
                               resizable=True,
                               x_label="Time",
                               y_label="Altitude(ft)",
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=600, height=300),
                HGroup(spring, Item("plot_type", style='custom'), spring),
                resizable = True,
                buttons = ["OK"],
                width=620, height=320)

class Controller(HasTraits):
# A reference to the plot viewer object
	viewer = Instance(Viewer)
# The max number of data points to accumulate and show in the plot
	max_num_points = Range(100, 10000, 1000)
	num_ticks = 0 
	view = View(Item('max_num_points', style='custom'), 
		    resizable=True)
	def newlist(self, *args):
		cur_data = self.viewer.data
		if len(storedata.element[0]) > 2:
			new_data = storedata.element[1][-self.max_num_points:]
			new_index = storedata.element[0][-self.max_num_points:]
			self.viewer.index = new_index
			self.viewer.data = new_data
		return

class DemoHandler(Handler):
	def closed(self, info, is_ok):
        #Handles a dialog-based user interface being closed by the user.
        #Overridden here to stop the timer once the window is destroyed.
		info.object.timer.Stop()
		return
    
class Demo(HasTraits):
	controller = Instance(Controller)
	viewer = Instance(Viewer, ())
	timer = Instance(Timer)
	view = View(Item('controller', style='custom', show_label=False), 
                    Item('viewer', style='custom', show_label=False), 
                    handler = DemoHandler,
                    resizable=True)
            
	def configure_traits(self, *args, **kws):        
        # Start up the timer! We should do this only when the demo actually
        # starts and not when the demo object is created.
		self.timer=Timer(10, self.controller.newlist)
		return super(Demo, self).configure_traits(*args, **kws)
    
	def _controller_default(self):
		return Controller(viewer=self.viewer)

store_data = storedata()
store_data.start()
popup=Demo()
popup.configure_traits()
