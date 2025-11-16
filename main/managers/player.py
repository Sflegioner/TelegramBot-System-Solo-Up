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
#-------------------------------------------------------------------------#   
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
        self.update_user()
        return str_notification
#-------------------------------------------------------------------------#
    def finish_task_award(self,exp):
        self.player_current_exp += exp 
        if self.player_current_exp>=self.player_exp_to_nvlv:
            self.player_current_exp -= self.player_exp_to_nvlv
            self.player_exp_to_nvlv += 5 
            print(self.player_exp_to_nvlv)
            print(self.player_current_exp)
            return self.lvl_up()
        self.update_user()
        return "Exp earned"
        
#--------------------------[CREATE]--[DELETE]--[UPDATE]--[READ]-------------------------------------#    
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
    
    def update_user(self):
        players_collection = self.mongoDB["Player"]
        update_data = {
                "player_lvl": self.player_lvl,
                "player_current_exp": self.player_current_exp,
                "player_exp_to_nvlv": self.player_exp_to_nvlv,
                "player_status": self.player_status
                }
        players_collection.update_one({"player_id": self.player_id},{"$set": update_data})
        return "Player stats updated"

    
    def login_player(self, id:str)->str:
        players_collection = self.mongoDB["Player"]
        player = players_collection.find_one({"player_id": id})
        
        self.player_id = player["player_id"]
        self.player_name = player["player_name"]
        self.player_lvl = player["player_lvl"]
        self.player_exp_to_nvlv = player["player_exp_to_nvlv"]
        self.player_current_exp = player["player_current_exp"]
        
        print(self.player_lvl)

        message = "Welcome back Player!"
        return 
#-------------------------------------------------------------------------#   

    def verify_if_exist(self,id, name)-> bool:
        players_collection = self.mongoDB["Player"]
        player = players_collection.find_one({"player_id": id})
        if player is None: 
            return False
        else:
            self.login_player(id)
            return True
        

#----------------------------[Leader board]--------------------------------#
    def send_leaderboard(self):
        players_collection = self.mongoDB["Player"]
        top_players = (
            players_collection.find({}, {"_id": 0, "player_name": 1, "player_lvl": 1, "player_current_exp": 1}).sort([("player_lvl", -1), ("player_current_exp", -1)]).limit(10) )
        leaderboard_str = "<b>🏆 Leaderboard 🏆</b>\n\n"
        rank = 1
        for player in top_players:
            leaderboard_str += (
                f"{rank}. <b>{player['player_name']}</b> "
                f"- Lvl: <b>{player['player_lvl']}</b> "
                f"(Exp: {player['player_current_exp']})\n"
            )
            rank += 1

        return leaderboard_str

#----------------------------[Leader board]--------------------------------#