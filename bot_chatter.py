from chatterbotapi import ChatterBotFactory, ChatterBotType

def getAIresponse(s):
	try: 
		return getAIresponse2(s)
	except:
		return "Sorry, I can't do that."

def getAIresponse2(s):
	factory = ChatterBotFactory()
	bot = factory.create(ChatterBotType.CLEVERBOT)
	bot_session = bot.create_session()
	response = bot_session.think(s)
	return response
