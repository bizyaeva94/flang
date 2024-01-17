import pytest
from selenium import webdriver
from selenium_test.locators.locators import AuthLocators
from time import sleep
from config import *


@pytest.fixture(scope="session")
def browser():
    print("browser")
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.maximize_window()
    browser.get(STAND_URL)
    browser.find_element(*AuthLocators.LOGIN_INPUT).send_keys(ADMIN_LOGIN)
    browser.find_element(*AuthLocators.PASSWORD_INPUT).send_keys(ADMIN_PASSWORD)
    browser.find_element(*AuthLocators.LOGIN_BUTTON).click()
    sleep(3)
    yield browser
    browser.quit()
