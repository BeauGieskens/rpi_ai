import datetime
import keyring

threshold = 100
sensitivity = 180
forceCapture = True
forceCaptureTime = 60 * 60 # Once an hour
filepath = "/home/pi/rpi_ai/video/"
filenamePrefix = "pgm"
fileType = "jpg"
saveWidth = 800 # File photo size settings
saveHeight = 600
diskSpaceToReserve = 40 * 1024 * 1024 # Keep 40 mb free on disk
CaptureDuration = 0
publicIP = keyring.get_password('my','public_ip')


gettingVoiceInput = 0
gettingStillAudio = 0

# Obsolete input variables
gettingStillImages = 0
gettingVisualInput = 0

blackLight = False
windowLamp = False

# How long to wait before stopping routine if nothing is happening
audioHangout = 60 # seconds
# How long to wait before starting up the routine again
timeTimeout = 0

debugging = False

# Need to set your own API codes 
#keyring.set_password('skybio','api_key','XX')
#keyring.set_password('skybio','api_secret','XX')
#keyring.set_password('skybio','app_name','XX')
#keyring.set_password('skybio','namespace','XX')
keyring.set_password('wolfram','app_id','L6PEJ5-34R5XV82VU')
#keyring.set_password('msft_azure','api_secret','XX')
#keyring.set_password('msft_azure','api_client','XX')
#keyring.set_password('google','api_secret','XX')



