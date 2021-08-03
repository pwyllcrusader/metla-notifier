import os

from dotenv import load_dotenv


def load_credentials():
    load_dotenv()


if __name__ == '__main__':
    TOKEN = os.environ.get("TOKEN")
    USERNAME = os.environ.get("USERNAME")
    PASSWORD = os.environ.get("PASSWORD")
