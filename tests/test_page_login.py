import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup")
class TestLoginForm:
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
    LOGIN_FORM_TITLE = (By.CSS_SELECTOR, "[data-testid='login-form-title']")

    @pytest.fixture(scope="function")
    def setup(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(self.URL)
        yield self.driver
        self.driver.quit()

    def test_submit_with_all_fields_empty_shows_error(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.ALL_FIELDS_REQUIRED_ERROR_TEXT == self.wait.until(EC.visibility_of_element_located(self.ERROR_FIELDS_EMPTY)).text

    def test_login_shorter_than_3_chars_shows_min_length_error(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.LOGIN_LESS_THAN_3_CHARS)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.LOGIN_MIN_LENGTH_ERROR_TEXT == self.wait.until(EC.visibility_of_element_located(self.ERROR_FIELDS_EMPTY)).text

    def test_submit_with_invalid_login_and_password_shows_invalid_credentials_error(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.NONEXISTENT_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(self.PASSWORD_EXACTLY_6_CHARS)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.INVALID_CREDENTIALS_ERROR_TEXT == self.wait.until(EC.visibility_of_element_located(self.ERROR_FIELDS_EMPTY)).text

    def test_submit_with_valid_login_and_short_password_shows_password_min_length_error(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.NONEXISTENT_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(self.PASSWORD_LESS_THAN_6_CHARS)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.PASSWORD_MIN_LENGTH_ERROR_TEXT == self.wait.until(EC.visibility_of_element_located(self.ERROR_FIELDS_EMPTY)).text

    def test_successful_login_shows_welcome_message_with_username(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.VALID_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(self.VALID_PASSWORD)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.WELCOME_MESSAGE_TEMPLATE == self.wait.until(EC.visibility_of_element_located(self.WELCOME_MESSAGE_FIELD)).text

    def test_logout_button_is_displayed_after_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.VALID_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(self.VALID_PASSWORD)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        assert self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).is_displayed()

    def test_logout_via_logout_button_returns_to_login_form(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(self.VALID_LOGIN)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(self.VALID_PASSWORD)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).click()
        assert self.LOGIN_FORM_TITLE_TEXT == self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM_TITLE)).text
        assert self.wait.until(EC.visibility_of_element_located(self.LOGIN_FIELD)).is_displayed()
        assert self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).is_displayed()
        assert self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON)).is_displayed()
