from .daily_task import DailyTask
class Player:
    """sumary_line
      this class represent user object and his propertyes 
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    player_id:str
    player_name:str
    
    player_lvl:int
    player_exp_to_nvlv:float
    player_current_exp:float
    
    player_status:str
    list_player_tasks:[]
    current_task_count:int
    
    def __init__(self,id, player_name,player_lvl,player_exp_to_nvlv,player_current_exp,player_status):
        self.id = id
        self.player_name = player_name
        
        self.player_lvl = player_lvl
        self.player_exp_to_nvlv = player_exp_to_nvlv
        self.player_current_exp = player_current_exp
        
        self.player_status = player_status
        pass
    
    def show_all_stats(self)->str:
        all_stats_str = (
                        f"[Stats] \n of <b>{self.player_name}</b> \n"
                        f"Current lvl: <b>{self.player_lvl}</b> \n"
                        f"Status of user: <b>{self.player_status}</b> \n"
                        f"Current EXP: <b>{self.player_current_exp}</b>"
                        )
        return all_stats_str
        
    def create_list_of_task(self,user_id,message:str)->any:
        new_task = DailyTask(user_id,message)
        self.list_player_tasks.append(new_task)
        return self.current_task_count + 1