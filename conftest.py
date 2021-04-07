import allure
import pytest
import platform

from selenium import webdriver
from api.cirrus_api import frontapi2


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope='function')
def new_environment(request):
    with allure.step('Open browser Google Chrome.'):
        ext = '.exe' if platform.system() == 'Windows' else ''
        driver = webdriver.Chrome(executable_path='drivers/chromedriver{}'.format(ext))
        driver.maximize_window()

    yield driver

    if request.node.rep_call.failed:
        try:
            allure.attach(driver.get_screenshot_as_png(),
                          name='Screenshot',
                          attachment_type=allure.attachment_type.PNG)
        except:
            print('Making screenshot was failed')
            pass  # just ignore

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
