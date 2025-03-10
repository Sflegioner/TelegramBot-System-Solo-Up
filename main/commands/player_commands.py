
from telegram import Update
from telegram.ext import ContextTypes
from ..managers import Player

#----------------------------------------------------------------------------------------------------------------------------------------#    

async def send_player_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    player = Player()
    player.login_player(user_id)
    message = player.show_all_stats()
    await context.bot.send_message(chat_id=update.effective_chat.id,text=(message),parse_mode='HTML')
    
#----------------------------------------------------------------------------------------------------------------------------------------#    
    
#----------------------------------------------------------------------------------------------------------------------------------------#    

#----------------------------------------------------------------------------------------------------------------------------------------#    
