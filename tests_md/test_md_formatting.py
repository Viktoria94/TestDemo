import allure
import pytest

from configs.device import WUI_ADMIN_URL
from configs.automation_config import JIRA_URL
from elements.MD.SDCard import SDCardPageHelper


@pytest.mark.skip
@pytest.mark.xfail
@allure.issue(JIRA_URL + "MD-11206")
@allure.feature('MD')
@allure.severity(allure.severity_level.MINOR)
@allure.title("MD-11460: Refresh page after choosing Full Format")
def test_refresh_page_after_choosing_full_format(new_environment):

    with allure.step("1. Open admin WUI on page SD card"):
        new_environment.get(WUI_ADMIN_URL + "/sdcardcfg")

    with allure.step("2. Start full card format"):
        sd_page = SDCardPageHelper(new_environment)
        sd_page.start_format("full card format")

    with allure.step("3. Check that chosen full format radio button"):
        sd_page.validate_choosing_format("full card format")

    with allure.step("4. Refresh the page"):
        new_environment.refresh()

    with allure.step("5. Check that chosen full format radio button after refreshing"):
        sd_page.validate_choosing_format("full card format")
