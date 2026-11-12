import time

from practice_form_page.practice_form_page_object import PracticeFormPage


class TestPracticeFormPage:
    # Данные
    first_name = 'Enakin'
    last_name = 'Skywalker'
    valid_number = '1234567890'
    ALL_FIELDS_REQUIRED_ERROR_TEXT = "Please fill required fields and enter a valid 10-digit mobile number."

    def test_submit_with_all_fields_empty_shows_error(self, driver):
        page = PracticeFormPage(driver)
        page.open()
        actual_error_message = page.close_modal().submit_click().get_error_message()
        assert self.ALL_FIELDS_REQUIRED_ERROR_TEXT == actual_error_message

    def test_submit_with_required_fields_shows_result_modal(self, driver):
        page = PracticeFormPage(driver)
        page.open()
        page.fill_first_name(self.first_name).fill_last_name(self.last_name).fill_user_number(self.valid_number)
        page.click_male_ratio()
        page.close_modal()
        modal = page.submit_click().wait_for_result_modal()
        assert modal.is_displayed()


