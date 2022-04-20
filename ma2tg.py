# flake8: noqa: E501
import os
from datetime import datetime, timedelta
from time import sleep

import requests
import telebot
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

from release import Release

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_CHAT_ID = os.getenv("BOT_CHAT_ID")
MA_USERNAME = os.getenv("MA_USERNAME")
MA_PASSWORD = os.getenv("MA_PASSWORD")

BOT = telebot.TeleBot(BOT_TOKEN)
YESTERDAY = datetime.today() - timedelta(days=1)


def get_release_links():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://metalarea.org")
        # login
        page.fill("//input[@name='UserName']", MA_USERNAME)
        page.fill("//input[@name='PassWord']", MA_PASSWORD)
        page.click("//input[@name='submit']")
        # go to new releases
        page.click("//a[@href='https://metalarea.org/forum/index.php?showforum=2']")
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
    auth = {"UserName": MA_USERNAME, "PassWord": MA_PASSWORD}
    session = requests.session()
    session.post(
        "https://metalarea.org/forum/index.php?act=Login&CODE=01&CookieDate=1&return=https://metalarea.org",
        data=auth,
    )
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})
    html = session.get(link).content
    soup = BeautifulSoup(html, features="html.parser")
    cover_link = soup.find("img", {"class": "linked-image"}).parent["href"]
    artist = list(soup.find_all("b", string="Артист")[0].parent.descendants)[4].text
    album = soup.find_all("b", string="Альбом")[0].next_sibling
    year = soup.find_all("b", string="Год")[0].next_sibling
    genre = soup.find_all("b", string="Стиль")[0].next_sibling
    country = soup.find_all("b", string="Страна")[0].next_sibling
    file = soup.find_all("b", string="Формат")[0].next_sibling
    size = soup.find_all("b", string="Размер")[0].next_sibling
    download_links_elements = soup.find("div", {"class": "hidemain"}).find_all("a")
    download_links = [el["href"] for el in download_links_elements]
    uploaded_at = datetime.strptime(
        soup.find_all("span", {"class": "postdetails"})[0].text.strip(),
        "%b %d %Y, %H:%M:%S",
    )
    return Release(
        link,
        cover_link,
        artist,
        album,
        year,
        genre,
        country,
        file,
        size,
        download_links,
        uploaded_at,
    )


def get_releases_from_ma():
    links = get_release_links()
    return [parse_release(link) for link in links]


def send_releases(releases_to_send):
    for release in releases_to_send:
        if release.uploaded_at >= YESTERDAY:
            print(
                f"Sending release {release.artist} - {release.album} ({release.year})"
            )
            BOT.send_message(BOT_CHAT_ID, release, parse_mode="markdown")
            sleep(5)


if __name__ == "__main__":
    releases = get_releases_from_ma()
    send_releases(releases)
