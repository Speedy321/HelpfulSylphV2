###
#   Character cards
###

from . import database
from .database import dbSingle 

from disco.types.message import MessageEmbed, MessageEmbedImage

import requests
import json
import re

class CharaCard:
    fetchApiUrl = "https://ffxiv_api.bbqdroid.org/fetch.php?userid="
    cardGeneratorApiCardUrl = "https://www.ffxivprofilegenerator.com/get/"
    cardGeneratorApiUrl = "https://www.ffxivprofilegenerator.com/get/0/"
    cardGeneratorApiEndUrl = "/1/0/en/none/0/0"

    embedMsg = MessageEmbed()

    charID = 0
    cardID = 0
    jsonData = ""

    def __init__(self, charID):
        self.charID = charID
        #url = self.fecthApiUrl+charID
        #self.jsonData = requests.post(url).json()
        #print(self.jsonData)

    def getCardMsg(self):
        data = dbSingle.getCardByUserID(self.charID)
        if data :
            print(data)
                if len(data) < 2:
                    self.fetchCardFromGenerator()
                else:
                    self.cardID = data[1]
        else:
            print("Empty data")
            self.fetchCardFromGenerator()

        if self.cardID > 0:
            self.embedMsg.image = MessageEmbedImage(url = self.cardGeneratorApiCardUrl + str(self.cardID))

        return self.embedMsg

    def fetchCardFromGenerator(self):
        print("generate "+str(self.charID))
        url = self.cardGeneratorApiUrl + str(self.charID) + self.cardGeneratorApiEndUrl
        response = requests.get(url)
        match = re.search("(?:https:\/\/www\.ffxivprofilegenerator\.com\/get\/)(\d{1,10})", response.text)
        self.cardID = int(match.group(1))
        dbSingle.addOrUpdateCard(self.charID, self.cardID)

        

        