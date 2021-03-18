import time
from json import loads
from logging import error, info
from sys import stderr

from requests import request
from requests.cookies import cookiejar_from_dict

from manga_py import meta
from manga_py.crypt.viz_com import solve
from manga_py.fs import get_util_home_path, path_join, is_file, unlink, file_size
from manga_py.provider import Provider
from .helpers.std import Std


class VizDownloader:

    def viz_downloader(self, file_name, url, method):
        with open(file_name, 'wb') as out_file:
            response = request(
                method, url, timeout=20,
                allow_redirects=True,
                headers={
                    'Referer': 'https://www.viz.com/shonenjump/',
                    'User-Agent': self.http().user_agent,
                },
                cookies=cookiejar_from_dict(self.http().cookies),
            )

            if 200 >= response.status_code < 300:
                out_file.write(response.content)
                response.close()
                out_file.close()


class VizCom(Provider, Std, VizDownloader):
    cookie_file = None
    __cookies = {}
    __has_auth = False
    _continue = True
    _metadata = None

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
                meta.repo_url, '/issues/new?template=bug_report.md'
            ), file=stderr)
        info('Chapter idx: {}'.format(idx))
        return idx

    def get_content(self):
        return self._get_content('{}/shonenjump/chapters/{}')

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

        info('Chapters count: %d' % len(chapters))

        return chapters

    def get_files(self):
        _proxies = self.http().proxies.copy()
        self.http().proxies = dict([])

        self._continue = True
        ch = self.chapter

        params = [
            'device_id=3',
            'manga_id={}'.format(self.re.search(r'/chapter/(\d+)', ch).group(1)),
            'metadata=1',
        ]
        url = '{}/manga/get_manga_url?'.format(self.domain) + '&'.join(params)
        self.log(self.http_get(self.http().normalize_uri(url)))
        __url = self.http_get(self.http().normalize_uri(url)).strip()
        self._metadata = loads(self.http_get(__url))

        params = [
            'device_id=3',
            'manga_id={}'.format(self.re.search(r'/chapter/(\d+)', ch).group(1)),
            'page={page}',
        ]
        url = '{}/manga/get_manga_url?'.format(self.domain) + '&'.join(params)
        info('Chapter url: %s' % url)
        if self.__has_auth:
            params.append('client_login=true')
            info('Logged client!')
        else:
            info('Anon client!')

        self.http().proxies = _proxies.copy()

        return [url.format(page=i) for i in range(250)]  # fixme: max 250 images per chapter

    def get_cover(self):
        self._cover_from_content('.o_hero-media')

    def prepare_cookies(self):
        self._params['max_threads'] = 2
        self.http()._download = self.viz_downloader

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

        name = self.arg('login') or self.quest([], 'Request login on viz.com')
        password = self.arg('password') or self.quest_password('Request password on viz.com\n')

        if len(name) == 0 or len(password) == 0:
            return

        req = self.http().requests(
            '{}/account/try_login'.format(self.domain),
            method='post', cookies=self.__cookies, data={
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
            self.__cookies['remember_token'] = remember.get(
                'trust_user_id_token_web',
                remember.get('remember_token', '')
            )
        except ValueError:
            error('Remember error!')
            error('Please, report this error {}{}'.format(
                meta.repo_url, '/issues/new?template=bug_report.md'
            ))

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
        auth_token_url = '{}/account/refresh_login_links'.format(self.domain)
        auth_token = self.http_get(auth_token_url, cookies=self.__cookies)
        token = self.re.search(r'AUTH_TOKEN\s*=\s*"(.+?)"', auth_token)
        return token.group(1)

    def has_auth(self):
        content = self.http_get('{}/account/refresh_login_links'.format(self.domain), cookies=self.__cookies)
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

    def before_download_file(self, idx, url):
        _path, idx, _url = super().before_download_file(idx, url)
        if not self._continue:
            return None, None, None
        info('\nSave file: {}'.format(idx))
        info('File url: {}'.format(_url))

        info('File params:\n PATH: {}\n IDX: {}\n URL: {}'.format(_path, idx, _url))

        self.http().cookies['chapter-series-5-follow-modal'] = time.strftime('%Y-%m-%d')

        __url = request(
            'get',
            self.http().normalize_uri(_url),
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.viz.com',
                'User-Agent': self.http().user_agent,
            },
            cookies=cookiejar_from_dict(self.http().cookies),
            allow_redirects=True
        ).text.strip()

        if __url.find('http') != 0:
            if self._continue:
                error('\nURL is wrong: \n {}\n'.format(__url))
            self._continue = False
            return None, None, None
        return _path, idx, __url

    def after_file_save(self, _path, idx):
        if file_size(_path) < 100:
            if self._continue:
                info('File not found. Stop for this chapter')
            self._continue = False
            is_file(_path) and unlink(_path)
            return None, None

        _path, arc_name = super().after_file_save(_path, idx)

        ref = solve(_path, self._metadata)

        self._wait_after_file()

        if ref is not None:
            solved_path = _path + '-solved.jpeg'
            ref.save(solved_path)
            return solved_path, 'solved{}.jpeg'.format(idx)
        return _path, arc_name


main = VizCom
