from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler
from managers.player import Player

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menuOption = [
        [
            InlineKeyboardButton("✅ Yes", callback_data="yes"),
            InlineKeyboardButton("❌ No", callback_data="no")
        ]
    ]
    replyMarkup = InlineKeyboardMarkup(menuOption)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "<b>[System]</b>\n"
            f"Congratulations, Hunter @{update.effective_chat.username}.\n"
            "You have been selected to join the <b>Player</b> program.\n"
            "Do you accept?"
        ),
        reply_markup=replyMarkup,
        parse_mode="HTML"
    )

async def reponce_to_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = update.callback_query
    await answer.answer()  
    if answer.data == "yes":
        await answer.message.reply_text("[System] \n Congratulations on becoming a Player.")
        await send_player_stats(update,context)
    else:
        await answer.message.reply_text("[System] \n YOUR HEART HAS BEEN STOPPED...")

async def send_player_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentPlayer = Player(
        update.callback_query.message.chat.id,
        update.callback_query.message.chat.username,
        1, 0, 0, "Freshie \n [Give motivation for Player, to climb higher ...] \n [{+10 exp per day up to lvl 10}] "
    )
    await context.bot.send_message(chat_id=update.effective_chat.id,text=(currentPlayer.show_all_stats()),parse_mode='HTML')
