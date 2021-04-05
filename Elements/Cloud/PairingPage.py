from selenium.webdriver.common.by import By

from Elements.BasePage import BasePage


class PairingPageLocators:
    """A class for Pairing Page locators. All locators should come here."""
    CODE_INPUT = (By.NAME, "code")
    NAME_INPUT = (By.NAME, "name")
    PAIR_DEVICE_BTN = (By.CSS_SELECTOR, "[type='submit']")


class PairingPageHelper(BasePage):

    def pair_device(self, code, device_name):
        self.find_element(PairingPageLocators.CODE_INPUT).send_keys(code)
        self.find_element(PairingPageLocators.NAME_INPUT).send_keys(device_name)
        self.find_element(PairingPageLocators.PAIR_DEVICE_BTN).click()
