import time

from selenium.webdriver.common.by import By

from configs.automation_config import TIMEOUT
from elements.BasePage import BasePage


class LoginPageLocators:
    """A class for Login Page locators. All locators should come here."""
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_WITH_GOOGLE_BTN = (By.CLASS_NAME, "sign-in-button--google")
    GOOGLE_MAIL_INPUT = (By.ID, "identifierId")
    GOOGLE_MAIL_PASSWORD = (By.ID, "password")
    GOOGLE_MAIL_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    GOOGLE_MAIL_NEXT_BTN = (By.CSS_SELECTOR, "#identifierNext [type='button']")
    GOOGLE_MAIL_PASSWORD_NEXT_BTN = (By.CSS_SELECTOR, "#passwordNext [type='button']")
    WRONG_PASSWORD_MSG = (By.CLASS_NAME, "gla-form__error")
    WRONG_USERNAME_MSG = (By.CLASS_NAME, "form-helper-text--error")
    INVALID_INPUT = (By.CSS_SELECTOR, "input:invalid[required][name='*']")


class LoginPageHelper(BasePage):

    def login(self, username, password):
        self.find_element(LoginPageLocators.USERNAME_INPUT).send_keys(username)
        self.find_element(LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.find_element(LoginPageLocators.LOGIN_BTN).click()

    def login_with_google(self, gmail, password):
        start_time = time.time()
        while not (len(self.driver.window_handles) == 2) and ((time.time() - start_time) < TIMEOUT):
            self.find_element(LoginPageLocators.LOGIN_WITH_GOOGLE_BTN).click()
            time.sleep(1)
        self.driver.switch_to_window(self.driver.window_handles[1])

        self.find_element(LoginPageLocators.GOOGLE_MAIL_INPUT).send_keys(gmail)
        self.find_element(LoginPageLocators.GOOGLE_MAIL_NEXT_BTN).click()
        self.send_keys_with_retry(LoginPageLocators.GOOGLE_MAIL_PASSWORD_INPUT, password)
        self.find_element(LoginPageLocators.GOOGLE_MAIL_PASSWORD_NEXT_BTN).click()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def validate_login_alert(self, element, text) -> object:
        validation_message = self.find_element(element).get_property(
            "validationMessage")

        way_invalid_element, locator_invalid_element = LoginPageLocators.INVALID_INPUT
        way_element, locator_element = element

        locator_invalid_element = locator_invalid_element.replace("*", locator_element)

        self.find_element((way_invalid_element, locator_invalid_element))

        assert validation_message == text, "Real: " + validation_message + \
                                           "expected: " + text
