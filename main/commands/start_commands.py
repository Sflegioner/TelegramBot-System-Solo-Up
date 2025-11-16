from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler
from main.commands.player_commands import send_player_stats
from managers.player import Player


#----------------------------------------------------------------------------------------------------------------------------------------#
async def show_menu_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
        KeyboardOption = [[
            "📁stats", "✉️task", "🏆leaders board$🏆", "⚙️options"
        ]]
        replyMarkup = ReplyKeyboardMarkup(keyboard=KeyboardOption,resize_keyboard=True)
        await update.effective_message.reply_markdown("So what now?",reply_markup=replyMarkup)
        return ConversationHandler.END

#----------------------------------------------------------------------------------------------------------------------------------------#
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """_summary_
        Take all info and save into user_data
    Args:
        update (Update): _description_
        context (ContextTypes.DEFAULT_TYPE): _description_
    """
    user_id = update.effective_chat.id
    username = update.effective_chat.username
    
    player = Player()
    isAunth = player.verify_if_exist(user_id,username)
    if not isAunth:
        menuOption = [[
            InlineKeyboardButton("✅ Yes", callback_data="yes"),
            InlineKeyboardButton("❌ No", callback_data="no")
        ]]
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
        parse_mode="HTML")
    else:
        KeyboardOption = [[
            "📁stats", "✉️task", "🏆leaders board$🏆", "⚙️options"
        ]]
        replyMarkup = ReplyKeyboardMarkup(keyboard=KeyboardOption,resize_keyboard=True)
        await update.message.reply_text("Wellcome back, Player, what about do something to feel much better?",reply_markup=replyMarkup)
#----------------------------------------------------------------------------------------------------------------------------------------#
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📁stats":
        await send_player_stats(update, context)
    elif text == "✉️task":
        return 1
    elif text == "🏆leaders board$🏆":
        await update.message.reply_text("Checking penalties...")
    elif text == "⚙️options":
        await update.message.reply_text("Opening options...")

#----------------------------------------------------------------------------------------------------------------------------------------#

async def reponce_to_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    answer = update.callback_query
    await answer.answer()  
        # Remove inline buttons
    try:
        await answer.message.edit_reply_markup(reply_markup=None)
    except:
        pass

    if answer.data == "yes":
        user_id = update.effective_chat.id
        username = update.effective_chat.username
        player = Player()
        created = player.register_new_player(user_id, username)
        if created:
            await answer.message.reply_text("[System] \n Congratulations on becoming a Player.")
        else:
            await answer.message.reply_text("[System] \n You are already registered.")
        await show_menu_options(update,context)
    else:
        await answer.message.reply_text("[System] \n YOUR HEART HAS BEEN STOPPED...")
        
#----------------------------------------------------------------------------------------------------------------------------------------#
    


    