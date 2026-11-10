from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class CalendarElement:
    def __init__(self, driver):
        self.driver = driver

    CALENDAR_INPUT = (By.ID, "dateOfBirthInput")
    YEAR_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__year-select")
    MONTH_OF_BIRTH_SELECT = (By.CSS_SELECTOR, ".react-datepicker__month-select")

    def select_birth_day(self, date: Tuple[str, str, str]):
        self.driver.find_element(*self.CALENDAR_INPUT).click()
        Select(self.driver.find_element(*self.YEAR_OF_BIRTH_SELECT)).select_by_value(date[0])
        Select(self.driver.find_element(*self.MONTH_OF_BIRTH_SELECT)).select_by_value(date[1])
        self.driver.find_element(By.CSS_SELECTOR, f".react-datepicker__day--0{date[2]}[tabindex='0']").click()
