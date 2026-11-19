from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class Calendar:
    CLOSE_MODAL = (By.CSS_SELECTOR, "button[aria-label=\"Close\"]")
    INFO_BANNER = (By.ID, "fixedban")
    DATE_OF_BIRTH_INPUT = (By.ID, "dateOfBirthInput")
    MONTH_SELECT = (By.CSS_SELECTOR, "select[class=\"react-datepicker__month-select\"]")
    YEAR_SELECT = (By.CSS_SELECTOR, "select[class=\"react-datepicker__year-select\"]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def close_banner(self):
        self.wait.until(EC.element_to_be_clickable(self.CLOSE_MODAL)).click()
        self.wait.until(EC.invisibility_of_element_located(self.INFO_BANNER))
        return self

    def select_date(self, day, month, year):
        self.wait.until(EC.element_to_be_clickable(self.DATE_OF_BIRTH_INPUT)).click()
        month_element = self.wait.until(EC.element_to_be_clickable(self.MONTH_SELECT))
        Select(month_element).select_by_visible_text(month)
        year_element = self.wait.until(EC.element_to_be_clickable(self.YEAR_SELECT))
        Select(year_element).select_by_visible_text(year)
        day_padded = day.zfill(3)
        day_locator = (By.CSS_SELECTOR,
                       f"span[class=\"react-datepicker__day react-datepicker__day--{day_padded}\"]:not(.react-datepicker__day--outside-month)")
        self.wait.until(EC.element_to_be_clickable(day_locator)).click()

driver = webdriver.Chrome()
try:
    driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
    calendar = Calendar(driver)
    calendar.close_banner().select_date("15", "July", "2000")
    date_id = driver.find_element(By.ID, "dateOfBirthInput")
    actual_date = date_id.get_property("value")
    assert actual_date == "15 Jul 2000"
finally:
    driver.quit()