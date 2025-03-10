from .daily_task import DailyTask
from main.mongo_connection.mogo_connetion import MongoDBConnection
from pymongo import MongoClient, database

class Player:
    """sumary_line
      this class represent singleton of user object and his propertyes 
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    #Anotation
    player_id:str
    player_name:str
    
    player_lvl:int
    player_exp_to_nvlv:float
    player_current_exp:float
    
    player_status:str
    list_player_tasks:[]
    current_task_count:int
    
    
    #-------------DB_Variables-----------------#
    mongoDBclient: MongoDBConnection
    mongoDB: database
    #-------------DB_Variables-----------------#
    
    def __init__(self):
        self.id = 0
        self.player_name = Player
        
        self.player_lvl = 1
        self.player_exp_to_nvlv = 10
        self.player_current_exp = 0
        
        self.player_status = "Freshie"
        
        self.mongoDBclient = MongoDBConnection()
        self.mongoDB = self.mongoDBclient.get_database()
        pass
    
    def show_all_stats(self)->str:
        all_stats_str = (
                        f"<b> [Stats]</b>\n"
                        f"<b>@{self.player_name}</b> \n"
                        f"Current lvl: <b>{self.player_lvl}</b> \n"
                        f"Status of user: <b>{self.player_status}</b> \n"
                        f"Current EXP: <b>{self.player_current_exp}</b>"
                        )
        return all_stats_str
        
    
    def lvl_up(self)->str:
        str_notification = f"Congratulations, you have raised your level! <b>|{self.player_lvl}|->|{self.player_lvl+1}|</b>"
        self.player_lvl += 1
        return str_notification
    
#-------------------------------------------------------------------------#
    def verify_if_exist(self,id, name)-> bool:
        players_collection = self.mongoDB["Player"]
        player = players_collection.find_one({"player_id": id})
        if player is None: 
            self.register_new_player(id,name)
            return False
        else:
            self.login_player(id)
            return True
    
    def register_new_player(self, id:str, name:str)->str:
        players_collection = self.mongoDB["Player"]
        players_collection.insert_one(
            {
                "player_id":id,
                "player_name":name,
                "player_lvl":self.player_lvl,
                "player_current_exp":self.player_current_exp,
                "player_exp_to_nvlv":self.player_exp_to_nvlv,
                "player_status":self.player_status,
            })
        
        message = "Player was registred"
        return message
    
    def login_player(self, id:str)->str:
        players_collection = self.mongoDB["Player"]
        player = players_collection.find_one({"player_id": id})
        
        self.player_id = player["player_id"]
        self.player_name = player["player_name"]
        self.player_lvl = player["player_lvl"]
        print(self.player_lvl)

        message = "Welcome back Player!"
        return 
#-------------------------------------------------------------------------#   