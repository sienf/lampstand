from lampstand import bible
from lampstand.tools import splitAt
import re, time, random, sys
import lampstand.reactions.base

def __init__ ():
	pass

class Reaction(lampstand.reactions.base.Reaction):
	__name = 'Bible'

	cooldown_number = 3
	cooldown_time   = 120
	uses = []

	def __init__(self, connection):
		self.channelMatch = re.compile('%s. (\w*) (\d+\:\S+)' % connection.nickname, re.IGNORECASE)
		self.privateMatch = re.compile('(\w*) (\d+\:\S+)')

	def channelAction(self, connection, user, channel, message):
		matches = self.channelMatch.findall(message);


		if self.overUsed():
			connection.msg(user, "Enough with the religion for now. (Overuse triggered)")
			return

		print "[Bible] %s" % matches

		bibleConnection = bible.ESVSession()
		result = bibleConnection.doPassageQuery('%s %s' % (matches[0][0], matches[0][1]))

		result = ' '.join(result.split('\n'))

		self.updateOveruse()

		if len(result) > 880*2:

			whereToSplit = splitAt(result, 860)
			result = "%s [Cut for length]" % result[0:whereToSplit]

		if len(result) > 440:
			whereToSplit = splitAt(result, 440)
			stringOne = result[0:whereToSplit]
			stringTwo = result[whereToSplit:]

			connection.msg(channel, "%s... " % stringOne)
			connection.msg(channel, "... %s [ESV]" % stringTwo)
		else:
			connection.msg(channel, "%s [ESV]" % result)

		return True
	
	def privateAction(self, connection, user, channel, message):
		matches = self.privateMatch.findall(message);


		print "[Bible] %s" % matches

		bibleConnection = bible.ESVSession()
		result = bibleConnection.doPassageQuery('%s %s' % (matches[0][0], matches[0][1]))

		result = ' '.join(result.split('\n'))

		if len(result) > 880*2:

			whereToSplit = splitAt(result, 860)
			result = "%s [Cut for length]" % result[0:whereToSplit]

		if len(result) > 440:
			whereToSplit = splitAt(result, 440)
			stringOne = result[0:whereToSplit]
			stringTwo = result[whereToSplit:]

			connection.msg(user, "%s... " % stringOne)
			connection.msg(user, "... %s [ESV]" % stringTwo)
		else:
			connection.msg(user, "%s [ESV]" % result)

		return True
