# telegram related stuff
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

from .levenshtein import calc_distance

class Bot:
    COMMANDS = ["/start", "/help", "/today", "/next", "/events"]
    
    START_MESSAGE = """
Bonjour, je suis le bot personnel de la Sprint !
Je vous tiendrais au courant des cours et des évenements de la journée.

Pour en savoir plus: /help.
    """
    
    HELP_MESSAGE = """
Les commandes suivantes sont disponibles:

/start -> Message de bienvenue
/help -> Affiche l'aide
/today -> Indique les cours d'aujourdhui
/next -> Indique le prochain cours
/events -> Indique les événements à venir
    """

    def __init__(self, token, calendar):
        self.token = token
        self.calendar = calendar

    # commands
    async def start(self, update: Update, context: CallbackContext) -> None:
        """Function called at each /start command"""
        await update.message.reply_text(Bot.START_MESSAGE)
    
    async def help_cmd(self, update: Update, context: CallbackContext) -> None:
        """Helper function"""
        await update.message.reply_text(Bot.HELP_MESSAGE)
    
    async def today(self, update: Update, context: CallbackContext) -> None:
        """Get today classes from calendar"""
        events = self.calendar.get_today_events()

        if not events:
            text = "Pas de cours aujourd'hui"
        else:
            text = "Les cours sont :\n\n" + "\n".join(map(str, events))
        await update.message.reply_text(text)
    
    async def next_cmd(self, update: Update, context: CallbackContext) -> None:
        """Get next classe from calendar"""
        await update.message.reply_text("X_X Pas encore implémenté X_X")
    
    async def events(self, update: Update, context: CallbackContext) -> None:
        """Get all incoming events from calendar"""
        await update.message.reply_text("X_X Pas encore implémenté X_X")
    
    # messages
    async def unknown(self, update: Update, context: CallbackContext) -> None:
        """Reply to all commands that were not recognized by the previous handlers"""
        similar = calc_distance(update.effective_message.text, Bot.COMMANDS)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                text=f"Désolé, je ne comprends pas cette commande.\n\nVous vouliez peut-être dire {similar} ?")
    
    def run_bot(self):
        app = Application.builder().token(self.token).build()
    
        # dispatch commands
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_cmd))
        app.add_handler(CommandHandler("today", self.today))
        app.add_handler(CommandHandler("next", self.next_cmd))
        app.add_handler(CommandHandler("events", self.events))
        
        # dispatch messages
        app.add_handler(MessageHandler(filters.COMMAND, self.unknown))
        
        # run the bot until signal or Ctrl-C
        app.run_polling()
