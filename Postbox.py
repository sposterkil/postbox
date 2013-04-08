import sys
import re
import cPickle as pickle
from ircutils import bot


class Postbox(bot.SimpleBot):

    def __init__(self):
        print 'Initializing...'

        # CONFIG VARIABLES
        NICK = 'Postbox'
        # Add more channels on more servers by adding a list in the form [['channel1', 'channel2'], 'server']
        self.CHANNElS = [[['ridersofbrohan'], 'irc.freenode.net']]
        self.MIN_LEN = 2
        self.CANON_REGEX = re.compile('(?:%s.capitalize()|%s)(?:[,:]\s|\s)(?P<x>[^.!]+)\s(?P<verb>is|are)(?P<action>\s<.+>)?\s(?P<y>[^.!]+).{0,3}' % (NICK, NICK))
        self.TRIGGERS = {}
        self.OPS = []
        bot.SimpleBot.__init__(self, NICK)

        print 'Attempting to load pickled triggers...'
        try:
            self.TRIGGERS = pickle.load(open('TRIGGERS', 'rb'))
        except IOError, e:
            print 'IOError Exception, using empty Triggers DB'
            print e
            self.TRIGGERS = {}
        else:
            print 'Triggers DB loaded.'

    def on_channel_message(self, event):
        message = event.message.split()
        if 'EXITNOW' in message:
            print 'Recived Exit Order'
            sys.exit()
        elif len(message[0]) > self.MIN_LEN:
            print 'Message over MIN_LEN, sending to parser: "%s" (from %s)' % (event.message, event.source)
            self.start_parse(event)

    def on_private_message(self, event):
        print('Echoing private message from %s: %s') % (event.source, event.message)
        self.send_message(event.source, event.message)

    def on_who_reply(self, event):
        print 'Recieved WHORPL!'
        print event.user_list
        for user in event.user_list:
            print user

    def on_name_reply(self, event):
        for name in event.name_list:
            print name
            if name[0] is '@' and name not in self.OPS:
                self.OPS.append(name)

    def on_join(self, event):
        self.execute('WHO', event.target)
        self.execute('NAMES', event.target)
        if event.source == self.nickname:
            print('Joined channel.')
            self.send_message('NickServ', 'identify bukkpass101')
        else:
            self.send_message(event.target, 'Hello, %s.' % (event.source))

    def parse_assignment(self, event, elements):
        # print 'parse_assignment called'
        print elements['action']
        print type(elements['action'])
        self.TRIGGERS.update({elements['x'].upper(): '%s %s %s.' % (elements['x'], elements['verb'] + elements['action'],
                elements['y'])})
        pickle.dump(self.TRIGGERS, open('triggers', 'wb'))
        self.send_message(event.target, 'Okay %s, %s %s %s.' % (event.source, elements['x'],
                elements['verb'] + elements['action'], elements['y']))
        print self.TRIGGERS.viewitems()

    def parse_trigger(self, event):
        # print 'parse_trigger called on %s' % (event.message.upper())
        if event.message.upper() in self.TRIGGERS:
            print self.TRIGGERS[event.message.upper()]
            self.send_message(event.target, self.TRIGGERS[event.message.upper()])

    def start_parse(self, event):
        # We'll handle initial parsing in here.
        # If the message looks like an assignment, pass it to an appropriate method
        # If it looks like it could trigger something, likewise
        # regex at http://cl.ly/3W2W0J2j0P3o for analysis
        if re.match(self.CANON_REGEX, event.message) is not None:
            self.parse_assignment(event, re.match(self.CANON_REGEX, event.message).groupdict(""))
        else:
            # If start_parse was called at all, we should check if it's a trigger
            self.parse_trigger(event)


if __name__ == '__main__':
    bot = Postbox()
    bot.connect('irc.freenode.net', channel=['#ridersofbrohan'])  # TODO: Unhardcode
    # for pair in bot.CHANNELS:
        # bot.connect(pair[1], pair[0])
    print 'Starting...'
    bot.start()
