from selenium.webdriver.common.by import By

from Elements.BasePage import BasePage


class SDCardPageLocators:
    """A class for SD card page locators. All locators should come here."""
    QUICK_RBTN = (By.ID, "format_mode_fast")
    FULL_RBTN = (By.ID, "format_mode_full")
    FORMAT_RBTNS = {"quick card format": QUICK_RBTN, "full card format": FULL_RBTN}
    FORMAT_CARD_BTN = (By.ID, "format_button")
    CHOSEN_RBTN = (By.CSS_SELECTOR, "[checked]")


class SDCardPageHelper(BasePage):

    def start_format(self, format_type):
        self.find_element(SDCardPageLocators.FORMAT_RBTNS.get(format_type)).click()
        self.find_element(SDCardPageLocators.FORMAT_CARD_BTN).click()
        self.accept_standard_popup()

    def validate_choosing_format(self, expected_format):
        assert self.find_element(SDCardPageLocators.FORMAT_RBTNS.get(
            expected_format)).is_selected(), "Wrong chosen format! Expected: " + expected_format
