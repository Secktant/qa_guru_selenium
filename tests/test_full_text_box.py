from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://qa-guru.github.io/one-page-form/text-box.html"

valid_full_name = "Вася Пупкин"
valid_email = "test@example.com"
invalid_email = "test.com"
valid_current_address = "Москва"
valid_permanent_address = "Санкт-Петербург"


def test_filling_in_fields():
    driver = webdriver.Chrome()
    try:
        # Открываем браузер
        driver.get(URL)

        # Ищем поле с именем и заполняем его
        field_full_name = driver.find_element(By.ID, "userName")
        field_full_name.send_keys(valid_full_name)

        # Ищем поле с почтой и заполняем его
        field_email = driver.find_element(By.ID, "userEmail")
        field_email.send_keys(valid_email)

        # Ищем поле с текущим адресом и заполняем его
        field_current_address = driver.find_element(By.ID, "currentAddress")
        field_current_address.send_keys(valid_current_address)

        # Ищем поле с постоянным адресом и заполняем его
        field_permanent_address = driver.find_element(By.ID, "permanentAddress")
        field_permanent_address.send_keys(valid_permanent_address)

        # Ищем кнопку Submit и нажимаем на неё
        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        # Находим форму с введенными данными
        output_box = driver.find_element(By.ID, "output")

        # Находим имена полей в форме с введенными данными
        output_box_full_name = output_box.find_element(By.ID, "name")
        output_box_email = output_box.find_element(By.ID, "email")
        output_box_current_address = output_box.find_element(By.ID, "currentAddress")
        output_box_permanent_address = output_box.find_element(By.ID, "permanentAddress")

        # Проверяем что все введенные данные есть в форме и в нужном поле
        assert valid_full_name in output_box_full_name.text
        assert valid_email in output_box_email.text
        assert valid_current_address in output_box_current_address.text
        assert valid_permanent_address in output_box_permanent_address.text
    finally:
        driver.quit()


def test_input_placeholder():
    driver = webdriver.Chrome()
    expected_name_placeholder = "Full Name"
    expected_email_placeholder = "name@example.com"
    expected_current_address_placeholder = "Current Address"
    try:
        driver.get(URL)

        field_full_name = driver.find_element(By.ID, "userName")
        actual_name_placeholder = field_full_name.get_attribute("placeholder")

        field_email = driver.find_element(By.ID, "userEmail")
        actual_email_placeholder = field_email.get_attribute("placeholder")

        field_current_address = driver.find_element(By.ID, "currentAddress")
        actual_current_address_placeholder = field_current_address.get_attribute("placeholder")

        field_permanent_address = driver.find_element(By.ID, "permanentAddress")
        actual_permanent_address_placeholder = field_permanent_address.get_attribute("placeholder")

        assert expected_name_placeholder == actual_name_placeholder
        assert expected_email_placeholder == actual_email_placeholder
        assert expected_current_address_placeholder == actual_current_address_placeholder
        assert not actual_permanent_address_placeholder
    finally:
        driver.quit()


def test_invalid_email():
    driver = webdriver.Chrome()
    expected_validation_message = "Адрес электронной почты должен содержать символ \"@\". В адресе \"test.com\" отсутствует символ \"@\"."
    try:

        driver.get(URL)

        full_name_field = driver.find_element(By.ID, "userName")
        full_name_field.send_keys(valid_full_name)

        email_field = driver.find_element(By.ID, "userEmail")
        email_field.send_keys(invalid_email)

        submit_button = driver.find_element(By.ID, "submit")
        submit_button.click()

        validation_message = driver.execute_script("return arguments[0].validationMessage", email_field)

        is_valid = driver.execute_script("return arguments[0].validity.valid", email_field)

        assert expected_validation_message in validation_message and is_valid is False

    finally:
        driver.quit()
