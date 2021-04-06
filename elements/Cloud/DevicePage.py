from hamcrest import assert_that, equal_to
from selenium.webdriver.common.by import By

from elements.BasePage import BasePage


class DevicePageLocators:
    """A class for Device Page locators. All locators should come here."""
    DEVICE_NAME = (By.CSS_SELECTOR, ".cr-text-input__value-indicator-value > .overflow-tooltip")


class DevicePageHelper(BasePage):

    def validate_device_name(self, expected_device_name):
        real_device_name = self.find_element(DevicePageLocators.DEVICE_NAME).text
        assert_that (real_device_name, equal_to(expected_device_name), "Wrong name of the device")
