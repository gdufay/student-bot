import os  # get environment variable
import sys  # exit when error
import argparse
from utils.auth import create_app  # cli handler

from utils.bot import Bot
from utils.calendar import Calendar


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telegram Student Bot")

    # add arguments to parser
    parser.add_argument("--secret_file", default="credentials.json",
                        help="Path to Google credentials file")
    parser.add_argument(
        "--port", help="port from where flask server is listening", type=int)

    return parser.parse_args()


def main() -> None:
    """Run the bot."""
    # get telegram token
    try:
        token = os.environ["BOT_TOKEN"]
    except KeyError:
        sys.exit("BOT_TOKEN not set")

    # get cli arguments
    args = parse_args()

    calendar = Calendar(credentials_path=args.credential_file,
                        token_path=args.cookie_file, port=args.port)
    calendar.build()

    # TODO: catch InvalidToken error
    # TODO: catch other errors
    # launch the bot
    bot = Bot(token, calendar)
    bot.run_bot()

    app = create_app(bot, args.secret_file)
    app.run('localhost', args.port, debug=True)

    print("Bye !")


if __name__ == "__main__":
    main()
