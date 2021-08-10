from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def get_release_links(username, password):
    time = 5
    browser = webdriver.Firefox()
    metalarea = "http://metalarea.org/"
    browser.get(metalarea)
    username_input = browser.find_element_by_xpath("//input[@name='UserName']")
    username_input.send_keys(username)
    password_input = browser.find_element_by_xpath("//input[@name='PassWord']")
    password_input.send_keys(password)
    browser.find_element_by_xpath("//input[@name='submit']").click()
    WebDriverWait(browser, time).until(
        ec.invisibility_of_element(
            "//a[@href='./forum/index.php?showforum=2']"
        )
    )
    browser.find_element_by_xpath(
        "//a[@href='./forum/index.php?showforum=2']"
    ).click()
    browser.find_element_by_xpath("//select[@name='topicfilter']").click()
    browser.find_element_by_xpath("//option[@name='hot']").click()
    links = browser.find_elements_by_xpath("//a[contains(@id,'tid-link')]")
    return [link.get_attribute("href") for link in links]


def parse_release():
    ...


def get_releases_list(username, password):
    links = get_release_links(username, password)
    return [parse_release(link) for link in links]
