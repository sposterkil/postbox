import sys
import re
from ircutils import bot, events, client
from postconfig import *


class IRCBot(bot.SimpleBot):
    print 'Starting...'
    print 'MIN_LEN = %d' % (MIN_LEN)
    print 'CANON_REGEX = %s' % (str(CANON_REGEX))

    def on_channel_message(self, event):
        message = event.message.split()
        if message[0].upper == 'EXITNOW':
            print 'Recived Exit Order'
            if event.source.upper() == 'PISKETCH' or event.source.upper() == 'PAOANI':
                sys.exit()
        elif len(message[0].upper()) > MIN_LEN:
            print 'Message over MIN_LEN, sending to parser: "%s" (from %s)' % (event.message, event.source)
            self.start_parse(event)
            # self.send_message(event.target, event.message)

    def on_private_message(self, event):
        print('Echoing private message from %s: %s') % (event.source, event.message)
        self.send_message(event.source, event.message)

    def update_ops(self, event):
        print "running NAMES"
        self.execute('NAMES', '#postroom')

    def on_name_reply(self, event):
        for name in event.name_list:
            if name[0] == '@' and OPS.count(name) == 0:
                OPS.append(name)

    def on_join(self, event):
        self.update_ops(event)
        print OPS
        print type(event.source)
        if event.source == self.nickname:
            print('Joined channel.')
            self.send_message('NickServ', 'identify bukkpass101')
        else:
            self.send_message(event.target, 'Hello, %s.' % (event.source))

    def parse_assignment(self, event, elements):
        print 'parse_assignment called'
        # regex at http://cl.ly/16152X1l292c for analysis
        TRIGGERS.update({elements['x']: '%s %s %s.' % (elements['x'], elements['verb'] + elements['action'],
                elements['y'])})
        self.send_message(event.target, 'Okay %s, %s %s %s.' % (event.source, elements['x'],
                elements['verb'] + elements['action'], elements['y']))
        print TRIGGERS.viewitems()

    def parse_trigger(self, event):
        print 'parse_trigger called'
        if event.message in TRIGGERS:
            self.send_message(TRIGGERS)

    def start_parse(self, event):
        # We'll handle checking for assignment/triggers in here.
        # If the message looks like an assignment, pass it to an appropriate method
        # If it looks like it could trigger something, likewise
        if re.match(CANON_REGEX, event.message) is not None:
            self.parse_assignment(event, re.match(CANON_REGEX, event.message).groupdict(""))
        else:
            # If start_parse was called at all, we should check if it's a trigger
            self.parse_trigger(event, event.message)


if __name__ == '__main__':
    echo = IRCBot('Postbox')  # Name it
    echo.connect('irc.rizon.net', channel=['#postroom', '#postroomctrl'])  # connect
    echo.start()  # start


class NameReplyListener(ReplyListener):

    class NameReplyEvent(Event):
        def __init__(self):
            self.channel = None
            self.name_list = []

    def __init__(self):
        ReplyListener.__init__(self)
        self._name_lists = collections.defaultdict(self.NameReplyEvent)

    def notify(self, client, event):
        if event.command == "RPL_NAMREPLY":
            # "( "=" / "*" / "@" ) <channel>
            # :[ "@" / "+" ] <nick> *( " " [ "@" / "+" ] <nick> )

            # - "@" is used for secret channels, "*" for private
            # channels, and "=" for others (public channels).
            channel = event.params[1].lower()
            names = event.params[2].strip().split(" ")
            # TODO: This line below is wrong. It doesn't use name symbols.
            # names = map(protocol.strip_name_symbol, names)
            self._name_lists[channel].name_list.extend(names)
        elif event.command == "RPL_ENDOFNAMES":
            # <channel> :End of NAMES list
            channel_name = event.params[0]
            name_event = self._name_lists[channel_name]
            name_event.channel = channel_name
            self.activate_handlers(client, name_event)
            del self._name_lists[channel_name]
