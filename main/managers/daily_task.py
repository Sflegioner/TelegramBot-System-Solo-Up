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
    
    def __init__(self, user_id):
        #user insert
        self.id = 1
        self.user_id = user_id
        self.status = "Not finished yet"
        
        self.time_of_creation = "00-00-00"
        self.time_to_finish = "00-00-00"
        
        self.exp_value = 20
        
        self.mongoDBclient = MongoDBConnection() 
        self.mongoDB = self.mongoDBclient.get_database()
        
    async def inset_descreption(self,description):
        self.description = description
    
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
        message =""
        if daily_task_col.find({"user_id":self.user_id}):
            tasks = daily_task_col.find({"user_id":self.user_id})
            for i in tasks:
                all_task_list.append(i)
            print(all_task_list)
        else:
            print("no task")
            
        for idx, task in enumerate(all_task_list,start=1):
            description = task.get("description", "...")
            #Add
            if task.get("status") == "finished":
                message += f"{idx}) <s>{description}</s>\n"
            else:
                message += f"{idx}) {description}\n"
        return message
    
    def get_task_by_number(self, task_number: int):
        if task_number < 0:
            return None
        daily_task_col = self.mongoDB["DailyTasks"]
        cursor = daily_task_col.find({"user_id": self.user_id}).sort("created_at").skip(task_number).limit(1)
        return next(cursor, None)

    def finish_task(self, task_number: int) -> str:
            task = self.get_task_by_number(task_number)
            if task:
                self.mongoDB["DailyTasks"].update_one(
                    {"_id": task["_id"]},
                    {"$set": {"status": "finished"}}
                )
                return "finished"
            return "task not found"

    def delete_task(self, task_number: int) -> str:
            task = self.get_task_by_number(task_number)
            if task:
                self.mongoDB["DailyTasks"].delete_one({"_id": task["_id"]})
                print("task was deleted")
                return "task was deleted"
            print("no mached task")
            return "task not found"
