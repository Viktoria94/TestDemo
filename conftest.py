import allure
import pytest
import platform

from selenium import webdriver
from api.cirrus_api import frontapi2


@pytest.fixture(scope='function')
def new_environment():
    with allure.step('Open browser Google Chrome.'):
        ext = '.exe' if platform.system() == 'Windows' else ''
        driver = webdriver.Chrome(executable_path='drivers/chromedriver{}'.format(ext))
        driver.maximize_window()

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
