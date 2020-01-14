import requests
import bs4


class FaceBook:
    def __init__(self, login, password):
        self.session = requests.Session()
        self.login = login
        self.password = password
        self.headers = requests.utils.default_headers()
        self.headers.update({
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.103 Safari/537.36',
        })
        self.is_logged_in = False

    def login_to_fb(self):
        ret = self.session.get('https://m.facebook.com/', headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'lsd': ret.find('input', {'name': 'lsd'})['value'],
            'jazoest': ret.find('input', {'name': 'jazoest'})['value'],
            'm_ts': ret.find('input', {'name': 'm_ts'})['value'],
            'li': ret.find('input', {'name': 'li'})['value'],
            'try_number': '0',
            'unrecognized_tries': '0',
            'email': self.login,
            'pass': self.password,
            'login': 'Zaloguj+się'
        }
        login_url = 'https://m.facebook.com' + ret.find('form', {'id': 'login_form'})['action']
        ret = self.session.post(login_url, data=data, headers=self.headers)
        if ret.status_code == 200:
            self.is_logged_in = True
            return True
        else:
            self.is_logged_in = False
            return False

    def change_password(self, new_password):
        if self.is_logged_in is False:
            self.login_to_fb()
        ret = self.session.get('https://m.facebook.com/settings/security/password/',
                               headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'jazoest': ret.find('input', {'name': 'jazoest'})['value'],
            'fb_dtsg': ret.find('input', {'name': 'fb_dtsg'})['value'],
            'password_change_session_identifier': ret.find('input', {'name': 'password_change_session_identifier'})['value'],
            'password_old': self.password,
            'password_new': new_password,
            'password_confirm': new_password
        }
        post_url = 'https://m.facebook.com' + ret.find('form', {'id': 'm-settings-form'})['action']
        ret = self.session.post(post_url, headers=self.headers, data=data)
        if ret.status_code == 200:
            self.logout()
            return True
        else:
            return False

    def logout(self):
        if self.is_logged_in is False:
            return
        ret = self.session.get('https://m.facebook.com', headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret)
        logout_url = ret.find('a', {'id': 'mbasic_logout_button'})['href']
        ret = self.session.get(f'https://m.facebook.com{logout_url}', headers=self.headers)
        if ret.status_code == 200:
            self.is_logged_in = False
            return True
        else:
            return False
