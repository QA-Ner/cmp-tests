import requests
import time
from datetime import datetime

from conf.config import Conf

config = Conf()


class AcGen(object):
    """
    Inbucket - is an email testing service;
    It will accept messages for any email address and make them available via web
    https://github.com/inbucket/inbucket
    API - https://github.com/inbucket/inbucket/wiki/REST-API
    See video How to install Inbucket server: https://www.youtube.com/watch?v=9UwygnOThCM
    Our internal request to install the Inbucket server:
    https://onappdev.atlassian.net/browse/ISYSTEMS-3219
    """
    def __init__(self):
        self.inbucket_api_url = config.get_user(user_data='inbucket', user='api_url')
        self.inbucket_domain = config.get_user(user_data='inbucket', user='domain')
        self.name = 'qa-user-' + datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

        self.get_email = self.name + self.inbucket_domain

    def get_mail_box(self, name):
        name = self.name if not name else name
        box = requests.get(self.inbucket_api_url + name)
        return box.json()

    def wait_for_mail(self, name):
        # Wait for mail
        mail = None
        for _ in range(20):
            mail = self.get_mail_box(name)
            if mail:
                pass
            time.sleep(2)  # "There are no emails yet"
        return mail

    def get_message(self, name, mail_id):
        message = requests.get(self.inbucket_api_url + name + f'/{mail_id}')
        return message.text
