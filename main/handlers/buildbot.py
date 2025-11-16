from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler,filters
from main.commands.start_commands import start_command, reponce_to_answer,handle_buttons, show_menu_options
from main.commands.player_commands import send_player_stats, comming_soon
from main.commands.leader_board import show_currently_leaderboard
from main.commands.task_commands import handle_task_entry, handle_task_choise, create_daily_task,show_daily_task,finish_daily_task, deleting_daily_task
from main.config import TOKEN
import logging

#STEP_MAIN_MENU = 0
STEP_TASK_CHOICE = 1
STEP_CREATE_TASK = 2
STEP_LIST_TASK = 3
STEP_FINISH_TASK = 4
STEP_DELETE_TASK = 5

def start_build():
    #handler after pressed task
    conv_task_handler = ConversationHandler( 
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^✉️task$"), handle_task_entry)],
        states={ 
                #STEP_MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_menu_options)],
                STEP_TASK_CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_task_choise)],
                STEP_CREATE_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_daily_task)],
                STEP_LIST_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_daily_task)],
                STEP_FINISH_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_daily_task)],
                STEP_DELETE_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, deleting_daily_task)]
                },
        fallbacks=[]                                                     
    )
    stats_handler = MessageHandler(filters.TEXT & filters.Regex("^📁stats$"), send_player_stats)
    leader_board = MessageHandler(filters.TEXT & filters.Regex("^🏆leaders board$🏆"), show_currently_leaderboard)
    option_opt = MessageHandler(filters.TEXT & filters.Regex("^⚙️options$"), comming_soon)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CallbackQueryHandler(reponce_to_answer))
    app.add_handler(CommandHandler('stats',send_player_stats))
    app.add_handler(conv_task_handler)
    app.add_handler(leader_board)
    app.add_handler(option_opt)
    app.add_handler(stats_handler)
    app.run_polling()
    logging.info("Bot started polling...")