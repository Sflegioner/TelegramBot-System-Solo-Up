from telegram.ext import ContextTypes, ConversationHandler
from telegram import ReplyKeyboardMarkup, Update
from main.managers.daily_task import DailyTask
from telegram.constants import ParseMode


async def handle_task_entry(update:Update, context:ContextTypes.DEFAULT_TYPE)->int:
        KeyboardOption = [[
                "finish task","show tasks", "create task ", "delete task "]]
        replyMarkup = ReplyKeyboardMarkup(keyboard=KeyboardOption,resize_keyboard=True)
        await update.message.reply_text("So what you want ?",reply_markup=replyMarkup)
        return 1 # For handling

async def show_menu(update:Update, context:ContextTypes.DEFAULT_TYPE)->int:
        keyboard_main = [["📁stats", "✉️task", "❌penality", "⚙️options"]]
        reply_main = ReplyKeyboardMarkup(keyboard=keyboard_main, resize_keyboard=True)
        await update.message.reply_text("Back to main menu:", reply_markup=reply_main)
        ConversationHandler.END

#Swicher based on STEP
async def handle_task_choise(update:Update, context:ContextTypes.DEFAULT_TYPE)->int:
        user_choise = update.message.text

        if user_choise == "finish task":
                await update.message.reply_text("Write number")
                return 4
        
        elif user_choise == "create task":
                await update.message.reply_text("Send your task: ")
                return 2
        
        elif user_choise == "show tasks":
                await update.message.reply_text("Showing yours tasks...")
                await show_daily_task(update,context)
                #ConversationHandler.END
                await handle_task_entry(update,context)
                return 1

        elif user_choise == "delete task":
                await update.message.reply_text("Write number")
                return 5
        else:
                await update.message.reply_text("Unknown choice.")
                
        return ConversationHandler.END

#if Step_3 callback => this
async def create_daily_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        print("save_task triggered")
        user_id = update.effective_user.id
        task_from_user = update.message.text   
        if task_from_user:
                daily_task = DailyTask(user_id)
                await daily_task.inset_descreption(task_from_user)
                await daily_task.save_to_mongoDB()
                await update.message.reply_text("Task saved successfully!")

        await show_menu(update,context )
        return ConversationHandler.END
    
async def show_daily_task(update: Update, context: ContextTypes.DEFAULT_TYPE)->int:
        user_id = update.effective_user.id
        daily_task=DailyTask(user_id)
        message = daily_task.load_all_tasks()
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)

async def finish_daily_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_message = update.message.text
        try:
                user_number = int(user_message)- 1
                if user_number < 0:
                        await update.message.reply_text("Task number must be 1 or more")
        except ValueError:
                await update.message.reply_text("Please enter the number of task.")
                return 1
        daily_task = DailyTask(user_id)
        result = daily_task.finish_task(user_number)  
        if result == "finished":
                await update.message.reply_text("The task is completed ✅")
        else:
                await update.message.reply_text("Failed to complete task ❌")
        await show_menu(update, context)
        return ConversationHandler.END

async def deleting_daily_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_message = update.message.text
        try:
                user_number = int(user_message)- 1
                if user_number < 0:
                        await update.message.reply_text("Task number must be 1 or more")
        except ValueError:
                await update.message.reply_text("Please enter the number of task.")
                return 1
        daily_task = DailyTask(user_id)
        result = daily_task.delete_task(user_number)
        if result == "task was deleted":
                await update.message.reply_text("The task is deleted ✅")
        else:
                await update.message.reply_text("Someting went wrong ❌")
        await show_menu(update,context)
        return ConversationHandler.END
