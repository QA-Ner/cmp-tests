import os
import json
import pytest
import allure
from settings import *
from pytest import fixture, hookimpl
from playwright.sync_api import sync_playwright
from pages.application import App
from helpers.web_service import WebService


@fixture(scope='session')
def get_web_service(request):
    """
    Fixture returns authenticated WebService object to work with tested app directly via API web services

    :param request: pytest fixture
    https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-request

    :return: WebService object
    """
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    web = WebService(base_url)
    web.login(**config['users']['userRole1'])
    yield web
    web.close()


@fixture(scope='session')
def get_playwright():
    """
    returns single instance of playwright itself
    :return:
    """
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session', params=['chromium', 'firefox', 'webkit'])
def get_browser(get_playwright, request):
    browser = request.param
    # save browser type to env variable so fixtures and tests can get current browser
    # Needed to skip unused browser-test combinations
    os.environ['PWBROWSER'] = browser
    headless = request.config.getini('headless')
    if headless == 'True':
        headless = True
    else:
        headless = False

    if browser == 'chromium':
        bro = get_playwright.chromium.launch(headless=headless)
    elif browser == 'firefox':
        bro = get_playwright.firefox.launch(headless=headless)
    elif browser == 'webkit':
        bro = get_playwright.webkit.launch(headless=headless)
    else:
        assert False, 'unsupported browser type'

    yield bro
    bro.close()
    del os.environ['PWBROWSER']


@fixture(scope='class')
def cmp_app(get_browser, request):
    """
    Fixture of playwright for non autorised tests
    """
    base_url = request.config.getini('base_url')
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='class')
def cmp_app_auth(cmp_app, request):
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    app = cmp_app
    app.goto('/')
    app.login(**config['users']['userRole1'])
    yield app


@fixture(scope='session')
def cmp_app_admin_user(get_browser, request):
    base_url = request.config.getini('base_url')
    secure = request.config.getoption('--secure')
    config = load_config(request.session.fspath.strpath, secure)
    app = App(get_browser, base_url=base_url, **BROWSER_OPTIONS)
    app.goto('/')
    app.login(**config['users']['admin_user'])
    yield app
    app.close()


@hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    # result.when == "setup" >> "call" >> "teardown"
    setattr(item, f'result_{result.when}', result)


@fixture(scope='function', autouse=True)
def make_screenshots(request):
    yield
    if request.node.result_call.failed:
        for arg in request.node.funcargs.values():
            if isinstance(arg, App):
                allure.attach(body=arg.page.screenshot(),
                              name='screenshot.png',
                              attachment_type=allure.attachment_type.PNG)


def pytest_addoption(parser):
    parser.addoption('--secure', action='store', default='conf/.credentials.json')
    parser.addini('base_url', help='base url of site under test', default='https://staging.cmp.jelastic.team/develop/cmp/')
    parser.addini('headless', help='run browser in headless mode', default='True')


# request.session.fspath.strpath - path to project root
def load_config(project_path: str, file: str) -> dict:
    config_file = os.path.join(project_path, file)
    with open(config_file) as cfg:
        return json.loads(cfg.read())
