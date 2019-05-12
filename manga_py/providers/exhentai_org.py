from time import sleep

from manga_py.fs import get_util_home_path, path_join, is_file, unlink
from .e_hentai_org import EHentaiOrg
from sys import exit


class exhentai_org(EHentaiOrg):
    cookie_file = None

    def prepare_cookies(self):
        super().prepare_cookies()

        self.cookie_file = path_join(get_util_home_path(), 'cookies_exhentai.dat')
        if is_file(self.cookie_file):
            with open(self.cookie_file, 'r') as r:
                self._storage['cookies'] = self.json.loads(r.read())
                self.http().cookies = self._storage['cookies'].copy()
        else:
            # Login on e-hentai!
            name = self.quest([], 'Request login on e-hentai.org')
            password = self.quest_password('Request password on e-hentai.org')
            content = self.http_post('https://forums.e-hentai.org/index.php?act=Login&CODE=01', data={
                'CookieDate': 1,
                'b': 'd',
                'bt': '1-1',
                'ipb_login_submit': 'Login!',
                'UserName': name,
                'PassWord': password,
            })
            if not ~content.find('You are now logged in as:'):
                print('Wrong password?')
                sleep(.1)
                exit()
            else:
                with open(self.cookie_file, 'w') as w:
                    w.write(self.json.dumps(self._storage['cookies']))

            sleep(5)

        if not self.check_panda():
            print('Panda detected. Please, try again')
            exit(1)

    def check_panda(self):
        success = True
        req = self.http().requests('http://exhentai.org/')
        if ~req.headers['Content-Type'].find('image/'):
            """
            if authorization was not successful
            """
            print('Sad panda detected')
            print('Cookies:\n')
            print(self.http().cookies, '\n')
            self.http().cookies = {}
            unlink(self.cookie_file)
            success = False
        req.close()

        return success


main = exhentai_org
