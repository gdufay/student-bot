import os  # get environment variable
import sys  # exit when error
import argparse
from utils.auth import FlaskThread, create_app  # cli handler

from utils.bot import Bot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Telegram Student Bot")

    # add arguments to parser
    parser.add_argument("--secret_file", default="credentials.json",
                        help="Path to Google credentials file")
    parser.add_argument(
        "--port", help="port from where flask server is listening", type=int)
    parser.add_argument("--tz", help="Timezone of the bot",
                        default="Europe/Paris")

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

    # TODO: catch InvalidToken error
    # TODO: catch other errors
    # launch the bot
    bot = Bot(token, timezone=args.tz)

    flask_thread = FlaskThread(port=args.port)
    flask_thread.app = create_app(bot, args.secret_file)
    flask_thread.start()

    bot.run_bot()

    print("Bye !")


if __name__ == "__main__":
    main()
