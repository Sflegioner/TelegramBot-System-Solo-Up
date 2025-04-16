from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update
from main.managers import DailyTask

TASK = 1

async def create_daily_task(update:Update, context:ContextTypes.DEFAULT_TYPE)->int:
    """Need only to start conversation"""
    print("create_daily_task triggered") 
    await update.effective_chat.send_message(text="Send your task")
    print(f"Setting conversation state to {TASK}")
    return TASK 

async def save_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("save_task triggered")
    user_id = update.effective_user.id
    task_from_user = update.message.text   
    if task_from_user:
        daily_task = DailyTask(task_from_user, user_id)
        await daily_task.save_to_mongoDB()
        await update.message.reply_text("Task saved successfully!")
    return ConversationHandler.END
    
async def daily_task_by_system()->None:
    print("all_task")
    
    
    pass

      
async def show_all_task_by_user(update:Update, context:ContextTypes.DEFAULT_TYPE)->None:
    print("all_task")
    user_id = update.effective_user.id
    tasks = DailyTask("start_command",user_id)
    tasks.load_all_tasks()
    
    
    pass
    
async def notify_daily_task()->None:
    pass
    
    