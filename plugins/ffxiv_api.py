
import requests
import json


class FFXIV_api:
    #enable debug prints
    DEBUG = True

    apiUrl = "https://ffxiv_api.bbqdroid.org"
    
    serverListEndpoint = "/server_list.php"

    charSearchEndpoint = "/search.php?username=" #Add the player name
    charSearchServerParam = "&server=" #Add the server name (properly capitalized [Gilgamesh])
    charSearchLodestoneParam = "&lodestone"

    
    fetchCharEndpoint = "/fetch.php?userid=" #Add the char/lodestoneID

    @classmethod
    def getServers(cls):
        res = requests.get(cls.apiUrl+cls.serverListEndpoint)
        return res.json()

    @classmethod
    def searchCharacter(cls, name, server=None):
        if cls.DEBUG:
            print("[debug] searchCharacter("+str(name)+", "+str(server)+")")

        #server cleanup
        server = server.lower().capitalize()

        url = cls.apiUrl+cls.charSearchEndpoint

        if not server:
            url += name
        else:
            url += (name + cls.charSearchServerParam + server)

        return cls.requestChar(url, False)

    @classmethod
    def requestChar(cls, url, lodestone):
        if cls.DEBUG:
            print("[debug] requestChar("+str(url)+", "+str(lodestone)+")")

        if lodestone:
            url += cls.charSearchLodestoneParam

        res = requests.get(url)
        data = res.json()
        
        if cls.DEBUG:
            print("[debug] data: ")
            print(data)

        if not data['error']:
            return data['data']

        elif data['error_msg'] == 'No results':
            if lodestone:
                return ["NA"]
            else:
                return cls.requestChar(url, True)

        elif data['error_msg'] == 'Too much results':
                return ["TMR"]

    @classmethod
    def fetchChar(cls, name, server):
        if cls.DEBUG:
            print("[debug] fetchChar("+str(name)+", "+str(server)+")")

        charID = cls.getCharID(name, server)

        url = cls.apiUrl+cls.fetchCharEndpoint+str(charID)

        res = requests(url)
        data = res.json()

        #TODO: implement error checking

        return data

    @classmethod
    def getCharID(cls, name, server):        
        chars = cls.searchCharacter(name, server)
        
        if cls.DEBUG:
            print("[debug] getCharID("+str(name)+", "+str(server)+")")
            print(chars)
            print("ID = "+str(chars[0]['ID']))

        if chars and (not chars[0] == "NA") and (not chars[0] == "TMR"):
            if not len(chars) == 1:
                print("[HLSYL] Fetching character returned multiple characters, sending the first one in the list.")
            
            return chars[0]['ID']
        else:
            return -1

