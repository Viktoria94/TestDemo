import time

from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver) -> object:
        self.driver = driver

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(ec.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def wait_element_text(self, locator, text, time=10):
        return WebDriverWait(self.driver, time).until(ec.text_to_be_present_in_element(locator, text),
                                                      message=f"Text {text} is not present in element {locator}")

    def accept_standard_popup(self):
        alert_obj = self.driver.switch_to.alert
        time.sleep(4)
        alert_obj.accept()
