import os.path
import requests
import json
import time


class Config:
    def __init__(self):
        if not os.path.exists('config.json'):
            with open('config.json', 'w+') as f:
                if os.path.exists('.default_config.json'):
                    f.write(open('.default_config.json', 'r').read())
                    f.close()
                else:
                    f.write(requests.get('https://raw.githubusercontent.com/Harbys/atc/master/.default_config.json').
                            content.decode('utf-8'))
                    f.close()
        with open('config.json', 'r') as config:
            self.configfile = json.load(config)

    def getpath(self):
        return self.configfile["dbpath"]

    @staticmethod
    def reset_config():
        with open('config.json', 'w+') as f:
            if os.path.exists('.default_config.json'):
                f.write(open('.default_config.json', 'r').read())
                f.close()
            else:
                f.write(requests.get('https://raw.githubusercontent.com/Harbys/atc/master/.default_config.json').
                        content.decode('utf-8'))
                f.close()

    def get_active(self):
        return self.configfile['used_services']

    def get_password(self):
        if self.configfile["password"] == "require_on_start":
            return None
        else:
            return self.configfile["password"]

    def check_for_update(self, service):
        if self.configfile['used_services'][service]['last_changed'] + self.configfile['used_services'][service]['timer'] < time.time():
            return True
        else:
            return False

    def update_time(self, service):
        self.configfile['used_services'][service]['last_changed'] = time.time()
        with open('config.json', 'w') as f:
            json.dump(self.configfile, f, indent=2)
