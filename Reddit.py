import requests
import bs4
import pyotp


class Reddit:
    def __init__(self, login, password, topt=None):
        self.logged_in = False
        self.session = requests.Session()
        self.login = login
        self.password = password
        self.topt = topt
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36',
        })
        if topt is None:
            self.otp = False
        else:
            self.otp = True

    def logintorediit(self):
        ret = self.session.get('https://www.reddit.com/login/', headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'csrf_token': ret.find('input', {'name': 'csrf_token'})['value'],
            'otp': '',
            'password': self.password,
            'dest': '',
            'username': self.login
        }
        if self.otp:
            token = pyotp.TOTP(self.topt)
            data['otp'] = token.now()
        ret = self.session.post('https://www.reddit.com/login', data=data, headers=self.headers)
        if ret.status_code == 200:
            self.logged_in = True
            return True
        else:
            return False

    def changepassword(self, newpassword):
        if not self.logged_in:
            self.logintorediit()
        ret = self.session.get('https://www.reddit.com/change_password/', headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'csrf_token': ret.find('input', {'name': 'csrf_token'})['value'],
            'current_password': self.password,
            'invalidate_oauth': 'false',
            'new_password': newpassword,
            'verify_password': newpassword
        }
        ret = self.session.post('https://www.reddit.com/change_password', data=data, headers=self.headers)
        if ret.status_code == 200:
            return True
        else:
            return False

    def logout(self):
        ret = self.session.post('https://www.reddit.com/logout', headers=self.headers)
        if ret.status_code == 200:
            self.logout()
            return True
        else:
            return False
