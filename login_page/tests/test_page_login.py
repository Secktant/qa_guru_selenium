from login_page.login_page import LoginPage


class TestLoginForm:
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

    def test_submit_with_all_fields_empty_shows_error(self, driver):
        page = LoginPage(driver)
        actual_error = page.open().submit().get_error_message()
        assert self.ALL_FIELDS_REQUIRED_ERROR_TEXT == actual_error

    def test_login_shorter_than_3_chars_shows_min_length_error(self, driver):
        page = LoginPage(driver)
        actual_error = page.open().fill_form(self.LOGIN_LESS_THAN_3_CHARS).submit().get_error_message()
        assert self.LOGIN_MIN_LENGTH_ERROR_TEXT == actual_error

    def test_submit_with_invalid_login_and_password_shows_invalid_credentials_error(self, driver):
        page = LoginPage(driver)
        actual_error = page.open().fill_form(self.NONEXISTENT_LOGIN, self.PASSWORD_EXACTLY_6_CHARS).submit().get_error_message()
        assert self.INVALID_CREDENTIALS_ERROR_TEXT == actual_error

    def test_submit_with_valid_login_and_short_password_shows_password_min_length_error(self, driver):
        page = LoginPage(driver)
        actual_error = page.open().fill_form(self.NONEXISTENT_LOGIN, self.PASSWORD_LESS_THAN_6_CHARS).submit().get_error_message()
        assert self.PASSWORD_MIN_LENGTH_ERROR_TEXT == actual_error

    def test_successful_login_shows_welcome_message_with_username(self,driver):
        page = LoginPage(driver)
        actual_welcome_message = page.open().fill_form(self.VALID_LOGIN, self.VALID_PASSWORD).submit().get_welcome_message()
        assert self.WELCOME_MESSAGE_TEMPLATE == actual_welcome_message

    def test_logout_button_is_displayed_after_login(self, driver):
        page = LoginPage(driver)
        page.open().fill_form(self.VALID_LOGIN, self.VALID_PASSWORD).submit()
        assert page.is_logout_button_visible()

    def test_logout_via_logout_button_returns_to_login_form(self, driver):
        page = LoginPage(driver)
        page.open().fill_form(self.VALID_LOGIN, self.VALID_PASSWORD).submit().logout()
        assert page.is_login_form_visible()
        assert self.LOGIN_FORM_TITLE_TEXT == page.get_login_form_title()


