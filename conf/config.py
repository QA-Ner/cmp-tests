import json
import os

conf_directory = os.path.dirname(os.path.abspath(__file__))


class Conf(object):
    def __init__(self):
        self.config = os.path.join(conf_directory, '.credentials.json')
        self.user = "userRole1"
        self.url = "cmp"
        self.generated_user_file = os.path.join(conf_directory, '.generated_user.json')

    def save_generated_user(self, work_email, full_name, passw):
        last_generated_user = {
            "work_email": work_email,
            "full_name": full_name,
            "passw": passw
            }
        with open(self.generated_user_file, "w") as write_file:
            json.dump(last_generated_user, write_file, sort_keys=True, indent=4, ensure_ascii=False)

    def get_user(self, user=None, user_data=None):
        if not user:
            user = self.user
        user_data = 'users' if not user_data else user_data
        with open(self.config, "r") as read_file:
            data = json.load(read_file)
            return data[user_data][user]

    def get_url(self, url=None):
        if not url:
            url = self.url
        with open(self.config, "r") as read_file:
            data = json.load(read_file)
            return data['project_urls'][url]
