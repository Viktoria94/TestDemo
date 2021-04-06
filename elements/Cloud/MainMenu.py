from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from elements.BasePage import BasePage


class CloudMainMenuLocators:
    """A class for All Devices Page locators. All locators should come here."""
    PAIR_DEVICE_BTN = (By.CSS_SELECTOR, "button.cr-btn.cr-btn--variant-link")


class CloudMainMenuHelper(BasePage):

    def click_pair_device(self):
        self.find_element(CloudMainMenuLocators.PAIR_DEVICE_BTN).click()

    def validate_main_menu_is_visible(self):
        self.wait_element_is_visible(CloudMainMenuLocators.PAIR_DEVICE_BTN)

    def validate_main_menu_is_not_visible(self):
        pair_btn_is_not_visible = False
        try:
            self.wait_element_is_visible(CloudMainMenuLocators.PAIR_DEVICE_BTN)
        except TimeoutException:
            pair_btn_is_not_visible = True

        assert pair_btn_is_not_visible, "Pair button is visible"
