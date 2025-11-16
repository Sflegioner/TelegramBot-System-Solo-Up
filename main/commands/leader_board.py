from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from managers.player import Player

async def show_currently_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player = Player()
    leader_board_text = player.send_leaderboard()
    await update.message.reply_text(leader_board_text)
    return ConversationHandler.END4