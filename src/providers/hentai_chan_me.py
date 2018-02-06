from src.providers.mangachan_me import MangaChanMe
from src.fs import get_current_path, path_join, is_file


class HentaiChanMe(MangaChanMe):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index()
        return 'vol_{:0>3}'.format(idx)

    def get_chapter_index(self) -> str:
        return str(self._chapter_index())

    def _login(self, **kwargs):
        url = self.get_domain() + '/index.php'
        login = kwargs.get('login', '')
        password = kwargs.get('password', '')
        method = kwargs.get('method', 'post')
        data = {'login_name': login, 'login_password': password, 'image': 'Вход', 'login': 'submit'}
        response = self.http()._requests(method=method, data=data, url=url)
        cookies = {}
        for i in response.cookies.items():
            cookies[i[0]] = i[1]
        return cookies

    def prepare_cookies(self):
        storage = path_join(get_current_path(), 'storage', '.passwords.json')
        if not is_file(storage):
            return
        file = open(storage, 'r').read()
        data = self.json.loads(file).get('hentai_chan_me', {})
        cookies = self._login(**data)
        for i in cookies:
            self._storage['cookies'][i] = cookies[i]

    def get_chapters(self):
        name = self.re.search(self._full_name_selector, self.get_url())
        url = '{}/related/{}'.format(self.get_domain(), name.group(1))
        chapters = self.html_fromstring(url, '.related .related_info > h2 a')
        nu = self.http().normalize_uri
        return [nu(i.get('href').replace('/manga/', '/online/')) for i in chapters]


main = HentaiChanMe
