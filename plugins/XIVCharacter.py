from disco.bot import Plugin
from disco.types.message import MessageEmbed

from . import CharaCard
from .CharaCard import CharaCard

from . import database
from .database import dbSingle

from .ffxiv_api import FFXIV_api

import requests
import json

class XIVCharacter(Plugin):

    #api consts
    apiUrl = "https://ffxiv_api.bbqdroid.org"
    serverListUrl = "/server_list.php"
    charSearchUrl = "/search.php?username="
    addServerUrl = "&server="
    forcelodestoneUrl = "&lodestone"

    serverList = []

    def load(self, ctx):
        self.serverList = FFXIV_api.getServers()
        super(XIVCharacter, self).load(ctx)

    # "@Bot search joe blo Gilgamesh" => search "joe blo" on Gilgamesh
    # "@Bot search joe Gilgamesh"     => search "joe Gilgamesh" on All
    # "@Bot search joe $Gilgamesh"    => search "joe" on Gilgamesh
    @Plugin.command('search', '<name:str> [surname:str] [server:str]')
    def command_search(self, event, name, surname=None, server=None):
        #check if surname is used as a server
        if (not server) and (surname):
            if surname[0] == '$':
                server = surname[1:]
                surname = None
        
        #add surname if non null
        if surname:
            name = name+" "+surname

        characters = FFXIV_api.searchCharacter(name, server)
        if (not characters[0] == "TMR") and (not characters[0] == "NA"):
            charNum = len(characters)
            msg = "You searched for `" + name + "` " 
            if server:
                msg += "on server `"+ server+"`. "
            else :
                msg += "on all servers. "
            msg +="\n I found `"+str(charNum)+"` result"
            if charNum > 1:
                msg +="s, here are the first few: "
            else: 
                msg += ", here it is:"
            for character in characters:
                if len(msg) < 800:
                    msg +="\n> "+character['Name']+" on "+character['Server']+".\n> <https://na.finalfantasyxiv.com/lodestone/character/"+character['ID']+"/> \n"
        
            event.msg.reply(msg)
        elif characters[0] == "TMR":
            event.msg.reply("I've got too many results for your search. Please tell me the full name and/or the server to help me.\n> use $<Server> if you're not giving `name surname` beforhand.")
        elif characters[0] == "NA":
            event.msg.reply("I've got no result for your search. Please make sure you've written everything the right way.")
        else:
            event.msg.reply("Something went very wrong and I have not recieved anything from my information broker. Please check with my devs to see what went wrong. (check @Bot info for devs)")
            print("[HLSYL] [ERROR] No information AT ALL from API for search: "+name+" "+str(server))

    # "@Bot show joe blo Gilgamesh" => show first result for "joe blo" on Gilgamesh
    @Plugin.command('show', '<name:str> <surname:str> <server:str>')
    def command_show(self, event, name, surname, server):
        #server cleanup
        server = server.lower().capitalize()

        #check if server is valid
        if server in self.serverList:
            card = CharaCard(FFXIV_api.getCharID((name+" "+surname), server))
            event.msg.reply(embed=card.getCardMsg())
        else:
            event.msg.reply("You need to provide a valid Server. \n> @Bot show <name> <surname> <Server>")

    # "@Bot iam joe blo Gilgamesh" => links you with the first result for "joe blo" on Gilgamesh
    @Plugin.command('iam', '<name:str> <surname:str> <server:str>')
    def command_iam(self, event, name, surname, server):
        dbSingle.addOrUpdateDiscord(FFXIV_api.getCharID((name+" "+surname), server), event.author.mention)
        event.msg.reply(event.author.mention + " you are " + str(name+" "+surname) + " [TEMP: need to get the char name from the api once it's fixed...]")
