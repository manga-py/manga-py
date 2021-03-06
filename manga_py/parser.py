from logging import warning

from requests import get

from .info import Info
from .provider import Provider
from .providers import get_provider


class Parser:
    def __init__(self, args: dict):
        self.params = args

    def init_provider(
            self,
            chapter_progress: callable = None,
            global_progress: callable = None,
            log: callable = None,
            quest: callable = None,
            info: Info = None,
            quest_password: callable = None,
    ):

        original_url = self.params.get('url', '')
        provider_url = self.params.get('force_provider', None)
        provider = get_provider(provider_url or original_url)

        if isinstance(provider, bool):
            raise AttributeError('Provider not found')

        # update url (if redirect)
        self.provider = provider(info)  # type: Provider

        self.provider.original_url = original_url

        real_url = self.check_url(original_url)

        if self.provider.allow_auto_change_url():
            if real_url != original_url:
                warning('Manga url changed! New url: {}'.format(real_url))
            self.params['url'] = real_url

        self.provider.quiet = self.params.get('quiet', False)

        self.provider.set_chapter_progress_callback(chapter_progress)
        self.provider.set_global_progress_callback(global_progress)
        self.provider.set_log_callback(log)
        self.provider.set_quest_callback(quest)
        self.provider.set_quest_password_callback(quest_password)

    def start(self):
        self.provider.process(self.params['url'], self.params)

    def check_url(self, url):
        proxy = self.params.get('proxy', None)

        proxies = {
            'http': proxy,
            'https': proxy,
        } if proxy else None

        with get(url, stream=True, proxies=proxies) as response:
            _url = response.url
            if url != _url:
                url = _url
        return url

