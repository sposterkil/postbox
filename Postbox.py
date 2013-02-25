import sys
# import re
from ircutils import bot


class IRCBot(bot.SimpleBot):
    global min_len
    min_len = 5
    print("Starting...")

    def on_channel_message(self, event):
        message = event.message.split()
        print(message[0].upper)
        if message[0].upper == "EXITNOW":
            print("Recived Exit Order")
            if event.source.upper() == "PISKETCH" or event.source.upper() == "PAOANI":
                sys.exit()
        elif len(message[0].upper()) > min_len:
            print("Message length over min_len: " + event.message + ' (From ' + event.source + ')')
            self.send_message(event.target, event.message)

    def on_private_message(self, event):
        print("Echoing private message from " + event.source + ": " + event.message)
        self.send_message(event.source, event.message)

    def on_join(self, event):
        if event.source == self.nickname:
            print("Joined channel.")
            self.send_message("NickServ", "identify bukkpass101")
        else:
            self.send_message(event.target, "Hello, " + event.source + ".")

    def parse(message):
        # We'll handle checking for assignment/triggers in here
        # http://www.debuggex.com/?re=%28%3F%3APostbox%7Cpostbox%29%28%3F%3A%5B%2C%3A%5D%5Cs%7C%5Cs%29%28%5Cw%2B%29%5Cs%28is%7Care%7C%3C.%2B%3E%29%5Cs%28%5Cw%2B%7C%5Cd%2B%29.&str=Postbox%3A+eggplants+%3Creply%3E+eggs.
        if message.match('(?:Postbox|postbox)(?:[,:]\s|\s)(\w+)\s(is|are|<.+>)\s(\w+|\d+).'):
            print("Matched a command!")
        else:
            print("Not a command.")
        return message

if __name__ == "__main__":
    echo = IRCBot("Postbox")  # Name it
    echo.connect("irc.freenode.net", channel=["#testbox"])  # connect
    echo.start()  # start
