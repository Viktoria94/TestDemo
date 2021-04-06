import allure
import pytest

from configs.cloud import CLOUD_USERNAME, CLOUD_PASSWORD, CLOUD_URL
from configs.google import GMAIL, GMAIL_PASSWORD
from elements.Cloud.LoginPage import LoginPageHelper
from elements.Cloud.MainMenu import CloudMainMenuHelper


@pytest.mark.parametrize("username", [CLOUD_USERNAME, "", "wrong_username"])
@pytest.mark.parametrize("password", ["", "wrong_password"])
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login in the Cloud through username and password with wrong credentials")
def test_cloud_login_with_wrong_credentials(new_environment, username, password):
    driver_chrome = new_environment

    with allure.step("1. Login in the Cloud"):
        driver_chrome.get(CLOUD_URL)
        LoginPageHelper(driver_chrome).login(username, password)

    with allure.step("2. Validate authorization"):
        CloudMainMenuHelper(driver_chrome).validate_main_menu_is_not_visible()


@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login in the Cloud through username and password")
def test_cloud_login_with_right_credentials(new_environment):
    driver_chrome = new_environment

    with allure.step("1. Login in the Cloud"):
        driver_chrome.get(CLOUD_URL)
        LoginPageHelper(driver_chrome).login(CLOUD_USERNAME, CLOUD_PASSWORD)

    with allure.step("2. Validate authorization"):
        CloudMainMenuHelper(driver_chrome).validate_main_menu_is_visible()


@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login in the Cloud with google")
def test_cloud_login_with_google(new_environment):
    driver_chrome = new_environment

    with allure.step("1. Login in the Cloud with google"):
        driver_chrome.get(CLOUD_URL)
        LoginPageHelper(driver_chrome).login_with_google(GMAIL, GMAIL_PASSWORD)

    with allure.step("2. Validate authorization"):
        CloudMainMenuHelper(driver_chrome).validate_main_menu_is_visible()
