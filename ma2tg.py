# flake8: noqa: E501
import os
from urllib.request import urlopen

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from release import Release

# load credentials from local environment
load_dotenv()
TOKEN = os.environ.get("TOKEN")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


def get_tlg_updates():
    ...


def create_db():
    ...


def get_release_links():
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
        page.wait_for_load_state("domcontentloaded")
        link_elements = page.query_selector_all("//a[contains(@id, 'tid-link')]")
        release_links = [element.get_attribute("href") for element in link_elements]
        browser.close()
    return release_links


def parse_release(link):
    html = urlopen(link)
    soup = BeautifulSoup(html.read(), features="html.parser")
    cover_link = soup.find("img", {"class": "linked-image"}).parent["href"]
    artist = soup.find_all("b")[6]
    album = soup.find_all("b")[7].next_sibling
    year = soup.find_all("b")[8].next_sibling
    genre = soup.find_all("b")[9].next_sibling
    country = soup.find_all("b")[10].next_sibling
    file = soup.find_all("b")[11].next_sibling
    size = soup.find_all("b")[12].next_sibling
    download_links_elements = soup.find("div", {"class": "hidemain"}).find_all("a")
    download_links = [el["href"] for el in download_links_elements]
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


def get_releases():
    links = get_release_links()
    return [parse_release(link) for link in links]


def send_releases(releases):
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
    get_tlg_updates()
    create_db()
    releases = get_releases()
    send_releases(releases)
