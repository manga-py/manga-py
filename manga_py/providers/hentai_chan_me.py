from shutil import copy

from manga_py.fs import is_file, storage, root_path, path_join
from .mangachan_me import MangaChanMe


class HentaiChanMe(MangaChanMe):

    def get_chapter_index(self) -> str:
        return str(self.chapter_id)

    def _login(self, **kwargs):
        url = self.domain + '/index.php'
        # login = kwargs.get('login', '')
        # password = kwargs.get('password', '')
        login = self.quest([], 'Please, input login')
        password = self.quest_password('Please, input password')
        method = kwargs.get('method', 'post')
        data = {'login_name': login, 'login_password': password, 'image': 'Вход', 'login': 'submit'}
        response = self.http().requests(method=method, data=data, url=url)
        cookies = {}
        for i in response.cookies.items():
            cookies[i[0]] = i[1]
        return cookies

    def prepare_cookies(self):
        _storage = storage('.passwords.json')
        if not is_file(_storage):
            copy(path_join(root_path(), 'manga_py', '.passwords.json.dist'), _storage)
        file = open(_storage, 'r').read()
        data = self.json.loads(file).get('hentai_chan_me', {})
        cookies = self._login(**data)
        for i in cookies:
            self._storage['cookies'][i] = cookies[i]

    def get_chapters(self):
        name = self.re.search(self._full_name_selector, self.get_url())
        url = '{}/related/{}'.format(self.domain, name.group(1))
        chapters = self.html_fromstring(url, '.related .related_info > h2 a')
        nu = self.http().normalize_uri
        return [nu(i.get('href').replace('/manga/', '/online/')) for i in chapters]

    def book_meta(self) -> dict:
        # todo meta
        pass


main = HentaiChanMe
