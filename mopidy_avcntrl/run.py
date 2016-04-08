from TouchListener import *




def hallo():
	print "Hallo"
	
def run():
	tl = TouchListener()	
	tl.create_listener(3, callback=hallo)
	print tl.listeners
	tl.run(0.05)