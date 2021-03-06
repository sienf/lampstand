import lampstand.reactions.base

from lampstand.tools import splitAt
import re, time, random, sys

def __init__ ():
	pass

class Reaction(lampstand.reactions.base.Reaction):


	__name = 'Choose'
	
	cooldown_number = 6
	cooldown_time   = 360
	uses = []

	def __init__(self, connection):
		self.channelMatch = re.compile('^%s. (choose|should I) (.* or .*)' % connection.nickname, re.IGNORECASE)
		self.privateMatch = re.compile('(choose|should I) (.* or .*)\??$', re.IGNORECASE)

	def channelAction(self, connection, user, channel, message):
		print "[Choose] called"


		if self.overUsed(self.uses, self.cooldown_number, self.cooldown_time):
			connection.msg(channel, "I'm not running your life for you, go away." )
			return True
		
		self.updateOveruse()
		
		match = self.channelMatch.findall(message)


                if random.randint(0,100) == 69:
			print "Yes";
                        connection.msg(channel, "%s: Yes" % user)
			return True
                
		if random.randint(0,100) == 67:
			print "Edge";
                        connection.msg(channel, "%s: edge" % user)
			return True
		
		print match
		reaction = self.choose(match[0][1])
		if reaction.lower() == "death" and user.lower() != "aquarion":
			connection.kick(channel,user, "Death.")
		elif reaction.lower() == "boom" and user.lower():
			connection.kick(channel,user, "BOOM")
		else:
			connection.msg(channel, "%s: %s" % (user, reaction))

		return True


	def privateAction(self, connection, user, channel, message):
		print "[Choose] called"


		if self.overUsed(self.uses, self.cooldown_number, self.cooldown_time):
			connection.msg(user, "I'm not running your life for you, go away." )
			return
		
		self.updateOveruse()
		
		match = self.privateMatch.findall(message)
		print "Match: %s" % match

		reaction = self.choose(match[0][1])
		connection.msg(user, "%s: %s" % (user, reaction))

	def choose(self, message):
		if message[-1:] == "?":
			message = message[:-1]

		print message

		#new regex by ccooke - 2010-05-28
		#regex = re.compile("(?:\s*(?:\s*(?:,|x?or)\s*)+\s*)+", re.IGNORECASE);
		#regex = re.compile("(?:\s+(?:\s*(?:x?or)\s*)+\s*|,)+", re.IGNORECASE);
		regex = re.compile("(?:\s+(?:\s*(?:x?or(?=\W))\s*)+\s*|,)+\s*", re.IGNORECASE);
		choose = regex.split(message);
		

		#choose = []

		#orsplit = message.split(" or ")
		#for thing in orsplit:
		#	lst = thing.split(", ")
		#	for x in lst:
		#		choose.append(x)
		#print choose

		print choose

		for thing in choose:
			if thing.lower() == "glados":
				print "Chosen Glados"
				return "GLaDOS. Obviously"

			if thing.lower() == "hal":
				print "Removed a Hal";
				choose.remove(thing)

		print choose
		return random.choice(choose)
