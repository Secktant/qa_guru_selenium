import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://qa-guru.github.io/one-page-form/login.html"

INVALID_LOGIN = "TEST123"
PASSWORD_LESS_LESS_6_CHARACTERS = "123"
EXPECTED_ERROR_MESSAGE_ALL_FIELDS = "Login and password are required (minimum 3 and 6 characters)"

LOGIN_FIELD = (By.CSS_SELECTOR, "[data-testid='login-input']")
PASSWORD_FIELD = (By.CSS_SELECTOR, "[data-testid='password-input']")
ERROR_FIELDS_EMPTY = (By.CSS_SELECTOR, "[data-testid='error-message']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-button']")


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def test_submit_with_empty_fields_shows_error(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_BUTTON).click()
    assert EXPECTED_ERROR_MESSAGE_ALL_FIELDS == browser.find_element(*ERROR_FIELDS_EMPTY).text
