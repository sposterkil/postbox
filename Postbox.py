import sys
import re
from ircutils import bot  # , events, client
from pbconf import *


class IRCBot(bot.SimpleBot):

    print 'Starting...'
    print 'MIN_LEN = %d' % (MIN_LEN)
    print 'CANON_REGEX = %s' % (str(CANON_REGEX))

    def on_channel_message(self, event):
        message = event.message.split()
        if message[0].upper() is 'EXITNOW':
            print 'Recived Exit Order'
            if event.source.upper() is 'SPOST' or event.source.upper() is 'PAOANI':  # Replace with ops check
                sys.exit()
        elif len(message[0]) > MIN_LEN:
            print 'Message over MIN_LEN, sending to parser: "%s" (from %s)' % (event.message, event.source)
            self.start_parse(event)
            # self.send_message(event.target, event.message)

    def on_private_message(self, event):
        print('Echoing private message from %s: %s') % (event.source, event.message)
        self.send_message(event.source, event.message)

    def update_ops(self, event):
        print "running NAMES"
        self.execute('NAMES', '#ridersofbrohan')  # Remove hardcoded reference
        print OPS

    def on_name_reply(self, event):
        for name in event.name_list:
            print name
            if name[0] is '@' and name not in OPS:
                OPS.append(name)

    def on_join(self, event):
        # self.update_ops(event)
        # print OPS
        # print type(event.source)
        if event.source == self.nickname:
            print('Joined channel.')
            self.send_message('NickServ', 'identify bukkpass101')
        else:
            self.send_message(event.target, 'Hello, %s.' % (event.source))

    def parse_assignment(self, event, elements):
        print 'parse_assignment called'
        # regex at http://cl.ly/16152X1l292c for analysis
        TRIGGERS.update({elements['x'].upper(): '%s %s %s.' % (elements['x'], elements['verb'] + elements['action'],
                elements['y'])})
        self.send_message(event.target, 'Okay %s, %s %s %s.' % (event.source, elements['x'],
                elements['verb'] + elements['action'], elements['y']))
        print TRIGGERS.viewitems()

    def parse_trigger(self, event):
        print 'parse_trigger called on %s' % (event.message.upper())
        if event.message.upper() in TRIGGERS:
            print TRIGGERS[event.message.upper()]
            self.send_message(event.target, TRIGGERS[event.message.upper()])

    def start_parse(self, event):
        # We'll handle checking for assignment/triggers in here.
        # If the message looks like an assignment, pass it to an appropriate method
        # If it looks like it could trigger something, likewise
        if re.match(CANON_REGEX, event.message) is not None:
            self.parse_assignment(event, re.match(CANON_REGEX, event.message).groupdict(""))
        else:
            # If start_parse was called at all, we should check if it's a trigger
            self.parse_trigger(event)


if __name__ == '__main__':
    echo = IRCBot(NICK)  # Name it
    echo.connect('irc.freenode.net', channel=['#ridersofbrohan'])  # connect
    print 'About to start!'
    echo.start()  # start
    print 'Started!'
