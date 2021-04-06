import allure
import pytest

from configs.device import WUI_ADMIN_URL
from elements.MD.MainMenu import MDMainMenuHelper
from elements.MD.RecordingPage import RecordingPageHelper


@allure.feature('MD')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Checking name of record")
@pytest.mark.parametrize("file_type", ["AVI", "MOV", "MPEG-TS", "MP4", "MP4-FRAGMENTED"])
@pytest.mark.parametrize("record_duration", [10])
def test_checking_record_name(new_environment, file_type, record_duration):
    driver_chrome = new_environment

    with allure.step("1. Open admin WUI"):
        driver_chrome.get(WUI_ADMIN_URL)

    with allure.step("2. Click channel HDMI-A in Main menu"):
        main_menu = MDMainMenuHelper(driver_chrome)
        main_menu.click_channel("HDMI-A")

    with allure.step("3. Go to Recording page"):
        main_menu.click_channel_recording()

    with allure.step("4. Choose file type " + file_type):
        recording_page = RecordingPageHelper(driver_chrome)
        recording_page.choose_file_type(file_type)

    with allure.step("5. Click Apply"):
        recording_page.apply()

    with allure.step("6. Record " + str(record_duration) + " secs"):
        recording_page.record(record_duration)

    with allure.step("7. Refresh the page"):
        driver_chrome.refresh()

    with allure.step("8. Validate that the record is the first record in the record table"):
        recording_page.validate_record_name(1, recording_page.last_record_name)
