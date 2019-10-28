from sys import exit
from time import sleep

from manga_py.fs import get_util_home_path, path_join, is_file, unlink
from .e_hentai_org import EHentaiOrg


from lxml.html import HtmlElement


class ExHentaiOrg(EHentaiOrg):
    __uri = 'https://forums.e-hentai.org/index.php?act=Login&CODE={}'
    cookie_file = None

    def prepare_cookies(self):
        super().prepare_cookies()

        self.cookie_file = path_join(get_util_home_path(), 'cookies_exhentai.dat')
        if is_file(self.cookie_file):
            with open(self.cookie_file, 'r') as r:
                self._storage['cookies'] = self.json.loads(r.read())
                self.http().cookies = self._storage['cookies'].copy()
        else:
            action, method, form_data = self.prepare_form()
            content = self.http().requests(action, data=form_data, method=method.lower())
            if not ~content.text.find('You are now logged in as:'):
                self.log('Wrong password?')
                sleep(.1)
                exit()
            else:
                with open(self.cookie_file, 'w') as w:
                    w.write(self.json.dumps(self._storage['cookies']))

            sleep(5)

        if not self.check_panda():
            self.log('Panda detected. Please, try again')
            exit(1)

    def prepare_form(self):
        # Login on e-hentai!
        name = self.quest([], 'Request login on e-hentai.org')
        password = self.quest_password('Request password on e-hentai.org\n')

        selectors = [
            'input[type="hidden"]',
            'input[checked]',
            'input[type="submit"]',
        ]

        form_data = {
            'UserName': name,
            'PassWord': password,
        }
        prepare = self.http_get(self.__uri.format('00'))
        parser = self.document_fromstring(prepare, 'form[name="LOGIN"]')[0]  # type: HtmlElement
        action = parser.get('action', self.__uri.format('01'))
        method = parser.get('method', 'get')
        for i in parser.cssselect(','.join(selectors)):  # type: HtmlElement
            form_data[i.get('name')] = i.get('value')

        return action, method, form_data

    def check_panda(self):
        success = True
        req = self.http().requests('https://exhentai.org/', method='head')
        if ~req.headers['Content-Type'].find('image/'):
            """
            if authorization was not successful
            """
            self.log('Sad panda detected')
            # self.log('Cookies:\n')
            # self.log(self.http().cookies, '\n')
            self.http().cookies = {}
            unlink(self.cookie_file)
            success = False
        req.close()

        return success


main = ExHentaiOrg
