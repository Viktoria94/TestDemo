from selenium.webdriver.common.by import By

from elements.BasePage import BasePage


class EpiphanCloudPageLocators:
    """A class for Epiphan Cloud Page locators. All locators should come here."""
    USE_CODE_TO_PAIR_LBL = (By.CLASS_NAME, "ng-binding")
    UNPAIR_BTN = (By.CLASS_NAME, "unpair_button")


class EpiphanCloudPageHelper(BasePage):

    def get_pairing_code(self):
        return self.find_element(EpiphanCloudPageLocators.USE_CODE_TO_PAIR_LBL).text.split(sep=" ", maxsplit=2)[1]

    def unpair_device(self):
        self.find_element(EpiphanCloudPageLocators.UNPAIR_BTN).click()
        self.accept_standard_popup()
