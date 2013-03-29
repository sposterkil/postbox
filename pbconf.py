import re


# Configuration variables, imported into Postbox.py.
NICK = 'King_of_Brohan'
CHANNElS = [['ridersofbrohan', 'irc.freenode.net']]  # Add more channels on more servers by adding a list in the form ['channel', 'server']
MIN_LEN = 2
CANON_REGEX = re.compile('(?:%s.capitalize()|%s)(?:[,:]\s|\s)(?P<x>[^.!]+)\s(?P<verb>is|are)(?P<action>\s<.+>)?\s(?P<y>[^.!]+).{0,3}' % (NICK, NICK))
OPS = []  # Move these into Postbox.py and pickle them!
TRIGGERS = {}  # This one too
