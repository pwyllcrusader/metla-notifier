import os

from dotenv import load_dotenv

import tgbot
import metalarea
import db


def load_credentials():
    load_dotenv()


if __name__ == "__main__":
    TOKEN = os.environ.get("TOKEN")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")

    bot = tgbot.get_bot(TOKEN)
    database = db.get_conn()
    metalarea.login(USERNAME, PASSWORD)
    releases = metalarea.get_releases_list()
