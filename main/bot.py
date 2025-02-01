import telegram
from telegram import Update,Bot, MenuButton
from telegram.ext import Application, ApplicationBuilder,CommandHandler, CallbackQueryHandler
from config import TOKEN
from commands import start_command,reponce_to_answer

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CallbackQueryHandler(reponce_to_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
