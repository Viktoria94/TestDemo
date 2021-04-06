import time
from datetime import datetime, timedelta

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from elements.BasePage import BasePage


class RecordingPageLocators:
    """A class for Recording Page locators. All locators should come here."""
    START_BTN = (By.ID, "btn_start")
    STOP_BTN = (By.ID, "btn_stop")
    RECORD_TABLE = (By.XPATH, "//*[@id='main_system']/table")
    CHANNEL_NAME = (By.ID, "channelname")
    PREFIX_INPUT = (By.ID, "user_prefix")
    RECORD_STATUS = (By.ID, "recstatus")
    FILE_TYPE_INPUT = (By.ID, "output_format")
    MP4_FRAGMENTED_OPTION = (By.CSS_SELECTOR, "[value='mp4f']")
    MP4_OPTION = (By.CSS_SELECTOR, "[value='mp4']")
    AVI_OPTION = (By.CSS_SELECTOR, "[value='avi']")
    MPEG_TS_OPTION = (By.CSS_SELECTOR, "[value='ts']")
    MOV_OPTION = (By.CSS_SELECTOR, "[value='mov']")
    FILE_TYPE_OPTION_SELECTED = (By.CSS_SELECTOR, "#output_format > [selected]")
    FILE_TYPE_OPTIONS = {"MP4-FRAGMENTED": MP4_FRAGMENTED_OPTION, "MPEG-TS": MPEG_TS_OPTION, "AVI": AVI_OPTION,
                         "MOV": MOV_OPTION, "MP4": MP4_OPTION}
    APPLY_BTN = (By.ID, "apply_rec_settings")


class RecordingPageHelper(BasePage):
    FILE_EXTENSIONS = {"MP4-FRAGMENTED": ".mp4", "MPEG-TS": ".ts", "AVI": ".avi",
                       "MOV": ".mov", "MP4": ".mp4"}
    current_file_type = ""
    last_record_name = {}

    def get_record_name(self):
        return self.last_record_name

    def get_file_type(self):
        return self.current_file_type

    def choose_file_type(self, file_type):
        self.current_file_type = file_type.upper()
        self.find_element(RecordingPageLocators.FILE_TYPE_INPUT).click()
        self.find_element(RecordingPageLocators.FILE_TYPE_OPTIONS.get(self.current_file_type)).click()

    def apply(self):
        self.find_element(RecordingPageLocators.APPLY_BTN).click()

    def start_record(self):
        # try:
        self.find_element(RecordingPageLocators.START_BTN).click()
        # except ElementClickInterceptedException:
        #     time.sleep(3)
        #     self.find_element(RecordingPageLocators.START_BTN).click()

        channel_name = self.find_element(RecordingPageLocators.CHANNEL_NAME).text
        if self.current_file_type == "":
            self.current_file_type = self.find_element(RecordingPageLocators.FILE_TYPE_OPTION_SELECTED).text
        file_extension = self.FILE_EXTENSIONS.get(self.current_file_type)

        current_date = datetime.today()

        for i in range(-5, 5):
            current_date_with_offset = current_date + timedelta(seconds=i)
            str_current_month_with_offset = current_date_with_offset.strftime("%B")
            str_current_date_with_offset = current_date_with_offset.strftime("%d_%H-%M-%S")
            self.last_record_name[i] = channel_name + "_" + str_current_month_with_offset[
                                                  0:3] + str_current_date_with_offset + file_extension

    def stop_record(self):
        self.find_element(RecordingPageLocators.STOP_BTN).click()
        self.wait_element_text(RecordingPageLocators.RECORD_STATUS, "Recorder stopped")

    def record(self, duration):
        self.start_record()
        time.sleep(duration)
        self.stop_record()

    def find_value_in_table_by_position(self, row, column):
        row = row + 1

        table_locator_way, table_locator = RecordingPageLocators.RECORD_TABLE
        value_locator = table_locator + "/tbody/tr[" + str(row) + "]/td[" + str(column) + "]/a"
        table_locator_value = (table_locator_way, value_locator)
        return self.find_element(table_locator_value)

    def validate_record_name(self, row, expected_name):
        real_name = self.find_value_in_table_by_position(row, 3).text
        assert real_name in expected_name.values(), "Wrong name of record. Real name: " + real_name
