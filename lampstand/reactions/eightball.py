from lampstand import eightball
import lampstand.reactions.base


from lampstand.tools import splitAt
import re, time, random, sys

def __init__ ():
	pass

class Reaction(lampstand.reactions.base.Reaction):


	__name = 'Eightball'
	
	cooldown_number = 6
	cooldown_time   = 360
	uses = []

	def __init__(self, connection):
		self.channelMatch = (re.compile('^%s.?  ?ask the [oracle|8.ball]' % connection.nickname, re.IGNORECASE),
			re.compile('^%s.? should I .*' % connection.nickname, re.IGNORECASE),
                        re.compile('^%s.? should (\S+) .*' % connection.nickname, re.IGNORECASE))


	def channelAction(self, connection, user, channel, message, matchIndex):
		print "[8Ball] called"

		if not message.lower().find(" or ") == -1:
			print "[8Ball] ... That looks like a choice to me"
			return False


		if self.overUsed():
			connection.msg(user, "The 8-ball says: 'Find a new prophet, I quit.', I'd give it a while to cool down." )
			return True


		self.updateOveruse()
		
		by_proxy_match = self.channelMatch[2].match(message)
		if (by_proxy_match is not None and
                    self.channelMatch[1].match(message) is None):
                        proxy_nick = by_proxy_match.group(1)
                        if proxy_nick in connection.people:
                            connection.msg(channel, "{}: {}".filter(
                                proxy_nick, eightball.question()))
                        else:
                            connection.msg(channel,
                            "{}: Who is {}?".format(user, proxy_nick)
		else:
                    connection.msg(channel, "{}: {}".format(
                        user, eightball.question()) )

		return True
