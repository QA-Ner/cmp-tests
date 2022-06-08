import logging
import allure
from playwright.sync_api import Browser
from playwright.sync_api import Request, Route, ConsoleMessage, Dialog
from pages.sign_inup_resetp import SignInUpPage
from pages.iaas import IaaS
from settings import DEFAULT_TIMEOUT
from contextlib import contextmanager


class App:
    def __init__(self, browser: Browser, base_url: str, **kwargs):
        self.browser = browser
        self.context = self.browser.new_context(**kwargs)
        self.context.set_default_timeout(DEFAULT_TIMEOUT)
        self.page = self.context.new_page()
        self.page1 = self.context.new_page()
        self.base_url = base_url
        self.sign_inup_resetp = SignInUpPage(self.page)
        self.iaas_page = IaaS(self.page, self.page1)

        def console_handler(message: ConsoleMessage):
            if message.type == 'error':
                logging.error(f'page: {self.page.url}, console error: {message.text}')

        def dialog_handler(dialog: Dialog):
            logging.warning(f'page: {self.page.url}, dialog text: {dialog.message}')
            dialog.accept()

        self.page.on('console', console_handler)
        self.page.on('dialog', dialog_handler)

    @allure.step
    def goto(self, endpoint: str, use_base_url=True):
        if use_base_url:
            self.page.goto(self.base_url + endpoint)
        else:
            self.page.goto(endpoint)

    @allure.step
    def navigate_to(self, menu: str):
        self.page.click(f"css=header >> text=\"{menu}\"") #"text=Billing History"
        self.page.wait_for_load_state()

    @allure.step
    def login(self, email: str, password: str):
        self.page.fill("input[name=\"username\"]", email)
        self.page.fill("input[name=\"password\"]", password)
        self.page.press("input[name=\"password\"]", "Enter")

    @allure.step
    def create_test(self, test_name: str, test_description: str):
        self.page.fill("input[name=\"name\"]", test_name)
        self.page.fill("textarea[name=\"description\"]", test_description)
        self.page.click("input[type=\"submit\"]")

    @allure.step
    def click_account_menu_toggler_button(self):
        self.page.click('.user-circle')

    @allure.step
    def account_menu_toggler_button_is_visible(self):
        return self.page.is_visible('.user-circle')

    @allure.step
    @contextmanager
    def intercept_requests(self, url: str, payload: str):
        def handler(route: Route, request: Request):
            route.fulfill(status=200, body=payload)

        self.page.route(url, handler)
        yield
        self.page.unroute(url)

    @allure.step
    def get_total_tests_stats(self):
        return self.page.text_content('.total >> span')

    @allure.step
    def close(self):
        self.page.close()
        self.context.close()
