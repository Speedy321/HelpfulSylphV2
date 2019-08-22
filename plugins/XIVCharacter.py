from disco.bot import Plugin
from disco.types.message import MessageEmbed

from . import CharaCard
from .CharaCard import CharaCard

import requests
import json

class XIVCharacter(Plugin):

    #api consts
    apiUrl = "https://ffxiv_api.bbqdroid.org"
    charSearchUrl = "/search.php?username="
    addServerUrl = "&server="
    forcelodestoneUrl = "&lodestone"

    #Temporary until i can get a serverlist from our api.
    serverlistAether = ["Adamantoise", "Cactuar", "Faerie", "Gilgamesh", "Jenova", "Midgardsormr", "Sargatanas", "Siren"]
    serverlistPrimal = ["Behemoth", "Excalibur", "Exodus", "Famfrit", "Hyperion", "Lamia", "Leviathan", "Ultros"]
    serverlistCrystal = ["Balmung", "Brynhildr", "Coeurl", "Diabolos", "Goblin", "Malboro", "Mateus", "Zalera"]
    serverlistElemental = ["Aegis", "Atomos", "Carbuncle", "Garuda", "Gungnir", "Kujata", "Ramuh", "Tonberry", "Typhon", "Unicorn"]
    serverlistGaia = ["Alexander", "Bahamut", "Durandal", "Fenrir", "Ifrit", "Ridill", "Tiamat", "Ultima", "Valefor", "Yojimbo", "Zeromus"]
    serverlistMana = ["Anima", "Asura", "Belias", "Chocobo", "Hades", "Ixion", "Mandragora", "Masamune", "Pandaemonium", "Shinryu", "Titan"]
    serverlistChaos = ["Cerberus", "Louisoix", "Moogle", "Omega", "Ragnarok", "Spriggan"]
    serverlistLight = ["Lich", "Odin", "Phoenix", "Shiva", "Twintania", "Zodiark"]

    serverlistMaster = []

    def getServers(self):

        self.serverlistMaster.extend(self.serverlistAether)
        self.serverlistMaster.extend(self.serverlistPrimal)
        self.serverlistMaster.extend(self.serverlistCrystal)
        self.serverlistMaster.extend(self.serverlistElemental)
        self.serverlistMaster.extend(self.serverlistGaia)
        self.serverlistMaster.extend(self.serverlistMana)
        self.serverlistMaster.extend(self.serverlistChaos)
        self.serverlistMaster.extend(self.serverlistLight)

        serverlistMain = []
        for server in self.serverlistAether:
            serverlistMain.append( server + " (Aether)" )
        for server in self.serverlistPrimal:
            serverlistMain.append( server + " (Primal)" )
        for server in self.serverlistCrystal:
            serverlistMain.append( server + " (Crystal)" )
        for server in self.serverlistElemental:
            serverlistMain.append( server + " (Elemental)" )
        for server in self.serverlistGaia:
            serverlistMain.append( server + " (Gaia)" )
        for server in self.serverlistMana:
            serverlistMain.append( server + " (Mana)" )
        for server in self.serverlistChaos:
            serverlistMain.append( server + " (Chaos)" )
        for server in self.serverlistLight:
            serverlistMain.append( server + " (Light)" )
        
        return serverlistMain
        

    #search for a character in the database, returns the json payload/object
    def searchCharacter(self, server, name):
        url = self.apiUrl + self.charSearchUrl + name + self.addServerUrl + server
        print("url: "+ url)
        response = requests.post(url)

        print(response.json())

    @Plugin.command('search', '<server:str> <name:str...>')
    def command_search(self, event, server, name):

        #string cleanup
        server = server.lower().capitalize()

        serverlist = self.getServers()

        if server in self.serverlistMaster:
            print("[HLSYL] Server "+server+" is in master list.")
            print("[HLSYL] Searching for character "+name+" on server "+server)

            serverInd = self.serverlistMaster.index(server)
            fullServer = serverlist[serverInd]

            self.searchCharacter(fullServer, name)     

    #Temp to test the player cards
    @Plugin.command('show', '<id:int>')
    def command_show(self, event, id):
        card = CharaCard(id)
        event.msg.reply(embed=card.getCardMsg())
