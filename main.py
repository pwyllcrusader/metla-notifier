import os

from dotenv import load_dotenv


def load_credentials():
    load_dotenv()


if __name__ == '__main__':
    TOKEN = os.environ.get("TOKEN")
