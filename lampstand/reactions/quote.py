from lampstand.tools import splitAt
import lampstand.reactions.base
from lampstand import tools
import os.path
import re, time, datetime

def __init__ ():
	pass

class Reaction(lampstand.reactions.base.Reaction):
	__name = 'Quote This'

	admin = ("aquarion")

	cooldown_number   = 5
	cooldown_time     = 120
	uses              = []

	last_quote_seen	  = False
	schedule_count    = 6
	
	
	def __init__(self, connection):
		self.channelMatch = (re.compile('%s: quote (.*?) (.*)\s*$' % connection.nickname, re.IGNORECASE),
					re.compile('%s: quote (.*?)$' % connection.nickname, re.IGNORECASE))
		self.dbconnection = connection.dbconnection

	def channelAction(self, connection, user, channel, message, matchIndex = False):
		
		print 'Looking at <<%s>>' % message

		matches = self.channelMatch[matchIndex].findall(message)[0]
		
		memory = False

		for module in connection.channelModules:
			if module.__name == "Memory":
				memory = module;
		

		if matchIndex == 1:
			result = memory.search(channel, matches);
			quotedUser = matches
		elif matchIndex == 0:	
			result = memory.search(channel, matches[0], matches[1]);
			quotedUser = matches[0]

		if quotedUser.lower() == user.lower():
			connection.msg(channel, "%s: Don't do that, you'll go blind" % user);
			return True


		if len(result) == 0:
			connection.msg(channel, "%s: Sorry, I've no idea what you're talking about" % user)
			return True

		else:
			print result
			line = result[-1]
			connection.msg(channel, "%s: Okay, quoting \"%s: %s\"" % (user, line['user'], line['message']))
			# Full Texts  	id 	body 	notes 	rating 	votes 	submitted 	approved 	flagged 	score
			quote = "%s: %s" % (line['user'], line['message'])
			sub = "Submitted by %s" % user
			
	                cursor = self.dbconnection.cursor()
	                cursor.execute('insert into chirpy.mf_quotes values (0, %s, %s, 0, 0, NOW(), 0, 0, 0)', (quote, sub) )
	                self.dbconnection.commit()
	
		return True

        def scheduleAction(self, connection):


		self.schedule_count = self.schedule_count + 1

		if self.schedule_count == 20:
			self.schedule_count = 0

		if not self.schedule_count == 0:
			return

		channel = "#maelfroth"

		if not self.last_quote_seen:
			q = "select submitted from chirpy.mf_quotes where approved = 1 order by submitted desc limit 1"
			cursor = self.dbconnection.cursor()
			cursor.execute(q)
			result = cursor.fetchone()
			self.last_quote_seen = result[0]
			print "Defaulting last seen: %s" % self.last_quote_seen

		print "[Quote] Looking for quotes submitted > %s" % self.last_quote_seen

		q = "select submitted from chirpy.mf_quotes where submitted > %s and approved = 1 order by submitted desc"
		cursor = self.dbconnection.cursor()
		cursor.execute(q, self.last_quote_seen)

		if cursor.rowcount > 0:
			print "[Quote] Sending message"

			url = "http://www.maelfroth.org/quotes/index.cgi?action=browse"
			if cursor.rowcount == 1:
				msg = "One new quote has been approved at %s" % url
			else:
				msg = "%d new quotes have been approved at %s" % (cursor.rowcount, url)

			connection.msg(channel, msg)
			quote = cursor.fetchone()
			self.last_quote_seen = quote[0]

