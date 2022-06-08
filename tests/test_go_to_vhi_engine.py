import pytest
from pytest_testrail.plugin import pytestrail

from conf.config import Conf


config = Conf()
vhi_username = f"project-{config.get_user()['email']}"
engine = 'Zaragoza'


@pytestrail.case('C12603', 'C12604', 'C13548')
@pytest.mark.smoke
def test_sign_in(cmp_app_auth):
    cmp_app_auth.iaas_page.breadcrumbs_h1("Infrastructure / IaaS")
    cmp_app_auth.iaas_page.go_to_vhi_engine(engine, vhi_username)
    assert 'zaragoza' in cmp_app_auth.iaas_page.get_vhi_url()
