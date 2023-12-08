from .base_page import BasePage
from selenium_test.locators.locators import OrderPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class OrderPage(BasePage):
    locators = OrderPageLocators

    def click_manager_input(self):
        """Клик на инпут менеджера"""

        manager_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.MANAGER_INPUT)
        )
        manager_input.click()

    def click_decorator_input(self):
        """Клик на инпут оформителя"""

        decorator_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.DECORATOR_INPUT)
        )
        decorator_input.click()

    def select_city(self, city):
        """Выбрать город доставки"""

        city_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.CITY_INPUT)
        )
        city_input.click()
        self.browser.find_element(*self.locators.CITY_INPUT).send_keys(city)
        options = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(self.locators.FIRST_SELECT_OPTION)
        )
        options.click()

    def select_manager(self, name):
        """Выбрать менеджера"""

        manager_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.MANAGER_INPUT)
        )
        manager_input.click()
        manager_option_by, manager_option_path = self.locators.MANAGER_OPTION

        options = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(
                (manager_option_by, manager_option_path.format(name))
            )
        )
        options.click()
        return self.browser.find_element(*self.locators.MANAGER_INPUT_NAME)

    def clear_manager(self):
        """Очистить поле менеджера"""

        clear_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.MANAGER_INPUT_CLEAR)
        )
        clear_button.click()
        return self.browser.find_element(*self.locators.MANAGER_INPUT_NAME)

    def select_decorator(self, name):
        """Выбрать оформителя"""

        decorator_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.DECORATOR_INPUT)
        )
        decorator_input.click()
        decorator_option_by, decorator_option_path = self.locators.DECORATOR_OPTION

        options = WebDriverWait(self.browser, 5).until(
            EC.element_to_be_clickable(
                (decorator_option_by, decorator_option_path.format(name))
            )
        )
        options.click()
        return self.browser.find_element(*self.locators.DECORATOR_INPUT_NAME)

    def clear_decorator(self):
        """Очистить поле оформителя"""

        clear_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.locators.DECORATOR_INPUT_CLEAR)
        )
        clear_button.click()
        return self.browser.find_element(*self.locators.DECORATOR_INPUT_NAME)
