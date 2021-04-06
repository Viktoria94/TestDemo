This is a repository for Epiphan Cloud and MD tests

**How to run it**

Install requirements with command:

    pip3 install requirements.txt

Set your configuration data in dir ./configs

Run MD tests without allure report:

    pytest tests_md/*

Run MD tests with allure report:

    pytest tests_md/* --alluredir=/allure_res

Run Cloud tests without allure report:

    pytest tests_cloud/*

Run Cloud tests with allure report:

    pytest tests_cloud/* --alluredir=/allure_res

To generate allure report:

    allure serve allure_res

    