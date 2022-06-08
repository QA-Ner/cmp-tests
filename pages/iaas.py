import allure
from playwright.sync_api import Page, expect


class IaaS:
    def __init__(self, page: Page, page1: Page):
        self.page = page
        self.page1 = page1
        self.engines_page_breadcrumbs = "[data-testid=\"engines-page-breadcrumbs-h1\"]"
        self.vhi_user_name = ".el-header__actions > .el-dropdown > button[role='button'] .el-button__text"

    @allure.step
    def breadcrumbs_h1(self, text: str):
        expect(self.page.locator(self.engines_page_breadcrumbs)).to_have_text(text)

    @allure.step
    def go_to_vhi_engine(self, engine: str, vhi_username: str):
        with self.page.expect_popup() as popup_info:
            self.page.locator(f"text={engine}").click()
        self.page1 = popup_info.value
        with self.page1.expect_navigation():
            self.page1.locator("button:has-text(\"Sign in with CMP\")").click()
        expect(self.page1.locator(self.vhi_user_name)
               ).to_have_text(vhi_username)

    @allure.step
    def get_vhi_url(self):
        current_url = self.page1.url
        return current_url
