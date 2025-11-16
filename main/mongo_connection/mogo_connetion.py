from pymongo import MongoClient
import logging

#Singleton 
class MongoDBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        logging.info("Connecting to MongoDB...")
        self.client = MongoClient("mongodb+srv://stepanmereniuk_db_user:5J8rwrWFO9kTljXh@cluster0.kljtj8w.mongodb.net/?appName=Cluster0")
        self.database = self.client.get_database("SoloLevelingBotDB")
        self.player_col = self.database["Player"]  
        self.player_daily_tasks = self.database["DailyTasks"]
        logging.info("Connected to MongoDB.")

    def get_database(self):
        return self.database