from selenium.webdriver.common.by import By

from Elements.BasePage import BasePage


class LoginPageLocators:
    """A class for Login Page locators. All locators should come here."""
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")


class LoginPageHelper(BasePage):

    def login(self, username, password):
        self.find_element(LoginPageLocators.USERNAME_INPUT).send_keys(username)
        self.find_element(LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.find_element(LoginPageLocators.LOGIN_BTN).click()
