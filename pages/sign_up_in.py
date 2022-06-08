import allure
from playwright.sync_api import Page, expect


class SignInUpPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = ".content .form .title"
        self.email_field = "[placeholder=\"Email\"]"
        self.password_field = "[placeholder=\"Password\"]"
        self.continue_button = "text=Continue"

    @allure.step
    def check_title_exists(self, text: str):
        title = self.page.locator(self.title)
        expect(title).to_have_text(text)

    @allure.step
    def login_as(self, email: str, password: str):
        self.page.locator(self.email_field).fill(email)
        self.page.locator(self.password_field).fill(password)
        with self.page.expect_navigation():
            self.page.locator(self.continue_button).click()

    @allure.step
    def get_url(self):
        current_url = self.page.url
        return current_url
