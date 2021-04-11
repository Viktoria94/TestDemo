import allure
import pytest

from configs.cloud import CLOUD_USERNAME, CLOUD_PASSWORD, CLOUD_URL
from configs.cloud import GMAIL, GMAIL_PASSWORD
from elements.Cloud.LoginPage import LoginPageHelper, LoginPageLocators
from elements.Cloud.MainMenu import CloudMainMenuHelper


@allure.feature('Cloud')
@allure.story('Login with mistakes')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login in the Cloud through username and password with wrong password")
def test_cloud_login_with_wrong_password(new_environment):

    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        lph = LoginPageHelper(new_environment)
        lph.login(CLOUD_USERNAME, "wrong_password")

    with allure.step("2. Validate authorization"):
        lph.wait_element_text(LoginPageLocators.WRONG_PASSWORD_MSG, "Incorrect username or password")


@allure.feature('Cloud')
@allure.story('Login with mistakes')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login in the Cloud through username and password with wrong username")
@pytest.mark.parametrize("password", [CLOUD_PASSWORD, ""])
def test_cloud_login_with_wrong_username(new_environment, password):

    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        lph = LoginPageHelper(new_environment)
        lph.login("wrong_username@cloud.cloud", CLOUD_PASSWORD)

    with allure.step("2. Validate authorization"):
        lph.wait_element_text(LoginPageLocators.WRONG_USERNAME_MSG, "User not found")


@allure.feature('Cloud')
@allure.story('Login with mistakes')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login in the Cloud through username and password: username without @")
@pytest.mark.parametrize("password", [CLOUD_PASSWORD, ""])
def test_cloud_login_with_wrong_type_username1(new_environment, password):

    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login("ItIsNotEmail", password)

    with allure.step("2. Validate authorization"):
        LoginPageHelper(new_environment).validate_login_alert(LoginPageLocators.USERNAME_INPUT,
                                                              "Please include an '@' in the email address. "
                                                              "'ItIsNotEmail' is missing an '@'.")


@allure.feature('Cloud')
@allure.story('Login with mistakes')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login in the Cloud through username and password: username without symbols after @")
@pytest.mark.parametrize("password", [CLOUD_PASSWORD, ""])
def test_cloud_login_with_wrong_type_username2(new_environment, password):
    username = "HasNoSymbolAfter@"

    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login(username, password)

    with allure.step("2. Validate authorization"):
        LoginPageHelper(new_environment).validate_login_alert(LoginPageLocators.USERNAME_INPUT,
                                                              "Please enter a part following '@'. '"
                                                              + username + "' is incomplete.")


@allure.feature('Cloud')
@allure.story('Login with mistakes')
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Login in the Cloud with empty fields")
@pytest.mark.parametrize("username,password,field", [("", CLOUD_PASSWORD, LoginPageLocators.USERNAME_INPUT),
                                                     (CLOUD_USERNAME, "", LoginPageLocators.PASSWORD_INPUT)])
def test_cloud_login_with_empty_fields(new_environment, username, password, field):
    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login(username, password)

    with allure.step("2. Validate authorization"):
        LoginPageHelper(new_environment).validate_login_alert(field, "You have empty field")


@allure.feature('Cloud')
@allure.story('Login')
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login in the Cloud through username and password")
def test_cloud_login_with_right_credentials(new_environment):

    with allure.step("1. Login in the Cloud"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login(CLOUD_USERNAME, CLOUD_PASSWORD)

    with allure.step("2. Validate authorization"):
        CloudMainMenuHelper(new_environment).validate_main_menu_is_visible()


@allure.feature('Cloud')
@allure.story('Google Login')
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Login in the Cloud with google")
def test_cloud_login_with_google(new_environment):

    with allure.step("1. Login in the Cloud with google"):
        new_environment.get(CLOUD_URL)
        LoginPageHelper(new_environment).login_with_google(GMAIL, GMAIL_PASSWORD)

    with allure.step("2. Validate authorization"):
        CloudMainMenuHelper(new_environment).validate_main_menu_is_visible()
