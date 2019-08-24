###
#   Character cards
###

from . import database
from .database import dbSingle 
from .ffxiv_api import FFXIV_api

from disco.types.message import MessageEmbed, MessageEmbedImage

import requests
import json
import re

class CharaCard:
    #enable debug prints
    DEBUG = True

    cardGeneratorApiCardUrl = "https://www.ffxivprofilegenerator.com/get/"
    cardGeneratorApiUrl = "https://www.ffxivprofilegenerator.com/get/0/"
    cardGeneratorApiEndUrl = "/1/0/en/none/0/0"

    charID = 0
    cardID = 0
    jsonData = ""

    def __init__(self, charID):
        self.charID = int(charID)
        #url = self.fecthApiUrl+charID
        #self.jsonData = requests.post(url).json()
        #print(self.jsonData)

    def getCardMsg(self):

        if self.DEBUG:
            print("[debug]CharaCard.getCardMsg()")

        if self.charID > 0:
            data = dbSingle.getCardByUserID(self.charID)
            if data :
            
                if self.DEBUG:
                    print("[debug]CharaCard.getCardMsg() data:")
                    print(data)
                    print("[debug]CharaCard.getCardMsg() data len:"+str(len(data)))
                    
                self.cardID = data[0]
            else:

                if self.DEBUG:
                    print("[debug]CharaCard.getCardMsg() Empty data")

                self.fetchCardFromGenerator()

            charData = FFXIV_api.fetchCharByID(self.charID)
            msg = "\n"+\
                " "+charData['Name']+" from "+charData['Server']+".\n"+\
                " Last seen as a level "+str(charData['ActiveClassJob']['Level'])+" "
            if charData['ActiveClassJob']['Level'] > 30:
                msg += charData['ActiveClassJob']['JobName']+". "
            else:
                msg += charData['ActiveClassJob']['ClassName']+". "
            msg += "\n <https://na.finalfantasyxiv.com/lodestone/character/"+str(self.charID)+"/>"

            msgEmb = MessageEmbed()
            msgEmb.image = MessageEmbedImage(url=(self.cardGeneratorApiCardUrl + str(self.cardID)))
            msgEmb.description = msg
            msgEmb.color = self.charID

        return msgEmb

    def fetchCardFromGenerator(self):
        
        if self.DEBUG:
            print("[debug]CharaCard.fetchCardFromGenerator() ID = "+str(self.charID))
        
        if self.charID > 0:
            url = self.cardGeneratorApiUrl + str(self.charID) + self.cardGeneratorApiEndUrl
            response = requests.get(url)
            match = re.search("(?:https:\/\/www\.ffxivprofilegenerator\.com\/get\/)(\d{1,10})", response.text)
            self.cardID = int(match.group(1))
            dbSingle.addOrUpdateCard(self.charID, self.cardID)

        

        