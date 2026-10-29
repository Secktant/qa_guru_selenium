import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://qa-guru.github.io/one-page-form/text-box.html"

valid_full_name = "Вася Пупкин"
valid_email = "test@example.com"
invalid_email = "test.com"
valid_current_address = "Москва"
valid_permanent_address = "Санкт-Петербург"
expected_name_placeholder = "Full Name"
expected_email_placeholder = "name@example.com"
expected_current_address_placeholder = "Current Address"
expected_validation_message = "Адрес электронной почты должен содержать символ \"@\". В адресе \"test.com\" отсутствует символ \"@\"."

FIELD_FULL_NAME = (By.ID, "userName")
FIELD_EMAIL = (By.ID, "userEmail")
FIELD_CURRENT_ADDRESS = (By.ID, "currentAddress")
FIELD_PERMANENT_ADDRESS = (By.ID, "permanentAddress")
SUBMIT_BUTTON = (By.ID, "submit")
OUTPUT_BOX = (By.ID, "output")
OUTPUT_BOX_FULL_NAME = (By.ID, "name")
OUTPUT_BOX_EMAIL = (By.ID, "email")
OUTPUT_BOX_CURRENT_ADDRESS = (By.ID, "currentAddress")
OUTPUT_BOX_PERMANENT_ADDRESS = (By.ID, "permanentAddress")


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.maximize_window()

    yield driver

    driver.quit()


def test_filling_in_fields(browser):
    # Открываем ссылку
    browser.get(URL)

    # Ищем поле с именем и заполняем его
    browser.find_element(*FIELD_FULL_NAME).send_keys(valid_full_name)

    # Ищем поле с почтой и заполняем его
    browser.find_element(*FIELD_EMAIL).send_keys(valid_email)

    # Ищем поле с текущим адресом и заполняем его
    browser.find_element(*FIELD_CURRENT_ADDRESS).send_keys(valid_current_address)

    # Ищем поле с постоянным адресом и заполняем его
    browser.find_element(*FIELD_PERMANENT_ADDRESS).send_keys(valid_permanent_address)

    # Ищем кнопку Submit и нажимаем на неё
    browser.find_element(*SUBMIT_BUTTON).click()

    # Находим форму с введенными данными
    output_box = browser.find_element(*OUTPUT_BOX)

    # Проверяем что все введенные данные есть в форме и в нужном поле
    assert valid_full_name in output_box.find_element(*OUTPUT_BOX_FULL_NAME).text
    assert valid_email in output_box.find_element(*OUTPUT_BOX_EMAIL).text
    assert valid_current_address in output_box.find_element(*OUTPUT_BOX_CURRENT_ADDRESS).text
    assert valid_permanent_address in output_box.find_element(*OUTPUT_BOX_PERMANENT_ADDRESS).text


def test_input_placeholder(browser):
    browser.get(URL)

    assert expected_name_placeholder == browser.find_element(*FIELD_FULL_NAME).get_attribute("placeholder")
    assert expected_email_placeholder == browser.find_element(*FIELD_EMAIL).get_attribute("placeholder")
    assert expected_current_address_placeholder == browser.find_element(*FIELD_CURRENT_ADDRESS).get_attribute(
        "placeholder")
    assert not browser.find_element(*FIELD_PERMANENT_ADDRESS).get_attribute("placeholder")


def test_invalid_email(browser):
    browser.get(URL)
    browser.find_element(*FIELD_FULL_NAME).send_keys(valid_full_name)
    browser.find_element(*FIELD_EMAIL).send_keys(invalid_email)
    browser.find_element(*SUBMIT_BUTTON).click()

    assert expected_validation_message in browser.execute_script("return arguments[0].validationMessage",
                                                                 browser.find_element(*FIELD_EMAIL))
    assert browser.execute_script("return arguments[0].validity.valid", browser.find_element(*FIELD_EMAIL)) is False
