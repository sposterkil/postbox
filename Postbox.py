import sys
import re
from ircutils import bot


class IRCBot(bot.SimpleBot):
    print('Starting...')
    MIN_LEN = 5
    CANON_REGEX = '(?:Postbox|postbox)(?:[,:]\s|\s)(?P<x>[^.!]+)\s(?P<verb>is|are)\s(?P<action><.+>)?\s([?{<y>^.!]+).{0,3}'

    def on_channel_message(self, event):
        message = event.message.split()
        if message[0].upper == 'EXITNOW':
            print('Recived Exit Order')
            if event.source.upper() == 'PISKETCH' or event.source.upper() == 'PAOANI':
                sys.exit()
        elif len(message[0].upper()) > MIN_LEN:
            print('Message over MIN_LEN, sending to parser: %s (from %s') % (event.message, event.source)
            start_parse(self, event)
            self.send_message(event.target, event.message)

    def on_private_message(self, event):
        print('Echoing private message from %s: %s') % (event.source, event.message)
        self.send_message(event.source, event.message)

    def get_ops(self, event):
        print "getops executing"
        self.execute('NAMES', '#postroom')
        if event.command == 'RPL_NAMREPLY':
            print re.findall(r'\b@\w+', event.message)

    def on_join(self, event):
        self.execute("PRIVMSG", 'PISKETCH', trailing='execute works!')
        self.get_ops()
        if event.source == self.nickname:
            print('Joined channel.')
            self.send_message('NickServ', 'identify bukkpass101')
        else:
            self.send_message(event.target, 'Hello, %s.') % (event.source)

    def parse_assignment(self, event):
        print 'parse_assignment '
        # regex at http://cl.ly/26112w0z0142 for analysis
        elements = re.match(CANON_REGEX, event.message).groupdict
        x = elements.get('x')
        verb = elements.get('verb') + ' ' + elements.get('action')
        y = elements.get('y')
        self.send_message(event.target, 'Okay %s, %s %s %s.') % (event.source, x, verb, y)

    def parse_trigger(self, event):
        # tbd
        print 'parse_trigger called'

    def start_parse(self, event):
        # We'll handle checking for assignment/triggers in here.
        # If the message looks like an assignment, pass it to an appropriate method
        # If it looks like it could trigger something, likewise
        # http://cl.ly/1R301X0c2E1Q
        if re.match(CANON_REGEX, event.message):
            parse_assignment(self, event)
        else:
            # If parse_addressed was called, we should check if it's a trigger
            parse_trigger(self, event)
        return event.message


if __name__ == '__main__':
    echo = IRCBot('Postbox')  # Name it
    echo.connect('irc.rizon.net', channel=['#postroom', '#postroomctrl'])  # connect
    echo.start()  # start
