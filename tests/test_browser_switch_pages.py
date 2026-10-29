import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.window import WindowTypes

URL_TEXT_BOX = "https://qa-guru.github.io/one-page-form/text-box.html"
URL_LOGIN_FORM = "https://qa-guru.github.io/one-page-form/login.html"


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver


def test_open_pages(browser):
    browser.get(URL_TEXT_BOX)
    page_first = browser.current_window_handle
    browser.switch_to.new_window(WindowTypes.TAB)
    browser.get(URL_LOGIN_FORM)
    browser.switch_to.new_window(WindowTypes.TAB)
    browser.get("https://google.com")
    all_windows = browser.window_handles
    time.sleep(2)
    browser.switch_to.window(page_first)
    time.sleep(2)
    for window in all_windows:
        if window != page_first:
            browser.switch_to.window(window)
            browser.close()
            time.sleep(2)
    browser.switch_to.window(page_first)
    browser.switch_to.new_window(WindowTypes.TAB)
    browser.switch_to.window(page_first)
    browser.switch_to.window(browser.window_handles[1])
    browser.get("https://ya.ru")
    browser.switch_to.window(page_first)
    browser.close()
    time.sleep(5)

