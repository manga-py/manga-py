from time import sleep

from manga_py.fs import get_util_home_path, path_join, is_file
from .e_hentai_org import EHentaiOrg


class exhentai_org(EHentaiOrg):
    def prepare_cookies(self):
        super().prepare_cookies()

        cookie_file = path_join(get_util_home_path(), 'cookies_exhentai.dat')
        if is_file(cookie_file):
            with open(cookie_file, 'r') as r:
                self._storage['cookies'] = self.json.loads(r.read())
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
                with open(cookie_file, 'w') as w:
                    w.write(self.json.dumps(self._storage['cookies']))

            sleep(5)


main = exhentai_org
