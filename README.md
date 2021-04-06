This is a repository for Epiphan Cloud and MD tests

**How to run it**

Install requirements with command:

    pip3 install -r requirements.txt

Set your configuration data in dir ./configs

Run MD tests without allure report:

    pytest tests_md/

Run MD tests with allure report:

    pytest tests_md/ --alluredir=./allure_res

Run Cloud tests without allure report:

    pytest tests_cloud/

Run Cloud tests with allure report:

    pytest tests_cloud/ --alluredir=./allure_res

To generate allure report:

    allure serve ./allure_res

**How to install Allure**

**Mac OS X**
For Mas OS, automated installation is available via Homebrew

    brew install allure

**Windows**
For Windows, Allure is available from the Scoop commandline-installer.

To install Allure, download and install Scoop and then execute in the Powershell:

    scoop install allure
Also Scoop is capable of updating Allure distribution installations. To do so navigate to the Scoop installation directory and execute

    \bin\checkver.ps1 allure -u
This will check for newer versions of Allure, and update the manifest file. Then execute

    scoop update allure

    