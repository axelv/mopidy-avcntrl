import pykka
from mopidy import core
from TouchListener import *

class AVCNTRLFrontend(pykka.ThreadingActor, core.CoreListener):

	#
	playback_control = range(0,4)
	
	PLAY = 0
	STOP = 1
	FORWARD = 2
	BACKWARD = 3
	
	def __init__(self, config, core):
		super(AVCNTRLFrontend, self).__init__()
		self.core = core
		self.config = config
		self.tl = TouchListener()
		self.tl.create_listener(3, callback=self.play())
		self.tl.run(0.05)
		
	def playback_action(self, action):
		try:
			if not action in self.playback_control:
				raise AttributeError
		except AttributeError:
			print "Attributes must lie in between specified limits." 
		if(action == self.__class__.PLAY):
			self.core.PlaybackController.play()
		elif(action == self.__class__.STOP):
			self.core.PlaybackController.stop()
		elif(action ==  self.__class__.FORWARD):
			pass
		elif(action ==  self.__class__.BACKWARD):
			pass
		else:
			pass
						
	def sourcecontrol():
		pass
		
	def play(self):
		self.playback_action("0")

    # Your frontend implementation