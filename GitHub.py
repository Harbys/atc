import requests
import bs4
import pyotp


class GitHub:
    def __init__(self, login, password, otp):
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.otp = otp
        self.logged_in = False

    def logintogh(self):
        ret = self.session.get('https://github.com/login').content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': ret.find("input", {'name': 'authenticity_token'})['value'],
            'timestamp': ret.find('input', {'name': 'timestamp'})['value'],
            'timestamp_secret': ret.find('input', {'name': 'timestamp_secret'})['value'],
            'login': self.login,
            'password': self.password
        }

        ret = self.session.post('https://github.com/session', data=data).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        if ret.find('meta', {'value': '/sessions/two-factor'}) is not None:
            otp = pyotp.TOTP(self.otp)
            data = {
                'utf8': '✓',
                'authenticity_token': ret.find("input", {'name': 'authenticity_token'})['value'],
                'otp': otp.now()
            }
            ret = self.session.post('https://github.com/sessions/two-factor', data=data)

        else:
            print('logged in')
        self.logged_in = True
        return ret

    def logout(self):
        ret = self.session.get('https://github.com/').content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'utf8': '✓',
            'authenticity_token': ret.findAll("input", {'name': 'authenticity_token'})[5]['value'],
        }
        self.session.post('https://github.com/logout', data=data)
        self.logged_in = False

    def changepassword(self, newpassword):
        if not self.logged_in:
            self.logintogh()
        ret = self.session.get('https://github.com/settings/security').content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': ret.findAll("input", {'name': 'authenticity_token'})[2]['value'],
            'session_revoked': 'false',
            'user[old_password]': self.password,
            'user[password]': newpassword,
            'user[password_confirmation]': newpassword,
            ret.find_all('input', {'class': 'form-control'})[6]: '',
            'timestamp': ret.find('input', {'name': 'timestamp'})['value'],
            'timestamp_secret': ret.find('input', {'name': 'timestamp_secret'})['value']
        }
        ret = self.session.post('https://github.com/account/password', data=data)
        if ret.status_code == 200:
            return True
        else:
            return False
