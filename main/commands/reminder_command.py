from telegram import Update
from telegram.ext import ContextTypes, JobQueue
from datetime import datetime

jobQ = JobQueue()

async def set_time_for_reminder(context: ContextTypes.DEFAULT_TYPE,time_to_remind:float):
    context.job_queue.run_repeating(reminde_task, time_to_remind,chat_id=context._chat_id)


async def reminde_task(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context._chat_id, text="You need to finish yours tasks")