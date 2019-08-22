import sqlite3
from sqlite3 import Error

class DataBase():

    hook = None
    db = 'HelpfulSylph.db'

    def __init__(self):
        self.hook = sqlite3.connect(self.db)
        self.hook.execute(
            '''CREATE TABLE IF NOT EXISTS characterCardsDic
                (   
                ID  INT PRIMARY KEY     NOT NULL,
                CARDID        INTEGER NOT NULL
                );
            '''
        )  
        print("[HLSYL] Database initialized.")
        self.hook.close()

    def addOrUpdateCard(self, userID, cardID):
        self.hook = sqlite3.connect(self.db)
        self.hook.execute("INSERT OR REPLACE INTO characterCardsDic (ID, CARDID) VALUES(?, ?)", (userID, cardID))
        self.hook.commit()
        self.hook.close()

    def getCardByUserID(self, userID):
        self.hook = sqlite3.connect(self.db)
        print(userID)
        req = "SELECT ID, CARDID FROM characterCardsDic WHERE ID = " + str(userID)
        cursor = self.hook.execute(req)
        data = cursor.fetchone()
        self.hook.close()
        return data

dbSingle = DataBase()