from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class LoginPage:
    URL = "https://qa-guru.github.io/one-page-form/login.html"

    # Локаторы страницы
    LOGIN_FIELD = (By.CSS_SELECTOR, "[data-testid='login-input']")
    PASSWORD_FIELD = (By.CSS_SELECTOR, "[data-testid='password-input']")
    ERROR_FIELDS_EMPTY = (By.CSS_SELECTOR, "[data-testid='error-message']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-button']")
    WELCOME_MESSAGE_FIELD = (By.CSS_SELECTOR, "[data-testid='welcome-message']")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='logout-button']")
    LOGIN_FORM_TITLE = (By.CSS_SELECTOR, "[data-testid='login-form-title']")

    def __init__(self, driver):  # указываем неявные ожидания
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):  # открываем вкладку с нужным урлом
        self.driver.get(self.URL)
        return self

    def submit(self):  # действие нажатия на кнопку "Login"
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        return self

    def get_error_message(self):  # получить сообщение об ошибке
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_FIELDS_EMPTY)).text

    def fill_form(self, login=None, password=None):  # заполнить логин пароль
        if login is not None:
            self.wait.until(EC.element_to_be_clickable(self.LOGIN_FIELD)).send_keys(login)
        if password is not None:
            self.wait.until(EC.element_to_be_clickable(self.PASSWORD_FIELD)).send_keys(password)
        return self

    def get_welcome_message(self):  # получить приветственное сообщение
        return self.wait.until(EC.visibility_of_element_located(self.WELCOME_MESSAGE_FIELD)).text

    def logout(self):  # нажать кнопку логаута
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_BUTTON)).click()
        return self

    def is_logout_button_visible(self):
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_BUTTON))
        return True

    def get_login_form_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.LOGIN_FORM_TITLE)).text

    def is_login_form_visible(self):  # ожидание отображение формы логина
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD))
        self.wait.until(EC.visibility_of_element_located(self.LOGIN_BUTTON))
        return True
