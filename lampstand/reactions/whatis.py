from lampstand.tools import splitAt
import lampstand.reactions.base
from lampstand import tools
import os.path
import re, time

def __init__ ():
	pass

class Reaction(lampstand.reactions.base.Reaction):
	__name = 'What is this thing?'

	admin = ("aquarion")

	cooldown_number   = 5
	cooldown_time     = 120
	uses              = []

	blame = "No idea"
	lastasked = ""
	lastasked2 = ""
	
	
	def __init__(self, connection):
		self.channelMatch = (re.compile('%s: (re|)define (.*?) as (.*)\s*$' % connection.nickname, re.IGNORECASE),
			re.compile('%s: What is (.*?)\??$' % connection.nickname, re.IGNORECASE),
			re.compile('%s: Who defined that\??$' % connection.nickname, re.IGNORECASE),
			re.compile('%s: Literal (.*)\s*$' % connection.nickname, re.IGNORECASE),
			re.compile('%s: (|give me a) Random definition' % connection.nickname, re.IGNORECASE))
		self.dbconnection = connection.dbconnection

	def channelAction(self, connection, user, channel, message, matchIndex = False):
		
		print 'Looking at <<%s>>' % message


		matches = self.channelMatch[matchIndex].findall(message)[0]

		if(matchIndex == 0):
			return self.setDefinition(connection, user, channel, message, matches)
		elif (matchIndex ==1):
			return self.getDefinition(connection, user, channel, message, matches)
		elif (matchIndex ==2):
			return self.getBlame(connection, user, channel, message, matches)
		elif (matchIndex ==3):
			return self.getLiteral(connection, user, channel, message, matches)
		elif (matchIndex ==4):
			return self.randomThing(connection, user, channel, message)
			

                #if self.overUsed(self.uses):
                #        connection.msg(channel, self.overuseReactions[matchIndex])
                #        return True


                ## Overuse Detectection ##
                #self.uses.append(int(time.time()))
                #if len(self.uses) > self.cooldown_number:
                #        self.uses = self.uses[0:self.cooldown_number-1]
                ## Overuse Detectection ##

	def setDefinition(self, connection, user, channel, message, matches):
		
		key = matches[1]
		value = matches[2]

		if key.lower() == "glados":
			connection.msg(channel, "%s: Nope" % user)
			return True

		cursor = self.dbconnection.cursor()

		query = "Select * from define where lower(word) = %s and lower(definition) = %s"
		cursor.execute(query, (key.lower(), value.lower()) )
		if cursor.fetchone():
			connection.msg(channel, "%s: I already had it that way" % user)
			return True

		query = "insert into define values (0, %s, %s, %s, NOW())";
		cursor.execute(query, (key, value, user) )
		connection.msg(channel, "%s: If you say so." % user)
		return True


	def getDefinition(self, connection, user, channel, message, matches):

		key = matches

		if key == self.lastasked and key == self.lastasked2:
			connection.kick(channel, user, "Bored now.")
			return True

		if key == self.lastasked:
			connection.msg(channel, "%s: I just said, %s" % (user, self.answered))
			return True

		if key.lower() == "glados":
			connection.msg(channel, "%s: The AI of my dreams" % user)
			return True

		row = self.define(key)

		if row:
			connection.msg(channel, "%s: %s" % (user, row[1]))
			self.blame = row[2]
			self.lastasked2 = self.lastasked
			self.lastasked = key
			self.answered = row[1]
		else:
			connection.msg(channel, "%s: No Clue" % user)
		
		return True


	def define(self, key):

		cursor = self.dbconnection.cursor()
		query = "Select word,definition,author from define where lower(word) = %s order by rand()"

		cursor.execute(query, (key.lower(), ) )
		return cursor.fetchone()


	def getBlame(self, connection, user, channel, message, matches):

		if self.blame.lower() == user.lower():
			connection.msg(channel, "%s: You did." % (user, ))
		else:
			connection.msg(channel, "%s: %s" % (user, self.blame))

		return True

	def randomThing(self, connection, user, channel, message):
		
                cursor = self.dbconnection.cursor()
                query = "Select word,definition,author from define order by rand()"

                cursor.execute(query)
                row = cursor.fetchone()

                connection.msg(channel, "%s: %s is %s" % (user, row[0], row[1]))
                self.blame = row[2]

                return True



	def getLiteral(self, connection, user, channel, message, matches):

		key = matches

		if not user.lower() in self.admin:
			row = self.define(key)
			if row:
				connection.msg(channel, "%s: %s is *literally* \"%s\"" % (user, row[0], row[1]))
				self.blame = row[2]
				self.lastasked2 = self.lastasked
				self.lastasked = key
				self.answered = row[1]
			else:
				connection.msg(channel, "%s: Literally No Clue" % user)
			

		cursor = self.dbconnection.cursor()
		query = "Select word,definition,author from define where lower(word) = %s"

		cursor.execute(query, (key.lower(), ) )

		defines = []

		rows = cursor.fetchall()

		for row in rows:
			defines.append(row[1])

		if len(defines) > 1:
			result = '"'
			result += "\", \"".join(defines[0:-1])
			result += "\" & \"%s\"" % defines[-1]
		elif len(defines) == 1:
			result = defines[0]
		else:
			result = "No idea"
			


		if len(result) > 880:

			whereToSplit = splitAt(result, 860)
			result = "%s [Cut for length]" % result[0:whereToSplit]

		if len(result) > 440:
			whereToSplit = splitAt(result, 440)
			stringOne = result[0:whereToSplit]
			stringTwo = result[whereToSplit:]

			connection.msg(channel, "%s... " % stringOne)
			connection.msg(channel, "... %s" % stringTwo)
		else:
			connection.msg(channel, "%s" % result)
		return True

