#This is the final version of the code. The GUI is complete with all options to plot various data. The myprotocol.xml file needs to be present in the protocol directory of FG for this to work.
#Threading imports
from threading import Thread
#String imports
from string import strip, split
#Socket imports
from socket import socket, AF_INET, SOCK_DGRAM
# Enthought imports
from enthought.traits.api import Array, Enum, HasTraits, Instance, Range
from enthought.traits.ui.api import Group, HGroup, Item, View, spring, Handler
from enthought.pyface.timer.api import Timer
# Chaco imports
from enthought.chaco.chaco_plot_editor import ChacoPlotItem

#This class acquires data from FG using socket communication and stores it in a csv file. + It also stores it in a dictionary of lists named 'state'"

class storedata(Thread):
	state = {'elapsedtime(sec)':[], 'z/altitude(ft)':[],'p/roll(deg)':[],'q/pitch(deg)':[],'r/yaw(deg)':[],'u-body(ft/sec)':[],'v-body(ft/sec)':[],'w-body(ft/sec)':[],'ax(ft/sec/sec)':[],'ay(ft/sec/sec)':[],'az(ft/sec/sec)':[],'sideslip(deg)':[],'rollrate(deg/sec)':[],'pitchrate(deg/sec)':[],'yawrate(deg/sec)':[],'alpha(deg)':[],'airspeed(kt)':[],'mach':[],'verticalspeed(ft/sec)':[],'heading(deg)':[]}
	order = ['elapsedtime(sec)', 'z/altitude(ft)','p/roll(deg)','q/pitch(deg)','r/yaw(deg)','u-body(ft/sec)','v-body(ft/sec)','w-body(ft/sec)','ax(ft/sec/sec)','ay(ft/sec/sec)','az(ft/sec/sec)','sideslip(deg)','rollrate(deg/sec)','pitchrate(deg/sec)','yawrate(deg/sec)','alpha(deg)','airspeed(kt)','mach','verticalspeed(ft/sec)','heading(deg)']
	def run(self):
		host = "localhost"
		port = 5500
		buf = 1048576
		addr = (host,port)
		UDPSock = socket(AF_INET,SOCK_DGRAM)
		UDPSock.bind(addr)
		alldata = open('alldata.csv','w')
		alldata.write(str("elapsedtime(sec) z/altitude(ft) p/roll(deg) q/pitch(deg) r/yaw(deg) u(ft/sec) v(ft/sec) w(ft/sec) ax(ft/sec/sec) ay(ft/sec/sec) az(ft/sec/sec) sideslip(deg) rollrate(deg/sec) pitchrate(deg/sec) yawrate(deg/sec) alpha(deg) airspeed(kt) mach verticalspeed(ft/sec) heading(deg)"))
		alldata.write(str('\n'))
		for n in range(0,20):
			del self.state[self.order[n]][:]
		while 1:
			alldata = open('alldata.csv','a')
			data,addr = UDPSock.recvfrom(buf)
			data = data.replace('"',' ')
			alldata.write(str(data))
			if(len(data) > 5):
				fields = data.split()
				if(len(fields) == 20):
					for i in range(0,20):
						self.state[self.order[i]].append(float(fields[i]))
		UDPSock.close()
# This class is responsible for making the plots and the GUI
class Viewer(HasTraits):
#This class just contains the two data arrays that will be updated
#by the Controller.  The visualization/editor for this class is a 
#Chaco plot.
	time = Array
	z = Array
	p = Array
	q = Array
	r = Array
	u = Array
	v = Array
	w = Array
	ax = Array
	ay = Array
	az = Array
	plot_type = Enum("line", "scatter")
	view = View(Group(ChacoPlotItem("time", "z",
 			       title = 'Altitude',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label= "z (ft)",
			       y_label_font = 'modern 15',
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=500, height=350),Item("plot_type", style='custom',show_label=False),label="Altitude", dock='tab', show_labels=False),
		    Group(HGroup(ChacoPlotItem("time", "p",
 			       title = 'p/roll',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="p (deg)",
			       y_label_font = 'modern 15',
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250),
			       ChacoPlotItem("time", "q",
 			       title = 'q/pitch',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="q (deg)",
			       y_label_font = 'modern 15',
                               color="red",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),
			HGroup(ChacoPlotItem("time", "r",
 			       title = 'r/yaw',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="r (deg)",
			       y_label_font = 'modern 15',
                               color="green",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),Item("plot_type", style='custom',show_label=False),label="Attitude", dock='tab', show_labels=False),
		    Group(HGroup(ChacoPlotItem("time", "u",
 			       title = 'u-Body',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="u (ft/sec)",
			       y_label_font = 'modern 15',
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250),
			       ChacoPlotItem("time", "v",
 			       title = 'v-Body',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="v (ft/sec)",
			       y_label_font = 'modern 15',
                               color="red",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),
			HGroup(ChacoPlotItem("time", "w",
 			       title = 'w-body',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="w (ft/sec)",
			       y_label_font = 'modern 15',
                               color="green",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),Item("plot_type", style='custom',show_label=False),label="Body-velocities", dock='tab', show_labels=False),
		    Group(HGroup(ChacoPlotItem("time", "ax",
 			       title = 'ax',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="ax (ft/sec/sec)",
			       y_label_font = 'modern 15',
                               color="blue",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250),
			       ChacoPlotItem("time", "ay",
 			       title = 'ay',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="ay (ft/sec)",
			       y_label_font = 'modern 15',
                               color="red",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),
			HGroup(ChacoPlotItem("time", "az",
 			       title = 'az',
                               type_trait="plot_type",
                               resizable=True,
                               x_label="\nTime",
			       x_label_font = 'modern 15',
                               y_label="az (ft/sec)",
			       y_label_font = 'modern 15',
                               color="green",
                               bgcolor="white",
                               border_visible=True,
                               border_width=1,
                               padding_bg_color="lightgray",
                               width=400, height=250), show_labels=False),Item("plot_type", style='custom',show_label=False),label="Body-accelerations", dock='tab', show_labels=False),
                resizable = True,
                buttons = ["OK"],width=600,height=400)

#This part sets the ranges of all the plots dynamically so that we get a shifting plot.
class Controller(HasTraits):
	# A reference to the plot viewer object
	viewer = Instance(Viewer)
	# The max number of data points to accumulate and show in the plot
	max_num_points = Range(50, 10000, 1000)
	view = View(Item('max_num_points', style='custom'), 
		    resizable=True)
	def newlist(self, *args):
		if len(storedata.state['elapsedtime(sec)']) > 2:
			self.viewer.time = storedata.state['elapsedtime(sec)'][-self.max_num_points:]
			self.viewer.z = storedata.state['z/altitude(ft)'][-self.max_num_points:]
			self.viewer.p = storedata.state['p/roll(deg)'][-self.max_num_points:]
			self.viewer.q = storedata.state['q/pitch(deg)'][-self.max_num_points:]
			self.viewer.r = storedata.state['r/yaw(deg)'][-self.max_num_points:]
			self.viewer.u = storedata.state['u-body(ft/sec)'][-self.max_num_points:]
			self.viewer.v = storedata.state['v-body(ft/sec)'][-self.max_num_points:]
			self.viewer.w = storedata.state['w-body(ft/sec)'][-self.max_num_points:]
			self.viewer.ax = storedata.state['ax(ft/sec/sec)'][-self.max_num_points:]
			self.viewer.ay = storedata.state['ay(ft/sec/sec)'][-self.max_num_points:]
			self.viewer.az = storedata.state['az(ft/sec/sec)'][-self.max_num_points:]
		return

#Handles a dialog-based user interface being closed by the user.
#Overridden here to stop the timer once the window is destroyed.
class DemoHandler(Handler):
	def closed(self, info, is_ok):
		info.object.timer.Stop()
		return
#This class combines and is the key to execution of the code in classes 'Viewer' and 'Controller'    
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
#These are the command lines for running the entire code written above
def main():
	store_data = storedata()
	store_data.start()
	popup=Demo()
	popup.configure_traits()

if __name__ == '__main__':
	main()

