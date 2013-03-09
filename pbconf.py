import re


# Configuration variables, imported into Postbox.py.
MIN_LEN = 5
CANON_REGEX = re.compile('(?:Postbox|postbox)(?:[,:]\s|\s)(?P<x>[^.!]+)\s(?P<verb>is|are)(?P<action>\s<.+>)?\s(?P<y>[^.!]+).{0,3}')
OPS = []
TRIGGERS = {}
