import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# load credentials from local environment
load_dotenv()
TOKEN = os.environ.get("TOKEN")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def get_release_links():
    release_links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("http://metalarea.org")
        # login
        page.fill("//input[@name='UserName']", USERNAME)
        page.fill("//input[@name='PassWord']", PASSWORD)
        page.click("//input[@name='submit']")
        # go to new releases
        page.click("//a[@href='./forum/index.php?showforum=2']")
        # show hot releases
        page.select_option("//select[@name='topicfilter']", "hot")
        page.click(
            "//form[@method='post']/input[@class='button'][@value='Ок'][@type='submit']"
        )
        elements = page.querySelectorAll("//a[contains(@id, 'tid-link')]")
        release_links = [element.get_attribute("href") for element in elements]
        browser.close()
    return release_links


def parse_release(link):
    ...


def get_releases():
    links = get_release_links()
    return [parse_release(link) for link in links]


def create_db():
    ...


def add_release_to_db(release):
    ...


def get_releases_from_db():
    ...


def save_chat_id_to_db(chat_id):
    ...


def get_chat_ids_from_db():
    ...


if __name__ == "__main__":
    get_release_links()
