import config
from temporal_lobe import listenToSurroundings
import thread

try:
	thread.start_new_thread( listenToSurroundings,("AudioCortex",))
except:
	print "Error, unable to start thread."

while 1:
	pass





