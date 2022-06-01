import datetime
import pytz

# telegram related stuff
from telegram import Update
from telegram.ext import (Application, CommandHandler,
                          MessageHandler, CallbackContext, filters)
import logging  # log for telegram

from .levenshtein import calc_distance


class Bot:
    # TODO: use same timezone as calendar
    # time at which the reminder is triggered
    TIME_REMINDER = datetime.time(
        hour=8, minute=15, tzinfo=pytz.timezone("Europe/Paris")
    )

    # commands handled by the bot
    COMMANDS = ["/start", "/help", "/today", "/next", "/tasks", "/reminder"]

    # message sent by the bot at start
    START_MESSAGE = """
Bonjour, je suis le bot personnel de la Sprint !
Je vous tiendrais au courant des cours et des évenements de la journée.

Pour en savoir plus: /help.
"""

    # message sent by the bot to help
    HELP_MESSAGE = """
Les commandes suivantes sont disponibles:

/start -> Message de bienvenue
/help -> Affiche l'aide
/today -> Indique les cours d'aujourdhui
/next -> Indique le prochain cours
/tasks <period> -> Indique les tâches à venir dans la période donnée
/reminder <set|unset> -> Configure le rappel des tâches
"""

    def __init__(self, token: str, calendar):
        self.token = token
        self.calendar = calendar

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    # commands
    async def start(self, update: Update, _: CallbackContext) -> None:
        """Function called at each /start command"""
        await update.effective_message.reply_text(Bot.START_MESSAGE)

    async def help_cmd(self, update: Update, _: CallbackContext) -> None:
        """Helper function"""
        await update.effective_message.reply_text(Bot.HELP_MESSAGE)

    def get_today_msg(self) -> str:
        events = self.calendar.get_today_events()

        if not events:
            text = "Pas de cours aujourd'hui"
        else:
            text = "Les cours sont :\n\n" + "\n".join(map(str, events))

        return text

    async def today(self, update: Update, _: CallbackContext) -> None:
        """Get today classes from calendar"""
        text = self.get_today_msg()

        await update.effective_message.reply_text(text)

    async def next_cmd(self, update: Update, _: CallbackContext) -> None:
        """Get next classe from calendar"""
        event = self.calendar.get_next_event()

        if not event:
            text = "Pas de prochain cours"
        else:
            text = "Le prochain cours est :\n\n" + str(event)
        await update.effective_message.reply_text(text)

    def get_tasks_msg(self, period: int) -> str:
        tasks = self.calendar.get_incoming_tasks(period)

        if not tasks:
            text = "Pas de tâches à venir"
        else:
            text = "Les tâches à venir sont :\n\n" + \
                "\n".join(map(str, tasks))
        return text

    async def tasks(self, update: Update, context: CallbackContext) -> None:
        """Get all incoming tasks from calendar in a given period"""
        try:
            period = int(context.args[0])
            text = self.get_tasks_msg(period)

            await update.effective_message.reply_text(text)
        except (IndexError, ValueError):
            await update.effective_message.reply_text("Usage: /tasks <period>")

    def remove_job_if_exists(self, name: str, context: CallbackContext) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True

    async def callback_today(self, context: CallbackContext) -> None:
        """Send the daily reminder"""
        text = self.get_today_msg()

        await context.bot.send_message(context.job.chat_id, text=text)

    async def callback_tasks(self, context: CallbackContext) -> None:
        """Send the daily reminder"""
        text = self.get_tasks_msg(7)

        await context.bot.send_message(context.job.chat_id, text=text)

    def set_reminder(self, context: CallbackContext, chat_id: int) -> str:
        """Set the reminders"""
        text = "Les rappels des cours et des tâches ont bien été configuré."

        if self.remove_job_if_exists(str(chat_id), context):
            text = "Les anciens rappels ont été supprimé.\n" + text

        # set classes reminder
        context.job_queue.run_daily(
            self.callback_today, Bot.TIME_REMINDER,
            days=tuple(range(5)), chat_id=chat_id, name=str(chat_id)
        )
        # set tasks reminder
        context.job_queue.run_daily(
            self.callback_tasks, Bot.TIME_REMINDER,
            days=tuple([0]), chat_id=chat_id, name=str(chat_id)
        )

        return text

    def unset_reminder(self, context: CallbackContext, chat_id: int) -> str:
        """Unset the reminders"""
        if self.remove_job_if_exists(str(chat_id), context):
            text = "Les rappels ont bien été supprimé."
        else:
            text = "Il n'y a pas de rappel actif."

        return text

    async def reminder(self, update: Update, context: CallbackContext) -> None:
        """Set or unset the reminders"""
        chat_id = update.effective_message.chat_id

        try:
            arg = context.args[0]
            if arg == "set":
                text = self.set_reminder(context, chat_id)
            elif arg == "unset":
                text = self.unset_reminder(context, chat_id)
            else:
                text = "Usage: /reminder <set|unset>"

            await update.effective_message.reply_text(text)

        except (IndexError, ValueError):
            await update.effective_message.reply_text("Usage: /reminder <set|unset>")

    # messages
    async def unknown(self, update: Update, context: CallbackContext) -> None:
        """Reply to all commands that were not recognized"""
        similar = calc_distance(update.effective_message.text, Bot.COMMANDS)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=("Désolé, je ne comprends pas cette commande.\n\n"
                  f"Vous vouliez peut-être dire {similar} ?")
        )

    def run_bot(self):
        app = Application.builder().token(self.token).build()

        # dispatch commands
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_cmd))
        app.add_handler(CommandHandler("today", self.today))
        app.add_handler(CommandHandler("next", self.next_cmd))
        app.add_handler(CommandHandler("tasks", self.tasks))
        app.add_handler(CommandHandler("reminder", self.reminder))

        # dispatch messages
        app.add_handler(MessageHandler(filters.COMMAND, self.unknown))

        # run the bot until signal or Ctrl-C
        app.run_polling()
