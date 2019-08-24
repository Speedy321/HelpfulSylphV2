from disco.bot import Plugin
from disco.types.message import MessageEmbed

from . import CharaCard
from .CharaCard import CharaCard

from . import database
from .database import dbSingle

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

    def getServers(self):
        if not self.serverList:
            resp = requests.get(self.apiUrl+self.serverListUrl)
            self.serverList = json.loads(resp.json())

    #search for a character in the database, returns the json payload/object
    def searchCharacter(self, server, name):
        url = self.apiUrl + self.charSearchUrl + name + self.addServerUrl + server
        print("url: "+ url)
        response = requests.get(url)

        print(response.json())

    @Plugin.command('search', '<server:str> <name:str...>')
    def command_search(self, event, server, name):

        #string cleanup
        server = server.lower().capitalize()
        self.getServers()

        if server in self.serverList:
            print("[HLSYL] Server "+server+" is in master list.")
            print("[HLSYL] Searching for character "+name+" on server "+server)

            self.searchCharacter(server, name)

    @Plugin.command('show', '<id:int>')
    def command_show(self, event, id):
        card = CharaCard(id)
        event.msg.reply(embed=card.getCardMsg())

    @Plugin.command('iam', '<server:str> <name:str...>')
    def command_iam(self, event, server, name):
        # TODO: make work when api is fixed.
        charID = 16452510
        # self.searchCharacter(server, name)

        dbSingle.addOrUpdateDiscord(charID, event.author.mention)
        event.msg.reply(event.author.mention + " you are " + str(charID) + " [TEMP: need to get the char name from the api once it's fixed...]")
