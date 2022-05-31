# telegram related stuff
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

from .levenshtein import calc_distance

class Bot:
    COMMANDS = ["/start", "/help", "/today", "/next", "/tasks"]
    
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
/tasks période -> Indique les tâches à venir dans la période donnée
"""

    def __init__(self, token, calendar):
        self.token = token
        self.calendar = calendar

    # commands
    async def start(self, update: Update, context: CallbackContext) -> None:
        """Function called at each /start command"""
        await update.effective_message.reply_text(Bot.START_MESSAGE)
    
    async def help_cmd(self, update: Update, context: CallbackContext) -> None:
        """Helper function"""
        await update.effective_message.reply_text(Bot.HELP_MESSAGE)
    
    async def today(self, update: Update, context: CallbackContext) -> None:
        """Get today classes from calendar"""
        events = self.calendar.get_today_events()

        if not events:
            text = "Pas de cours aujourd'hui"
        else:
            text = "Les cours sont :\n\n" + "\n".join(map(str, events))
        await update.effective_message.reply_text(text)
    
    async def next_cmd(self, update: Update, context: CallbackContext) -> None:
        """Get next classe from calendar"""
        event = self.calendar.get_next_event()

        if not event:
            text = "Pas de prochain cours"
        else:
            text = "Le prochain cours est :\n\n" + str(event)
        await update.effective_message.reply_text(text)
    
    async def tasks(self, update: Update, context: CallbackContext) -> None:
        """Get all incoming tasks from calendar in a given period"""
        period = int(context.args[0]) if context.args else 7
        tasks = self.calendar.get_incoming_tasks(period)

        if not tasks:
            text = "Pas de tâches à venir"
        else:
            text = "Les tâches à venir sont :\n\n" + "\n".join(map(str, tasks))

        await update.effective_message.reply_text(text)
    
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
        app.add_handler(CommandHandler("tasks", self.tasks))
        
        # dispatch messages
        app.add_handler(MessageHandler(filters.COMMAND, self.unknown))
        
        # run the bot until signal or Ctrl-C
        app.run_polling()
