from pymongo import MongoClient

#Singleton 
class MongoDBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.database = self.client.get_database("SoloLevelingBotDB")
        self.player_col = self.database["Player"]  
        self.player_daily_tasks = self.database["DailyTasks"]
        print("DB connected")

    def get_database(self):
        return self.database