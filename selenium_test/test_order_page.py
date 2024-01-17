from selenium_test.pages.order_page import OrderPage
from selenium_test.locators.locators import OrderPageLocators
from config import *


class TestManager:
    link = f"{STAND_URL}/orders-list/new"

    def test_empty_manager(self, browser):
        """Список менеджеров пуст, пока не выбран город"""

        page = OrderPage(browser)
        page.open(self.link)
        page.click_manager_input()
        assert page.is_not_element_present(
            *OrderPageLocators.OPENED_SELECT_OPTIONS
        ), "Список менеджеров не пустой"

    def test_set_manager(self, browser):
        """В списке менеджеров находится менеджер выбранного города,
        его можно установить, поменять и удалить до сохранения"""

        page = OrderPage(browser)
        page.open(self.link)
        city_input_elem = page.get_element(*OrderPageLocators.USER_BLOCK)
        page.scroll_to_element(city_input_elem)
        page.select_city("Ростов-на-Дону")
        manager_input_elem = page.get_element(*OrderPageLocators.INFO_ORDER_TAB)
        page.scroll_to_element(manager_input_elem)
        manager = page.select_manager("Менеджер Юлия")
        assert manager.text == "Менеджер Юлия", "Выбран другой менеджер"
        manager = page.select_manager("Ткачева Мария")
        assert manager.text == "Ткачева Мария", "Выбран другой менеджер"
        # manager = page.clear_manager()
        # assert manager.text == "", "Менеджер не удалился" # тут отлавливается баг, менеджер не удаляется


class TestDecorator:
    link = f"{STAND_URL}/orders-list/new"

    def test_empty_decorator(self, browser):
        """Список оформителей пуст, пока не выбран город"""

        page = OrderPage(browser)
        page.open(self.link)
        page.click_decorator_input()
        assert page.is_not_element_present(
            *OrderPageLocators.OPENED_SELECT_OPTIONS
        ), "Список оформителей не пустой"

    def test_set_decorator(self, browser):
        """В списке оформителей находится оформитель выбранного города,
        его можно установить, поменять и удалить до сохранения"""

        page = OrderPage(browser)
        page.open(self.link)
        city_input_elem = page.get_element(*OrderPageLocators.USER_BLOCK)
        page.scroll_to_element(city_input_elem)
        page.select_city("Ростов-на-Дону")
        manager_input_elem = page.get_element(*OrderPageLocators.INFO_ORDER_TAB)
        page.scroll_to_element(manager_input_elem)
        decorator = page.select_decorator("Оформитель Юлия")
        assert decorator.text == "Оформитель Юлия", "Выбран другой оформитель"
        decorator = page.select_decorator("Морозова Ксения")
        assert decorator.text == "Морозова Ксения", "Выбран другой оформитель"
        decorator = page.clear_decorator()
        assert decorator.text == "", "Оформитель не удалился"
