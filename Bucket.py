import sys
# import re
from ircutils import bot


class EchoBot(bot.SimpleBot):
    global min_len
    min_len = 5
    print("Starting...")

    def on_channel_message(self, event):
        message = event.message.split()
        print(message)
        if message[0].upper == "EXITNOW":
            print("Recived Exit Order")
            if event.source.upper() == "PISKETCH" or event.source.upper() == "PAOANI":
                sys.exit()
        elif len(message[0].upper()) > min_len:
            print("Message length over min_len: " + event.message)
            self.send_message(event.target, self.parse(event.message))

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
        if message.match("[(postbox|Postbox)\\W\\s+.+(is)\\s+.+]"):
            print("Matched a command!")
        else:
            print("Not a command.")
        return message

if __name__ == "__main__":
    echo = EchoBot("Postbox")  # Name it
    # echo.connect("irc.freenode.net", channel=["#testbed213"])  # connect
    echo.connect("irc.rizon.net", channel=["#postroom"])  # connect
    echo.start()  # start
