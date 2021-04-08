import allure

from configs.cloud import CLOUD_USERNAME, CLOUD_PASSWORD, CLOUD_URL
from configs.device import WUI_ADMIN_URL
from elements.Cloud.DevicePage import DevicePageHelper
from elements.Cloud.LoginPage import LoginPageHelper
from elements.Cloud.MainMenu import CloudMainMenuHelper
from elements.Cloud.PairingPage import PairingPageHelper
from elements.MD.EpiphanCloudPage import EpiphanCloudPageHelper


@allure.feature('Cloud')
@allure.story('Test pairing')
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Device pairing")
def test_device_pairing(new_environment):
    device_name = "My favorite device"

    with allure.step("1. Open admin WUI on page Epiphan Cloud"):
        new_environment.get(WUI_ADMIN_URL + "/avstudio")

    with allure.step("2. Get pairing code"):
        pairing_code = EpiphanCloudPageHelper(new_environment).get_pairing_code()

    with allure.step("3. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login(CLOUD_USERNAME, CLOUD_PASSWORD)

    with allure.step("4. Click button Pair device"):
        CloudMainMenuHelper(new_environment).click_pair_device()

    with allure.step("5. Pair device to the Cloud with name" + device_name):
        PairingPageHelper(new_environment).pair_device(pairing_code, device_name)

    with allure.step("6. Validate that the device has expected name"):
        DevicePageHelper(new_environment).validate_device_name(device_name)

    with allure.step("7. Unpair the device"):
        new_environment.get(WUI_ADMIN_URL + "/avstudio")
        EpiphanCloudPageHelper(new_environment).unpair_device()
