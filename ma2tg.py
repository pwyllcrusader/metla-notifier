# flake8: noqa: E501
import os
import sqlite3
from time import sleep
from urllib.request import urlopen

import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from release import Release

# load credentials from local environment
load_dotenv()
TOKEN = os.environ.get("TOKEN")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")
BOT = telebot.TeleBot(TOKEN)
DB_CONN = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/ma.sqlite")
DB = DB_CONN.cursor()
DB.execute("CREATE TABLE IF NOT EXISTS chat_ids (id TEXT)")
DB.execute(
    """CREATE TABLE IF NOT EXISTS releases (
        img_link TEXT, 
        artist TEXT, 
        album TEXT, 
        year TEXT, 
        genre TEXT,
        country TEXT,
        file TEXT,
        size TEXT,
        links TEXT
    )"""
)


def get_tlg_updates():
    updates = BOT.get_updates()
    for update in updates:
        if update:
            user_chat_id = update.message.chat.id
            username = update.message.chat.username
            if not is_chat_id_is_in_db(user_chat_id):
                BOT.send_message(
                    user_chat_id,
                    f"Infernal hailz, {username}!",
                )
                DB.execute("INSERT INTO chat_ids VALUES (?)", (user_chat_id,))
                DB_CONN.commit()


def is_chat_id_is_in_db(chat_id):
    DB.execute("SELECT * FROM chat_ids WHERE id=?", (chat_id,))
    is_present = False
    if DB.fetchall():
        return True
    return is_present


def is_release_is_in_db(release):
    DB.execute("SELECT * FROM releases WHERE links=?", (release.download_links,))
    is_present = False
    if DB.fetchall():
        return True
    return is_present


def get_release_links():
    with sync_playwright() as p:
        browser = p.chromium.launch()
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
        page.wait_for_load_state("domcontentloaded")
        link_elements = page.query_selector_all("//a[contains(@id, 'tid-link')]")
        release_links = [element.get_attribute("href") for element in link_elements]
        browser.close()
    return release_links


def parse_release(link):
    auth = {"UserName": USERNAME, "PassWord": PASSWORD}
    session = requests.session()
    session.post(
        "https://metalarea.org/forum/index.php?act=Login&CODE=01&CookieDate=1&return=https://metalarea.org",
        data=auth,
    )
    html = session.get(link).content
    soup = BeautifulSoup(html, features="html.parser")

    cover_link = soup.find("img", {"class": "linked-image"}).parent["href"]
    artist = soup.find_all("b")[6].next
    album = soup.find_all("b")[7].next_sibling
    year = soup.find_all("b")[8].next_sibling
    genre = soup.find_all("b")[9].next_sibling
    country = soup.find_all("b")[10].next_sibling
    file = soup.find_all("b")[11].next_sibling
    size = soup.find_all("b")[12].next_sibling
    download_links_elements = soup.find("div", {"class": "hidemain"}).find_all("a")
    download_links = [el["href"] for el in download_links_elements][0]
    return Release(
        cover_link,
        artist,
        album,
        year,
        genre,
        country,
        file,
        size,
        download_links,
    )


def get_releases_from_ma():
    links = get_release_links()
    return [parse_release(link) for link in links]


def send_releases(releases_to_send):
    users = get_chat_ids_from_db()
    for user in users:
        for release in releases_to_send:
            if not is_release_is_in_db(release):
                add_release_to_db(release)
                BOT.send_message(user[0], release)
                sleep(5)


def add_release_to_db(release):
    DB.execute(
        "INSERT INTO releases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            release.cover_link,
            release.artist,
            release.album,
            release.year,
            release.genre,
            release.country,
            release.file,
            release.size,
            release.download_links,
        ),
    )
    DB_CONN.commit()


def get_chat_ids_from_db():
    cursor = DB.execute("SELECT * FROM chat_ids")
    return cursor.fetchall()


if __name__ == "__main__":
    get_tlg_updates()
    releases = get_releases_from_ma()
    send_releases(releases)
