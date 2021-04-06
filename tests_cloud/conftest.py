import allure
import pytest
from selenium import webdriver

from api.cirrus_api import frontapi2


@pytest.fixture(scope='function')
def new_environment():
    with allure.step('Open browser Google Chrome.'):
        driver = webdriver.Chrome('../drivers/chromedriver')
        driver.fullscreen_window()

    yield driver

    with allure.step("Close tab"):
        driver.close()

    with allure.step("Close browser"):
        driver.quit()


@pytest.fixture(scope='function')
def delete_all_devices_from_cloud():
    yield

    with allure.step("Delete all scenes, devices and assets from the Cloud"):
        api = frontapi2.FrontAPI2("staging.epiphan.cloud")
        api.delete_all()
