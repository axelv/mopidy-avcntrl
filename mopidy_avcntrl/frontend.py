import pykka
from mopidy import core
from TouchListener import *

class AVCNTRLFrontend(pykka.ThreadingActor, core.CoreListener):

	pykka_traversable = True

	#
	playback_control = range(0,5)
	
	PLAY = 0
	PAUSE = 1
	FORWARD = 2
	BACKWARD = 3
	STOP = 4
	
	def __init__(self, config, core):
		print "Frontend: __init__"
		super(AVCNTRLFrontend, self).__init__()
		self.core = core
		self.config = config
		self.proxy = self.actor_ref.proxy()
		print "Frontend: Created proxy of myself"
		tl_ref = TouchListener.start()
		print "Frontend: Created actor_ref of TouchListener"
		self.tl = tl_ref.proxy()
		print "Frontend: end __init"
		self.tl.create_listener(3, callback=self.proxy.play).get()
		self.tl.create_listener(2, callback=self.proxy.pause).get()
		print "Frontend: Ready to start the loop."
		self.tl.listen(0.05)
		
	def on_stop(self):
		self.tl.stop()
		print "Frontend: stopping"
				
	def playback_action(self, action):
		try:
			if not action in self.playback_control:
				raise AttributeError
		except AttributeError:
			print "Attributes must lie in between specified limits." 
		if(action == self.__class__.PLAY):
			self.core.playback.play()
		elif(action == self.__class__.PAUSE):
			self.core.playback.play()
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
		print "Frontend: triggered play"
		self.playback_action(self.__class__.PLAY)
	def pause(self):
		print "Frontend: triggered pause"
		self.playback_action(self.__class__.PAUSE)

    # Your frontend implementation