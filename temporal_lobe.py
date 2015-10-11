import config
import wolframalpha, wikipedia
from bot_chatter import getAIresponse
from mouth_function import saySomething
import re
import os
import urllib, urllib2, json, requests
from timeout import timeout
import keyring
import sys
import speech_recognition as sr

# audio_cortex merge
import pyaudio
import audioop
import time, datetime
 
# Translate text with Microsoft Translation
def translateText(s,language): 
	translation = ""
	try:
		pattern = re.compile('([^\s\w]|_)+')
		b_string = re.sub(pattern, '', s.lower())
		phrase=" " + b_string + " "
		pattern = re.compile("\\b(in|chinese|italian|german|hebrew|say|translate|spanish|to)\\W", re.I)
		phrase_noise_removed = [pattern.sub("", phrase)] 
		text = phrase_noise_removed[0]
		print "translating " + text + " to " + language + "..."
		args = {
			'client_id': keyring.get_password('msft_azure','api_client'),#your client id here
			'client_secret': keyring.get_password('msft_azure','api_secret'),#your azure secret here
			'scope': 'http://api.microsofttranslator.com',
			'grant_type': 'client_credentials'
			}
			
		oauth_url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
		oauth_junk = json.loads(requests.post(oauth_url,data=urllib.urlencode(args)).content)
		translation_args = {
			'text': text,
			'to': language,
			'from': 'en'
			}
		 
		headers={'Authorization': 'Bearer '+oauth_junk['access_token']}
		translation_url = 'http://api.microsofttranslator.com/V2/Ajax.svc/Translate?'
		translation_result = requests.get(translation_url+urllib.urlencode(translation_args),headers=headers)
		translation=translation_result.text[2:-1]
		print 'Translating ' + translation_args["text"]
		print 'Translation: ' + translation
		return translation
	except:
		print "Unexpected error:", sys.exc_info()[0]
	

# Play song with VLC
def playMusic(query):
	
	# get YouTube list
	pattern = re.compile('([^\s\w]|_)+')
	b_string = re.sub(pattern, '', query)
	phrase=b_string
	pattern = re.compile("\\b(some|play)\\W", re.I)
	query = [pattern.sub("", phrase)] 
	# get YouTube list
	query = query[0]
	print query
	url = "https://www.googleapis.com/youtube/v3/search?part=snippet&key="+keyring.get_password('google','api_secret')+"&q="+urllib.quote_plus(query)+"&type=video"
	response = urllib2.urlopen(url)
	jsonResp = response.read()
	decoded = json.loads(jsonResp)
	#os.system('echo \''+url+'\' > url.txt') #for debugging
	url = 'http://youtube.com/watch?v=' + decoded['items'][0]['id']['videoId']
	theSongName = decoded['items'][0]['snippet']['title']
	pattern = re.compile("([^a-zA-Z\d\s:,.']|_)+")
	theSongName = re.sub(pattern, '', theSongName)
	#for x in range(1,len(decoded['items'])):
	#url = url + ' ' + 'http://youtube.com/watch?v=' + decoded['items'][x]['id']['videoId']
	permission = audio_cortex.getUserPermission("Do you want to hear " + theSongName)
	if permission:
		vlc = 'cvlc --no-video --volume 270 -A alsa,none --alsa-audio-device hw:1' + ' ' + url + ' --play-and-exit &'
		print url
		os.system(vlc)
		print "started music.."
		return "Sure I'll play " + theSongName
	else:
		return "Okay, I will play nothing."

# Look up declarative knowledge with Wolfram
def wolframLookUp(a_string):
	client = wolframalpha.Client(keyring.get_password('wolfram','app_id'))
	pattern = re.compile('([^\s\w]|_)+')
	b_string = re.sub(pattern, '', a_string)
	phrase=b_string
	pattern = re.compile("\\b(what|is)\\W", re.I)
	phrase_noise_removed = [pattern.sub("", phrase)] 
	try:
		res= client.query(a_string)
		return next(res.results).text
	except:
		return "Sorry"

def wikipediaLookUp(a_string,num_sentences):
	print a_string
	pattern = re.compile('([^\s\w]|_)+')
	b_string = re.sub(pattern, '', a_string)
	phrase=b_string
	print phrase
	pattern = re.compile("\\b(lot|lots|a|an|who|can|you|what|is|info|somethings|whats|have|i|something|to|know|like|Id|information|about|tell|me)\\W", re.I)
	phrase_noise_removed = [pattern.sub("", phrase)] 
	print phrase_noise_removed[0]
	a = wikipedia.search(phrase_noise_removed[0])
	print a[0]
	the_summary = (wikipedia.summary(a[0], sentences=num_sentences))
	print the_summary
	return the_summary	
	

def processInput(s):
	s = s.lower()
	print "You entered %s" % (s)
	rsp = ""
	language="en"
	if "spanish" in s:
		language = 'es'
		try:
			rsp = translateText(s,language)
		except:
			language = 'en'
			print "Unexpected error:", sys.exc_info()[0]
			rsp = 'Language services not accessible at this time'
	elif "german" in s:
		language = 'de'
		try:
			rsp = translateText(s,language)
		except:
			language = 'en'
			rsp = 'Language services not accessible at this time'
	elif "italian" in s:
		language = 'it'
		try:
			rsp = translateText(s,language)
		except:
			language = 'en'
			rsp = 'Language services not accessible at this time'
	elif "play" in s:
		rsp = playMusic(s)
	elif "music" in s:
		if any(["stop", "cancel", "kill", "close"] in s:
			os.system('pkill vlc')
	elif "what is the" in s or "what's the" in s:	
		rsp = wolframLookUp(s)
		if "Sorry" in rsp:
			rsp = getAIresponse(s)
	elif "how many" in s:
		rsp = wolframLookUp(s)
		if "Sorry" in rsp:
			rsp = getAIresponse(s)
	elif "tell me" in s:
		if "lot" in s:
			try:
				rsp = wikipediaLookUp(s,2)
			except:
				try:
					rsp = wikipediaLookUp(s,2)
				except:
					rsp = "I am sorry, I can not access that information."
		else:
			try:
				rsp = wikipediaLookUp(s,2)
			except:
				try:
					rsp = wikipediaLookUp(s,2)
				except:
					rsp = "I am sorry, I can not access that information."
	elif "do you know" in s:
		try:
			rsp = wikipediaLookUp(s,2)
		except:
			try:
				rsp = wikipediaLookUp(s,2)
			except:
				rsp = "I am sorry, I can not access that information."
	elif "who" in s:
		try:
			rsp = wikipediaLookUp(s,1)
		except:
			try:
				rsp = wikipediaLookUp(s,1)
			except:
				rsp = "I am sorry, I can not access that information."
	elif "shut" in s and "down" in s:
		saySomething("Shutting the computer down")
		os.system("sudo shutdown now &")
	else:
		rsp = getAIresponse(s)
	print rsp

	pattern = re.compile("([^a-zA-Z\d\s:,.']|_)+")
	rsp = re.sub(pattern, '', rsp)
	print rsp + " in " + language
	saySomething(rsp)		


# audio_cortex merge

def getUserPermission(question):
    answer = 0
    saySomething(question)
    response = getUsersVoice(2)
    if "yes" in response or "sure" in response or "okay" in response:
        answer = 1
    return answer
	
def listenToSurroundings(threadName):
    try:
        print "Started listening on thread %s" % threadName
        chunk = 1024
        
        if config.debugging:
            rms = []
            for i in range(0,10):
                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=chunk)
                data = stream.read(chunk)
                rmsTemp = audioop.rms(data,2)
                print rmsTemp
                rms.append(rmsTemp)
                rmsMean = numpy.mean(rms)
                rmsStd = numpy.std(rms)
                print rms
                stream.stop_stream()
                stream.close()
                p.terminate()
        
        volumeThreshold = 1050 # set after running the previous commands and looking at vtput
        print "Volume threshold set at %2.1f" % volumeThreshold 
        lastInterupt = datetime.datetime.now()
        
        while True:
            if config.gettingStillImages and config.gettingStillAudio:
                pass
            elif config.gettingVisualInput:
                time.sleep(5)
            else:
                print "Starting listening stream"
                lastInterupt = datetime.datetime.now()
                config.gettingStillAudio = 0
                rmsTemp = 0
                p = pyaudio.PyAudio()
                stream = p.open(format=pyaudio.paInt16,channels=1,rate=16000,input=True,frames_per_buffer=chunk)
                # listen to surroundings
                while rmsTemp < volumeThreshold and not config.gettingVisualInput:
                    data = stream.read(chunk)
                    rmsTemp = audioop.rms(data,2)
                    timeDifference = datetime.datetime.now() - lastInterupt
                    if timeDifference.total_seconds() > config.audioHangout:
                        config.gettingStillAudio = 1
                    if config.gettingStillAudio and config.gettingStillImages:
                        break
                stream.stop_stream()
                stream.close()
                p.terminate()
                if not config.gettingVisualInput and not config.gettingStillAudio:
                    config.timeTimeout = 0 # reset timeout
                    config.gettingVoiceInput = 1
                    output = getUsersVoice(5)
                    processInput(output)
                    config.gettingVoiceInput = 0
    except:
        import traceback
    print traceback.format_exc()

def getUsersVoice(speakingTime):
        os.system("aplay sounds/blip.wav > /dev/null 2>&1 ")
        os.system("arecord -D plughw:1,0 -f cd -d %d out.wav" % speakingTime)
        os.system("aplay sounds/elevbell1.wav > /dev/null 2>&1")
        #os.system("parseVoiceText.sh")

        # obtain path to "test.wav" in the same folder as this script
        from os import path
        WAV_FILE = path.join(path.dirname(path.realpath(__file__)), "out.wav")

        # use "out.wav" as the audio source
        r = sr.Recognizer()
        with sr.WavFile(WAV_FILE) as source:
                audio = r.record(source) # read the entire WAV file

        # recognize speech using Google Speech Recognition
        try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                output = r.recognize_google(audio)
                print("Google Speech Recognition thinks you said " + output)
        except sr.UnknownValueError:
                output = 'empty'
                print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
                output = 'empty'
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
        #output = ""
        #with open('txt.out','r') as f:
        #        output = f.readline()
        print "output:"
        print output#[1:-2]
        theOutput = output#[1:-2]
        return theOutput
