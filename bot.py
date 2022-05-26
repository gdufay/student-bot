import argparse # cli handler
import logging # log for telegram

# telegram related stuff
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

# commands
async def start(update: Update, context: CallbackContext) -> None:
    """Function called at each /start command"""
    await update.message.reply_text(START_MESSAGE)

async def help_cmd(update: Update, context: CallbackContext) -> None:
    """Helper function"""
    await update.message.reply_text(HELP_MESSAGE)

async def today(update: Update, context: CallbackContext) -> None:
    """Get today classes from calendar"""
    await update.message.reply_text("X_X Pas encore implémenté X_X")

async def next_cmd(update: Update, context: CallbackContext) -> None:
    """Get next classe from calendar"""
    await update.message.reply_text("X_X Pas encore implémenté X_X")

async def events(update: Update, context: CallbackContext) -> None:
    """Get all incoming events from calendar"""
    await update.message.reply_text("X_X Pas encore implémenté X_X")

# messages
async def unknown(update: Update, context: CallbackContext) -> None:
    """Reply to all commands that were not recognized by the previous handlers"""
    await update.message.reply_text("Désolé, je ne comprends pas cette commande.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telegram Sprint Bot")

    # add arguments to parser
    parser.add_argument("token", help="Telegram token")
    parser.add_argument("--credential_file", default="credentials.json", help="Path to Google credentials file")
    parser.add_argument("--cookie_file", default="token.json", help="Path to Google token storage file")

    return parser.parse_args()

def main() -> None:
    """Run the bot."""
    # get cli arguments
    args = parse_args()

    # TODO: catch InvalidToken error
    # TODO: catch other errors
    app = Application.builder().token(args.token).build()

    # dispatch commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("next", next_cmd))
    app.add_handler(CommandHandler("events", events))
    
    # dispatch messages
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # run the bot until signal or Ctrl-C
    app.run_polling()

    print("Bye !")

if __name__ == "__main__":
    main()
