from main.mongo_connection.mogo_connetion import MongoDBConnection
from pymongo import MongoClient, database
from pymongo.errors import PyMongoError
import random

class DailyTask:
    # Annotation
    id: int
    status: str
    description: str
    time_of_creation: str
    time_to_finish: str
    exp_value: int

    user_id: int

    # -------------DB_Variables-----------------#
    mongoDBclient: MongoDBConnection
    mongoDB: database
    # -------------DB_Variables-----------------#

    def __init__(self, user_id):
        self.id = 1
        self.user_id = user_id
        self.status = "Not finished yet"

        self.time_of_creation = "00-00-00"
        self.time_to_finish = "00-00-00"

        self.exp_value = random.randrange(10, 25)

        try:
            self.mongoDBclient = MongoDBConnection()
            self.mongoDB = self.mongoDBclient.get_database()
        except PyMongoError as e:
            print(f"Error connecting to MongoDB: {e}")
            self.mongoDB = None  
            
    async def inset_descreption(self,description):
        self.description = description
    

    async def save_to_mongoDB(self) -> str:
        if self.mongoDB is None:
            return "<b>Error: Database connection failed</b>"
        
        try:
            daily_task_col = self.mongoDB["DailyTasks"]
            daily_task_col.insert_one({
                "user_id": self.user_id,
                "status": self.status,
                "description": self.description,
                "time_of_creation": self.time_of_creation,
                "time_to_finish": self.time_to_finish,
                "exp_value": self.exp_value,
            })
            return "<b>Task created successfully</b>"
        except PyMongoError as e:
            print(f"Error saving task: {e}")
            return "<b>Error: Failed to create task</b>"

    def load_all_tasks(self) -> str:
        if self.mongoDB is None:
            return "<b>Error: Database connection failed</b>"
        
        try:
            daily_task_col = self.mongoDB["DailyTasks"]
            all_task_list = list(daily_task_col.find({"user_id": self.user_id}))
            
            if not all_task_list:
                return "<b>You have no tasks</b>"
            
            message = ""
            for idx, task in enumerate(all_task_list, start=1):
                description = task.get("description", "...")
                if task.get("status") == "finished":
                    message += f"{idx}) <s>{description}</s>\n"
                else:
                    message += f"{idx}) {description}\n"
            return message
        except PyMongoError as e:
            print(f"Error loading tasks: {e}")
            return "<b>Error: Failed to load tasks</b>"

    def get_task_by_number(self, task_number: int):
        if self.mongoDB is None:
            return None
        
        if task_number < 0:
            return None
        
        try:
            daily_task_col = self.mongoDB["DailyTasks"]
            cursor = daily_task_col.find({"user_id": self.user_id}).sort("time_of_creation").skip(task_number).limit(1)
            return next(cursor, None)
        except PyMongoError as e:
            print(f"Error getting task: {e}")
            return None

    def finish_task(self, task_number: int) -> str:
        if self.mongoDB is None:
            return "Error: Database connection failed"
        
        try:
            task = self.get_task_by_number(task_number)
            if task:
                self.mongoDB["DailyTasks"].update_one(
                    {"_id": task["_id"]},
                    {"$set": {"status": "finished"}}
                )
                return "finished"
            return "task not found"
        except PyMongoError as e:
            print(f"Error finishing task: {e}")
            return "Error: Failed to finish task"

    def delete_task(self, task_number: int) -> str:
        if self.mongoDB is None:
            return "Error: Database connection failed"
        
        try:
            task = self.get_task_by_number(task_number)
            if task:
                self.mongoDB["DailyTasks"].delete_one({"_id": task["_id"]})
                print("task was deleted")
                return "task was deleted"
            print("no matched task")
            return "task not found"
        except PyMongoError as e:
            print(f"Error deleting task: {e}")
            return "Error: Failed to delete task"