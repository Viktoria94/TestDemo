import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants import TIMEOUT


class BasePage:

    def __init__(self, driver) -> object:
        self.driver = driver

    def find_element(self, locator, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(ec.presence_of_element_located(locator),
                                                         message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located(locator),
                                                         message=f"Can't find elements by locator {locator}")

    def wait_element_text(self, locator, text, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(ec.text_to_be_present_in_element(locator, text),
                                                         message=f"Text {text} is not present in element {locator}")

    def wait_element_is_visible(self, locator, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_any_elements_located(locator),
                                                         message=f"Elements with locator {locator} is not visible")

    def wait_element_is_not_visible(self, locator, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(ec.invisibility_of_element(locator),
                                                         message=f"Elements with locator {locator} is visible")

    def send_keys_with_retry(self, locator, text, timeout=TIMEOUT):
        is_typed = False
        start_time = time.time()

        while not is_typed and ((time.time() - start_time) < timeout):
            try:
                self.find_element(locator).send_keys(text)
                is_typed = True
            except ElementNotInteractableException:
                time.sleep(1)

        assert is_typed, "Text " + text + " is not typed into element with locator " + str(
            locator) + " in timeout = " + str(
            timeout) + " secs"

    def switch_to_window_with_retry(self, window_number, timeout=TIMEOUT):
        is_switched = False
        start_time = time.time()

        while not is_switched and ((time.time() - start_time) < timeout):
            try:
                self.driver.switch_to_window(self.driver.window_handles[window_number])
                is_switched = True
            except IndexError:
                time.sleep(1)

        assert is_switched, "Window with number " + str(window_number) + " is not chosen in timeout = " + str(
            timeout) + " secs"

    def click_with_retry(self, locator, condition, timeout=TIMEOUT):
        is_clicked = False
        start_time = time.time()

        while not is_clicked and ((time.time() - start_time) < timeout):
            self.find_element(locator).click()

            if condition():
                is_clicked = True
            else:
                time.sleep(1)

        assert is_clicked, "Element with locator " + str(locator) + " is not clicked in timeout = " + str(
            timeout) + " secs"

    def accept_standard_popup(self):
        alert_obj = self.driver.switch_to.alert
        time.sleep(4)
        alert_obj.accept()
