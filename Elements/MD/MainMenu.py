from selenium.webdriver.common.by import By
from Elements.BasePage import BasePage


class MDMainMenuLocators:
    """A class for Main Menu locators. All locators should come here."""
    CHANNELS = (By.XPATH, "//a[contains(@id,'menu_channel_')]")
    RECORDING = (By.XPATH, "//a[contains(., 'Recording')]")


class MDMainMenuHelper(BasePage):

    def find_channel_by_name(self, name):
        channels = self.find_elements(MDMainMenuLocators.CHANNELS)
        for channel in channels:
            value = channel.get_attribute("title")
            if value == name:
                return channel

    def click_channel(self, name):
        self.find_channel_by_name(name).click()

    def click_channel_recording(self):
        self.find_element(MDMainMenuLocators.RECORDING).click()


