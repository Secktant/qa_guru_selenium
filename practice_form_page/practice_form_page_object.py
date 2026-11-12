from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class PracticeFormPage:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    # Локаторы
    FIRST_NAME_FIELD = (By.ID, "firstName")
    LAST_NAME_FIELD = (By.ID, "lastName")
    GENDER_RADIO_MALE = (By.ID, "gender-radio-1")
    GENDER_RADIO_FEMALE = (By.ID, "gender-radio-2")
    GENDER_RADIO_OTHER = (By.ID, "gender-radio-3")
    USER_NUMBER_FIELD = (By.ID, "userNumber")
    SUBMIT_BUTTON = (By.ID, "submit")
    RESULT_MODAL = (By.ID, "resultModal")
    ERROR_MESSAGE = (By.ID, "formError")
    CLOSE_MODAL = (By.CSS_SELECTOR, "button[aria-label=\"Close\"]")

    def __init__(self, driver):  # указываем неявные ожидания
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def fill_first_name(self, first_name=None):
        if first_name is not None:
            self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_FIELD)).send_keys(first_name)
        return self

    def fill_last_name(self, last_name=None):
        if last_name is not None:
            self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_FIELD)).send_keys(last_name)
        return self

    def fill_user_number(self, number=None):
        if number is not None:
            self.wait.until(EC.element_to_be_clickable(self.USER_NUMBER_FIELD)).send_keys(number)

    def submit_click(self):
        submit_button = self.wait.until((EC.element_to_be_clickable(self.SUBMIT_BUTTON)))
        # submit_button.execute_script("arguments[0].scrollIntoView(true);")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        return self

    def wait_for_result_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.RESULT_MODAL))

    def get_error_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text

    def click_male_ratio(self):
        self.wait.until(EC.element_to_be_clickable(self.GENDER_RADIO_MALE)).click()
        return self

    def close_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_MODAL)).click()
        return self
