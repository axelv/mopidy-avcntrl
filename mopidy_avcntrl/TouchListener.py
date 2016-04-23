# TouchListener by Axel Vanraes

import Adafruit_MPR121.MPR121 as MPR121
import time
import pykka
# TODO: refactor this code with threading. Make subclass Listener from threading.Thread that plays the role of a button.
import sys
from collections import namedtuple
Listener = namedtuple('Listener', ['mode','callback'])

class TouchListener(pykka.ThreadingActor):

	pykka_traversable = True
	
	#Maximum number of touchlisteners possible
	listener_ids = range(0,12) #0-11
	MAX_LISTENERS = len(listener_ids)
	
	#Possible modes for each listener
	TOGGLE = 0
	MOMENTARY = 1
	listener_modes = range(0,2) #0-1
	MAX_MODES = len(listener_modes)
	
	
	def __init__(self):
		print "TouchListener: __init__"
		super(TouchListener, self).__init__()
		#Initialize array of positive integer numbers
		self.listeners = [Listener(None, None) for i in self.__class__.listener_ids]
		self.__running = True
		self.cap = MPR121.MPR121()
		print "TouchListener: Created MPR121 object"
		
		
		#TODO: rewrite with exception handling system!
		# Initialize communication with MPR121 using default I2C bus of device, and 
		# default I2C address (0x5A).  On BeagleBone Black will default to I2C bus 0.
		if not self.cap.begin():
			print 'Error initializing MPR121.  Check your wiring!'
			sys.exit(1)
				
		print "TouchListener: Initilialized MPR121"

		
		#Create proxy to itself to plan future work
		self.actor_proxy = self.actor_ref.proxy()
		print "TouchListener: Created proxy to myself"
		
	def on_start(self):
		pass
		
	def on_stop(self):
		print "TouchListener: stopping"
	
	def create_listener(self, id, mode = TOGGLE, callback = None):
		try:
			id = int(id)
			mode = int(mode)
			if not id in self.__class__.listener_ids and mode in self.__class__.listener_modes:
				raise AttributeError
		except AttributeError:
			print "Attributes must lie in between specified limits."
	
		self.listeners.insert(id, Listener(mode, callback))
		
	def remove_listener(self, id):
		try:
			id = int(id)
			if not id in self.__class__.listener_ids:
				raise AttributeError
		except AttributeError:
			print "Attributes must lie in between specified limits."
		
		self.listeners.pop(id);
		
	def bind_event(self, id, callback):
		self.listeners[id].callback = callback;
		
	def remove_event(self, id, callback):
		self.listeners[id].callback = None;
		
	def test(self, id):
		self.listeners[id].callback()
		print "Test done"
		
	def listen(self, pause ):
		self.__loop(pause)
		#t = threading.Thread(target=self.__loop,args=(pause,))
		#threads.append(t)
		#t.start()
		
	def __loop(self, pause):
		last_touched = self.cap.touched()
		time.sleep(pause)
		current_touched = self.cap.touched()
		for i in self.listener_ids:
			pin_bit = 1 << i
			if current_touched & pin_bit and not last_touched & pin_bit:
				#touched
				if not self.listeners[i].callback == None:
					print "TouchListener: Touched "+i
					self.listeners[i].callback()
					print "TouchListener: Callback finished"
			if not current_touched & pin_bit and last_touched & pin_bit:
				#released
				pass
		last_touched = current_touched
		
		# schedule new command
		if(self.__running):
			self.actor_proxy.listen(pause)
		
		
		