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

    def logintofb(self):
        ret = self.session.get('https://www.facebook.com/', headers=self.headers).content.decode('utf-8')
        ret = bs4.BeautifulSoup(ret, 'html.parser')
        data = {
            'jazoest': ret.find('input', {'name': 'jazoest'})['value'],
            'lsd': ret.find('input', {'name': 'lsd'})['value'],
            'email': self.login,
            'pass': self.password,
            'login_source': 'comet_headerless_login',
            'login': '1'
        }
        ret = self.session.post('https://www.facebook.com/login/', data=data, headers=self.headers)
        return ret
