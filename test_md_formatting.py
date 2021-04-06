import allure
import pytest

from data.device import WUI_ADMIN_URL
from elements.MD.SDCard import SDCardPageHelper


@pytest.mark.skip
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
