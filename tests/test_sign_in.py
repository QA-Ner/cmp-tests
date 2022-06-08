import pytest
from pytest_testrail.plugin import pytestrail

from conf.config import Conf


config = Conf()
email = config.get_user()['email']
password = config.get_user()['password']


@pytestrail.case('C12479')
@pytest.mark.smoke
def test_sign_in(cmp_app):
    cmp_app.sign_in_up.check_title_exists("Sign In")
    cmp_app.sign_in_up.login_as(email, password)
    cmp_app.iaas_page.breadcrumbs_h1("Infrastructure / IaaS")
    assert 'engines' in cmp_app.sign_in_up.current_url()

