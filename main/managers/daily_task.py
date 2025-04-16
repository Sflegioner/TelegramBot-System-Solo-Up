from main.mongo_connection.mogo_connetion import MongoDBConnection
from pymongo import MongoClient, database 

class DailyTask:
    #Annotation 
    id:int
    status:str
    description:str
    time_of_creation: str
    time_to_finish: str 
    exp_value: int
    
    user_id: str
    
    #-------------DB_Variables-----------------#
    mongoDBclient: MongoDBConnection
    mongoDB: database
    #-------------DB_Variables-----------------#
    
    def __init__(self, description, user_id):
        #user insert
        self.description = description
        #user insert
        
        self.id = 1
        self.user_id = user_id
        self.status = "Not finished yet"
        
        self.time_of_creation = "00-00-00"
        self.time_to_finish = "00-00-00"
        
        self.exp_value = 20
        
        self.mongoDBclient = MongoDBConnection() 
        self.mongoDB = self.mongoDBclient.get_database()
        
    
    
    async def save_to_mongoDB(self)->str:
        daily_task_col = self.mongoDB["DailyTasks"]
        daily_task_col.insert_one({
            "user_id":self.user_id,
            "status":self.status,
            "description":self.description,
            "time_of_creation":self.time_of_creation,
            "time_to_finish":self.time_to_finish,
            "exp_value":self.exp_value,
        })
        return "<b>Task created succesfully<b>"
    
    def load_all_tasks(self)->str:
        daily_task_col = self.mongoDB["DailyTasks"]
        all_task_list = []
        if daily_task_col.find({"user_id":self.user_id}):
            tasks = daily_task_col.find({"user_id":self.user_id})
            for i in tasks:
                all_task_list.append(i)
            print(all_task_list)
        else:
            print("no task")
            
        
        pass
    
    def finish_task():
        pass
    
    def reminder():
        pass
        