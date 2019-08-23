import sqlite3
from sqlite3 import Error

class DataBase():

    hook = None
    db = 'HelpfulSylph.db'

    def __init__(self):
        self.hook = sqlite3.connect(self.db)
        self.hook.execute(
            '''CREATE TABLE IF NOT EXISTS charaDic
                (   
                ID      INT PRIMARY KEY     NOT NULL,
                CARDID  INTEGER             ,
                DISCID  TEXT
                );
            '''
        )  
        print("[HLSYL] Database initialized.")
        self.hook.close()

    def addOrUpdate(self, userID, cardID, discordID):
        self.hook = sqlite3.connect(self.db)
        self.hook.execute("INSERT OR REPLACE INTO charaDic (ID, CARDID, DISCID) VALUES(?, ?, ?)", (userID, cardID, discordID))
        self.hook.commit()
        self.hook.close()
        
    def addOrUpdateCard(self, userID, cardID):
        self.addOrUpdate(userID, cardID, 0)

    def addOrUpdateDiscord(self, userID, discordID):
        self.addOrUpdate(userID, 0, discordID)

    #returns the cardID if there is one, else returns 0. you need to filter outside of this.
    def getCardByUserID(self, userID):
        self.hook = sqlite3.connect(self.db)
        req = "SELECT CARDID FROM charaDic WHERE ID = " + str(userID)
        cursor = self.hook.execute(req)
        data = cursor.fetchone()
        self.hook.close()
        return data

    #returns the userID for the discordID if the discord ID exists, else returns 0.
    #Don't search for discordID 0, it will return the first (or every) non associated character.
    def getUserIDByDiscordID(self, discordID):
        self.hook.sqlite3.connect(self.db)
        req = "SELECT ID FROM charaDic WHERE DISCID = " + str(discordID)
        cursor = self.hook.execute(req)
        data = cursor.fetchone()
        self.hook.close()
        if data:
            return data
        else:
            return 0


dbSingle = DataBase()