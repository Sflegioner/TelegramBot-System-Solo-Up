from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ConversationHandler, MessageHandler,filters
from main.commands.start_commands import start_command, reponce_to_answer,handle_buttons
from main.commands.daily_task_command import create_daily_task,save_task, TASK
from main.commands.player_commands import send_player_stats
from main.config import TOKEN

def start_build():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CallbackQueryHandler(reponce_to_answer))
    app.add_handler(CommandHandler('stats',send_player_stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons),group=1)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("ct", create_daily_task)], 
        states={TASK: [MessageHandler(filters.ALL, save_task)]},
        fallbacks=[],
    )
    app.add_handler(conv_handler)
    #app.add_handler(ConversationHandler(entry_points=[CommandHandler("Create")] ))
    app.run_polling()