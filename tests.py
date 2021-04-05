import allure
import pytest
from pytest_testrail.plugin import pytestrail

from Elements.Cloud.DevicePage import DevicePageHelper
from Elements.Cloud.LoginPage import LoginPageHelper
from Elements.Cloud.MainMenu import CloudMainMenuHelper
from Elements.Cloud.PairingPage import PairingPageHelper
from Elements.MD.EpiphanCloudPage import EpiphanCloudPageHelper
from Elements.MD.MainMenu import MDMainMenuHelper
from Elements.MD.RecordingPage import RecordingPageHelper
from Elements.MD.SDCard import SDCardPageHelper
from constants import WUI_ADMIN_URL, CLOUD_USERNAME, CLOUD_PASSWORD, CLOUD_URL


@pytestrail.case('C1703364')
@allure.feature('Cloud')
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Device pairing")
def test_device_pairing(new_environment):
    driver_chrome = new_environment
    device_name = "My favorite device"

    with allure.step("1. Open admin WUI on page Epiphan Cloud"):
        driver_chrome.get(WUI_ADMIN_URL + "/avstudio")

    with allure.step("2. Get pairing code"):
        pairing_code = EpiphanCloudPageHelper(driver_chrome).get_pairing_code()

    with allure.step("3. Login in the Cloud"):
        driver_chrome.get(CLOUD_URL)
        LoginPageHelper(driver_chrome).login(CLOUD_USERNAME, CLOUD_PASSWORD)

    with allure.step("4. Click button Pair device"):
        CloudMainMenuHelper(driver_chrome).click_pair_device()

    with allure.step("5. Pair device to the Cloud with name" + device_name):
        PairingPageHelper(driver_chrome).pair_device(pairing_code, device_name)

    with allure.step("6. Validate that the device has expected name"):
        DevicePageHelper(driver_chrome).validate_device_name(device_name)

    with allure.step("7. Unpair the device"):
        driver_chrome.get(WUI_ADMIN_URL + "/avstudio")
        EpiphanCloudPageHelper(driver_chrome).unpair_device()


@pytestrail.case('C1703362')
@allure.feature('MD')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Checking name of record")
@pytest.mark.parametrize("file_type", ["AVI", "MOV", "MPEG-TS", "MP4", "MP4-FRAGMENTED"])
@pytest.mark.parametrize("record_duration", [10, 20, 30])
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


@pytestrail.case('C1703363')
@allure.feature('MD')
@allure.severity(allure.severity_level.MINOR)
@allure.title("MD-11460: Refresh page after choosing Full Format")
def test_refresh_page_after_choosing_full_format(new_environment):
    driver_chrome = new_environment

    with allure.step("1. Open admin WUI on page SD card"):
        driver_chrome.get(WUI_ADMIN_URL + "/sdcardcfg")

    with allure.step("2. Start full card format"):
        sd_page = SDCardPageHelper(driver_chrome)
        sd_page.start_format("full card format")

    with allure.step("3. Check that chosen full format radio button"):
        sd_page.validate_choosing_format("full card format")

    with allure.step("4. Refresh the page"):
        driver_chrome.refresh()

    with allure.step("5. Check that chosen full format radio button after refreshing"):
        sd_page.validate_choosing_format("full card format")
