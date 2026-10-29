import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("setup")
class TestDynamicallyLoadedPageElements:
    URL = "https://the-internet.herokuapp.com/dynamic_loading"
    EXAMPLE_1_LINK = (By.XPATH, "//a[text()='Example 1: Element on page that is hidden']")
    EXAMPLE_2_LINK = (By.XPATH, "//a[text()='Example 2: Element rendered after the fact']")
    START_BUTTON = (By.CSS_SELECTOR, "[id='start'] button")
    EXPECTED_TEXT = "Hello World!"

    @pytest.fixture(scope="function")
    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_example_1_link_1(self):
        self.driver.find_element(*self.EXAMPLE_1_LINK).click()
        self.driver.find_element(*self.START_BUTTON).click()
        finish_text = self.wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        assert self.EXPECTED_TEXT == finish_text.text

    def test_example_2_link_2(self):
        self.driver.find_element(*self.EXAMPLE_2_LINK).click()
        self.driver.find_element(*self.START_BUTTON).click()
        finish_text = self.wait.until(EC.visibility_of_element_located((By.ID, "finish")))
        assert self.EXPECTED_TEXT == finish_text.text
