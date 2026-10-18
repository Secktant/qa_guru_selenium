import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://qa-guru.github.io/one-page-form/login.html"

NONEXISTENT_LOGIN = "TEST123"
LOGIN_LESS_THAN_3_CHARS = "te"
PASSWORD_LESS_THAN_6_CHARS = "123"
PASSWORD_EXACTLY_6_CHARS = "123456"
PASSWORD_MORE_THAN_6_CHARS = "1234567"
ALL_FIELDS_REQUIRED_ERROR_TEXT = "Login and password are required (minimum 3 and 6 characters)"
LOGIN_MIN_LENGTH_ERROR_TEXT = "Login must be at least 3 characters"
INVALID_CREDENTIALS_ERROR_TEXT = "Wrong login or password"
PASSWORD_MIN_LENGTH_ERROR_TEXT = "Password must be at least 6 characters"
VALID_LOGIN = "user1"
VALID_PASSWORD = "password1"
WELCOME_MESSAGE_TEMPLATE = f"Welcome, {VALID_LOGIN}!"
LOGIN_FORM_TITLE_TEXT = "Login Form"

LOGIN_FIELD = (By.CSS_SELECTOR, "[data-testid='login-input']")
PASSWORD_FIELD = (By.CSS_SELECTOR, "[data-testid='password-input']")
ERROR_FIELDS_EMPTY = (By.CSS_SELECTOR, "[data-testid='error-message']")
LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-button']")
WELCOME_MESSAGE_FIELD = (By.CSS_SELECTOR, "[data-testid='welcome-message']")
LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='logout-button']")
LOGIN_FORM_TITLE =(By.CSS_SELECTOR, "[data-testid='login-form-title']")

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def test_submit_with_all_fields_empty_shows_error(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_BUTTON).click()
    assert ALL_FIELDS_REQUIRED_ERROR_TEXT == browser.find_element(*ERROR_FIELDS_EMPTY).text


def test_login_shorter_than_3_chars_shows_min_length_error(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(LOGIN_LESS_THAN_3_CHARS)
    browser.find_element(*LOGIN_BUTTON).click()
    assert  LOGIN_MIN_LENGTH_ERROR_TEXT == browser.find_element(*ERROR_FIELDS_EMPTY).text


def test_submit_with_invalid_login_and_password_shows_invalid_credentials_error(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(NONEXISTENT_LOGIN)
    browser.find_element(*PASSWORD_FIELD).send_keys(PASSWORD_EXACTLY_6_CHARS)
    browser.find_element(*LOGIN_BUTTON).click()
    assert INVALID_CREDENTIALS_ERROR_TEXT == browser.find_element(*ERROR_FIELDS_EMPTY).text

def test_submit_with_valid_login_and_short_password_shows_password_min_length_error(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(NONEXISTENT_LOGIN)
    browser.find_element(*PASSWORD_FIELD).send_keys(PASSWORD_LESS_THAN_6_CHARS)
    browser.find_element(*LOGIN_BUTTON).click()
    assert  PASSWORD_MIN_LENGTH_ERROR_TEXT == browser.find_element(*ERROR_FIELDS_EMPTY).text

def test_successful_login_shows_welcome_message_with_username(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(VALID_LOGIN)
    browser.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
    browser.find_element(*LOGIN_BUTTON).click()
    assert WELCOME_MESSAGE_TEMPLATE == browser.find_element(*WELCOME_MESSAGE_FIELD).text

def test_logout_button_is_displayed_after_login(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(VALID_LOGIN)
    browser.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
    browser.find_element(*LOGIN_BUTTON).click()
    assert browser.find_element(*LOGOUT_BUTTON).is_displayed()


def test_logout_via_logout_button_returns_to_login_form(browser):
    browser.get(URL)
    browser.find_element(*LOGIN_FIELD).send_keys(VALID_LOGIN)
    browser.find_element(*PASSWORD_FIELD).send_keys(VALID_PASSWORD)
    browser.find_element(*LOGIN_BUTTON).click()
    browser.find_element(*LOGOUT_BUTTON).click()
    assert LOGIN_FORM_TITLE_TEXT == browser.find_element(*LOGIN_FORM_TITLE).text
    assert browser.find_element(*LOGIN_FIELD).is_displayed()
    assert browser.find_element(*PASSWORD_FIELD).is_displayed()
    assert browser.find_element(*LOGIN_BUTTON).is_displayed()


