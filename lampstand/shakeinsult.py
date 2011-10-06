# 
# This is an adaptation of Nick Hodges' Shakspearean Insult Generator in python.
# In it's current form, it is useful as an external method for Zope sites
# The function below is also useful as python CGI.  Call the function in your
# CGI, and it will return the phrase.  Add HTML and stir briskly.
# 
# To use as an external method with zope, place shakeinsult.py in your
# $ZOPEHOMEDIR/Extensions directory.  Then, add an external method in the
# ZODB.  Call the function in dtml: <dtml-var name="shakeinsult">. That's it!
#
# Originally appearing at:
#   http://community.borland.com/article/0,1410,26178,00.html
# See the Delphi code in action at Nick's page:
#   http://www.nickhodges.com/bin/nick.exe/goofy
# Get Zope at:
#   http://www.zope.org/
# Get this at:
#   http://www.zope.org/Members/tfarrell/shakeinsult
#
# This is available under a BSD style license.  Once I said I would never
# write any non-GPL stuff for fun.  Oh well.  Just let me know if you use it.

from random import choice

def shakeinsult(self):
  vowels = ['a', 'e', 'i', 'o', 'u']
  isvowel = 0

  adj1 = ['artless', 'bawdy', 'beslubbering', 'bootless', 'churlish', 'cockered', 'clouted', 'craven', 'currish', 'dankish', 'dissembling', 'droning', 'errant', 'fawning', 'fobbing', 'froward', 'frothy', 'gleeking', 'goatish', 'gorbellied', 'impertinent', 'infectious', 'jarring', 'loggerheaded', 'lumpish', 'mammering', 'mangled', 'mewling', 'paunchy', 'pribbling', 'puking', 'puny', 'qualling', 'rank', 'reeky', 'roguish', 'ruttish', 'saucy', 'spleeny', 'spongy', 'surly', 'tottering', 'unmuzzled', 'vain', 'venomed', 'villainous', 'warped', 'wayward', 'weedy', 'yeasty', 'vomiting', 'vulturous', 'contemptuous', 'groping', 'miniscule', 'quivering', 'shivering', 'trembling', 'miserable', 'licentious', 'cowering', 'sulking', 'gloating', 'murmuring', 'audacious', 'befouling', 'insolent', 'murky', 'pitiable', 'wretched', 'dolorous', 'lamentable', 'inadequate', 'contemptible', 'paltry', 'measly', 'meager', 'paltry', 'inadequate', 'insignificant', 'empty', 'inferior', 'pathetic', 'atrocious', 'execrable', 'damnable', 'repugnant', 'repulsive', 'revolting', 'repellent', 'offensive', 'disgusting', 'horrid', 'horrible', 'obscene', 'beastly', 'vile', 'abominable', 'pitiful', 'wrangled', 'whoring']
  adj2 = ['base-court', 'bat-fowling', 'beef-witted', 'beetle-headed', 'boil-brained', 'clapper-clawed','clay-brained', 'common-kissing', 'crook-pated', 'dismal-dreaming', 'dizzy-eyed', 'doghearted', 'dread-bolted', 'earth-vexing', 'elf-skinned', 'fat-kidneyed', 'fen-sucked', 'flap-mouthed', 'fly-bitten', 'folly-fallen', 'fool-born', 'full-gorged', 'guts-griping', 'half-faced', 'hasty-witted', 'hedge-born', 'hell-hated', 'idle-headed', 'ill-breeding', 'ill-nurtured', 'knotty-pated', 'milk-livered', 'motley-minded', 'onion-eyed', 'plume-plucked', 'pottle-deep', 'pox-marked', 'reeling-ripe', 'rough-hewn', 'rude-growing', 'rump-fed', 'shard-borne', 'sheep-biting', 'spur-galled', 'swag-bellied', 'tardy-gaited', 'tickle-brained', 'toad-spotted', 'unchin-snouted', 'weather-bitten', 'weather-beaten', 'mutton-eating', 'coffee-nosed', 'malodorous']
  noun = ['apple-john', 'baggage', 'barnacle', 'bladder', 'boar-pig', 'bugbear', 'bum-bailey', 'canker-blossom', 'clack-dish', 'clotpole', 'coxcomb', 'codpiece', 'death-token', 'dewberry', 'flap-dragon', 'flax-wench', 'flirt-gill', 'foot-licker', 'fustilarian', 'giglet', 'gudgeon', 'haggard', 'harpy', 'hedge-pig', 'horn-beast', 'hugger-mugger', 'joithead', 'lewdster', 'lout', 'maggot-pie', 'malt-worm', 'mammet', 'measle', 'minnow', 'miscreant', 'moldwarp', 'mumble-news', 'nut-hook', 'pigeon-egg', 'pignut', 'puttock', 'pumpion', 'ratsbane', 'scut', 'skainsmate', 'strumpet', 'varlet', 'vassal', 'whey-face', 'wagtail', 'phlegm-barrel', 'numb-skull', 'lip-infection', 'blood-clot', 'boar-tick', 'pervert', 'catbus']
  prefixA = ['Thou art a','Thou shalt always be a', 'Thou']
  prefixAn = ['Thou art an', 'Thou shalt always be an', 'Thou']
  
  rnoun = choice(noun)
  radj1 = choice(adj1)
  radj2 = choice(adj2)

  for letter in vowels:
    if (radj1[0] == letter):
      rprefix = choice(prefixAn)
      isvowel = 1
  if (isvowel == 0):
    rprefix = choice(prefixA)
  insult = "%s %s %s %s!" % (rprefix, radj1, radj2, rnoun)
  return insult
