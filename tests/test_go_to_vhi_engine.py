import pytest
from pytest_testrail.plugin import pytestrail

from conf.config import Conf


config = Conf()
vhi_username = f"project-{config.get_user()['email']}"
engine = 'Zaragoza'


@pytestrail.case('C12603', 'C12604', 'C13548')
@pytest.mark.smoke
def test_go_to_vhi_engine(cmp_app_auth):
    page1 = cmp_app_auth.page1()
    cmp_app_auth.iaas_page.breadcrumbs_h1("Infrastructure / IaaS")
    cmp_app_auth.iaas_page.go_to_vhi_engine(engine, vhi_username, page1)
    assert 'zaragoza' in cmp_app_auth.iaas_page.get_vhi_url()
