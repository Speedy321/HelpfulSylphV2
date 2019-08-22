#Start with 
# >py -m disco.cli --token [Your discord bot token] --config config.json

from disco.bot import Plugin

class HelpfulSylph(Plugin):
    
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')