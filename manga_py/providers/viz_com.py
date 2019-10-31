from sys import stderr
from pathlib import Path
from json import loads

from manga_py import meta
from manga_py.crypt.viz_com import solve
from manga_py.fs import get_util_home_path, path_join, is_file, unlink, file_size
from manga_py.provider import Provider
from .helpers.std import Std


class VizCom(Provider, Std):
    cookie_file = None
    __cookies = {}
    __has_auth = False
    _continue = True
    __is_debug = True

    def get_chapter_index(self) -> str:
        # return str(self.chapter_id)
        # todo: need tests
        idx = str(self.chapter_id)
        try:
            re = self.re.compile(r'-chapter-(\d+)/')
            idx = re.search(self.chapter).group(1)
        except AttributeError:
            self.log('manga-py can not get the number of the chapter!\nurl: {}'.format(self.chapter), file=stderr)
            self.log(' Please, report this error\n {}{}\n\n'.format(
                meta.__downloader_uri__, '/issues/new?template=bug_report.md'
            ), file=stderr)
        self.__is_debug and self.log('Chapter idx: {}'.format(idx))
        return idx

    def get_main_content(self):
        content = self._get_content('{}/shonenjump/chapters/{}')
        if self.__is_debug:
            page = Path('viz_debug')
            page.mkdir(parents=True, exist_ok=True)
            _path = str(page.joinpath('main-{}.html'.format(self.manga_name)))
            with open(_path, 'w') as w:
                w.write(content)
        return content

    def get_manga_name(self) -> str:
        return self._get_name('/chapters/([^/]+)')

    def get_chapters(self):
        chapters = []
        for chapter in self._elements('a.o_chapter-container[href*="/chapter/"]'):
            url = chapter.get('href')
            if url not in chapters:
                chapters.append(url)
        
        # Paid chapters are dynamically loaded so we need to take a different approach.
        re = self.re.compile(r'targetUrl:\'(.*)\',targetTitle')
        for chapter in self._elements('a.o_chapter-container[onclick*="/chapter/"]'):
            url = re.search(chapter.get('onclick')).group(1)
            if url not in chapters:
                chapters.append(url)

        self.__is_debug and self.log('Chapters count: %d' % len(chapters))

        if self.__is_debug:
            page = Path('viz_debug')
            page.mkdir(parents=True, exist_ok=True)
            _path = str(page.joinpath('chapters.html'))
            self.log('Save path to %s' % _path)
            with open(_path, 'w') as w:
                w.write('\n'.join(chapters))

        return chapters

    def get_files(self):
        self.__is_debug and self.log('Files')
        self._continue = True
        ch = self.chapter

        params = [
            'device_id=3',
            'manga_id={}'.format(self.re.search(r'/chapter/(\d+)', ch).group(1)),
            'metadata=1',
        ]
        url = 'https://www.viz.com/manga/get_manga_url?' + '&'.join(params)
        self.log(self.http_get(self.http().normalize_uri(url)))
        __url = self.http_get(self.http().normalize_uri(url)).strip()
        self._metadata = loads(self.http_get(__url))
        
        params = [
            'device_id=3',
            'manga_id={}'.format(self.re.search(r'/chapter/(\d+)', ch).group(1)),
            'page={page}',
        ]
        url = 'https://www.viz.com/manga/get_manga_url?' + '&'.join(params)
        self.__is_debug and self.log('Chapter url: %s' % url)
        if self.__has_auth:
            params.append('client_login=true')
            self.__is_debug and self.log('Logged client!')
        else:
            self.__is_debug and self.log('Anon client!')

        return [url.format(page=i) for i in range(250)]  # fixme: max 250 images per chapter

    def get_cover(self):
        self._cover_from_content('.o_hero-media')

    def prepare_cookies(self):
        self.__is_debug = self._params.get('debug', False)
        self.__is_debug = self._params
        self.http().mute = True
        self.cookie_file = path_join(get_util_home_path(), 'cookies_viz_com.dat')
        cookies = self.load_cookies()
        content = self.http().requests(self.get_url(), cookies=cookies)
        cookies.update(content.cookies.get_dict())
        self.__cookies = cookies

        if not self.has_auth():
            self.auth()
            if not self.has_auth():
                self.log('Warning! Login/password incorrect?\nTry to get free chapters...', file=stderr)
                self.log('Warning! This site worked from USA and Japan! Check your location', file=stderr)
                unlink(self.cookie_file)
                return

        self.save_cookies(self.__cookies)
        self.http().cookies = self.__cookies

    def auth(self):
        token = self.get_token()

        name = self.quest([], 'Request login on viz.com')
        password = self.quest_password('Request password on viz.com\n')

        if len(name) == 0 or len(password) == 0:
            return

        req = self.http().requests('https://www.viz.com/account/try_login', method='post', cookies=self.__cookies, data={
            'login': name,
            'pass': password,
            'rem_user': 1,
            'authenticity_token': token,
        })

        if req.status_code >= 400:
            self.log('Login/password error')
            exit(1)

        self.__cookies = req.cookies.get_dict()

        try:
            remember = self.json.loads(req.text)
            self.__cookies['remember_token'] = remember.get('trust_user_id_token_web', remember.get('remember_token', ''))
        except ValueError:
            self.__is_debug and self.log('Remember error!', file=stderr)
            self.__is_debug and self.log('Please, report this error {}{}'.format(
                meta.__downloader_uri__, '/issues/new?template=bug_report.md'
            ), file=stderr)

    def save_cookies(self, cookies: dict):
        with open(self.cookie_file, 'w') as w:
            w.write(self.json.dumps(cookies))

    def load_cookies(self):
        if is_file(self.cookie_file):
            try:
                with open(self.cookie_file, 'r') as r:
                    return self.json.loads(r.read())
            except ValueError:
                unlink(self.cookie_file)
        return {}

    def get_token(self):
        auth_token_url = 'https://www.viz.com/account/refresh_login_links'
        auth_token = self.http().get(auth_token_url, cookies=self.__cookies)
        token = self.re.search(r'AUTH_TOKEN\s*=\s*"(.+?)"', auth_token)
        return token.group(1)

    def has_auth(self):
        content = self.http_get('https://www.viz.com/account/refresh_login_links', cookies=self.__cookies)
        parser = self.document_fromstring(content)
        profile = parser.cssselect('.o_profile-link')
        success = len(profile) > 0
        self.__has_auth = success
        if success:
            # self.log('Login as {}'.format(profile[0].text))
            self.log('Login success')
        return success

    @staticmethod
    def has_chapters(parser):
        return len(parser.cssselect('.o_chapter-container')) > 0

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        if not self._continue:
            return

        self.__is_debug and self.log('\nSave file: {}'.format(idx))
        self.__is_debug and self.log('File url: {}'.format(url))

        _path, idx, _url = self._save_file_params_helper(url, idx)

        self.__is_debug and self.log('File params:\n PATH: {}\n IDX: {}\n URL: {}'.format(_path, idx, _url))

        __url = self.http_get(self.http().normalize_uri(url)).strip()

        if self.__is_debug and int(idx) < 2:
            ch = 'chapter_{}_page_{}.txt'.format(self.get_chapter_index(), idx)
            page = Path('viz_debug')
            page.mkdir(parents=True, exist_ok=True)
            __debug_path = str(page.joinpath(ch))
            self.log('Save path to %s' % __debug_path)
            with open(__debug_path, 'w') as w:
                self.log(__url)
                w.write(str(__url))
                w.close()

        if __url.find('http') != 0:
            self.__is_debug and self.log('\nURL is wrong: \n {}\n'.format(__url), file=stderr)
            return

        self.http().download_file(__url, _path, idx)

        if file_size(_path) < 32:
            self.__is_debug and self.log('File not found. Stop for this chapter')
            self._continue = False
            is_file(_path) and unlink(_path)
            return

        self.after_file_save(_path, idx)

        ref = solve(_path, self._metadata)
        if ref is not None:
            solved_path = _path + '-solved.jpeg'
            ref.save(solved_path)
            self._archive.add_file(solved_path, 'solved{}.jpeg'.format(idx))
            callable(callback) and callback()


main = VizCom
