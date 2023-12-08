from selenium.webdriver.common.by import By


class BasePageLocators:
    ADD_BUTTON = (By.XPATH, "//button[text()='Добавить']")


class AuthLocators:
    LOGIN_INPUT = (By.XPATH, "//label[text()='Логин']/parent::*//input")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")


class OrdersListPageLocators:
    SETTINGS_BUTTON = (By.XPATH, "//button[text()='Настроить']")
    FILTER_SETTINGS_MODAL = (By.XPATH, "//div[@role='dialog']//*[text()='Настройка фильров']")
    FILTER_CHECKBOXES = (By.XPATH, "//div[@role='dialog']//input")
    FILTER_SAVE_BUTTON = (By.XPATH, "//div[@role='dialog']//button[text()='Сохранить']")
    FILTER_RESET_BUTTON = (By.XPATH, "//div[@role='dialog']//button[text()='Сбросить']")
    EXPAND_MORE = (By.XPATH, "//*[text()='Фильтры']/following-sibling::button/*[@data-testid='ExpandMoreIcon']")
    APPLY_FILTERS = (By.XPATH, "//button[text()='Применить']")
    FILTER_CUSTOMER = (By.XPATH, "//h6[text()='Покупатель']/parent::div/following-sibling::div")


class OrderPageLocators:
    OPENED_SELECT_OPTIONS = (By.TAG_NAME, "li")
    FIRST_SELECT_OPTION = (By.XPATH, "//li[1]")

    MANAGER_OPTION = (By.XPATH, "//li[text()='{}']")
    MANAGER_INPUT = (By.XPATH, "//label[text()='Менеджер']/parent::div")
    MANAGER_INPUT_NAME = (By.XPATH, "//label[text()='Менеджер']/following-sibling::div/div[@role='button']")
    MANAGER_INPUT_CLEAR = (By.XPATH, "//label[text()='Менеджер']/following-sibling::div//*[local-name() = 'svg' "
                                     "and @data-testid='CloseIcon']")

    DECORATOR_OPTION = (By.XPATH, "//li[text()='{}']")
    DECORATOR_INPUT = (By.XPATH, "//label[text()='Оформитель']/parent::div")
    DECORATOR_INPUT_NAME = (By.XPATH, "//label[text()='Оформитель']/following-sibling::div/div[@role='button']")
    DECORATOR_INPUT_CLEAR = (By.XPATH, "//label[text()='Оформитель']/following-sibling::div//*[local-name() = 'svg' "
                                       "and @data-testid='CloseIcon']")

    CITY_INPUT = (By.XPATH, "//label[text()='Город']/parent::div//input")

    USER_BLOCK = (By.XPATH, "//h6[text()='Пользователь']")
    INFO_ORDER_TAB = (By.XPATH, "//button[text()='Информация о заказе']")
