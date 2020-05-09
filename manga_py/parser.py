from argparse import ArgumentParser

from .info import Info
from .providers import get_provider

from requests import get
from logging import warning


class Parser:
    params = None
    provider = None

    def __init__(self, args):
        self.params = {}
        self.args = args
        self._add_params(args)

    def _add_params(self, params: ArgumentParser = None):
        if params is None:
            params = self.args.parse_args()
        else:
            params = params.parse_args()
        self.params = params.__dict__

    def init_provider(
            self,
            progress: callable = None,
            log: callable = None,
            quest: callable = None,
            info: Info = None,
            quest_password: callable = None,
    ):

        real_url = self.params.get('url', '')
        provider_url = self.params.get('force_provider', None)
        provider = get_provider(provider_url or real_url)

        # update url (if redirect)
        with get(real_url, stream=True) as response:
            _url = response.url
            if self.params['url'] != _url:
                warning('Manga url changed! New url: {}'.format(_url))
                self.params['url'] = response.url

        if isinstance(provider, bool):
            raise AttributeError('Provider not found')

        self.provider = provider(info)  # provider __init__

        self.provider.quiet = self.params.get('quiet', False)

        self.provider.set_progress_callback(progress)
        self.provider.set_log_callback(log)
        self.provider.set_quest_callback(quest)
        self.provider.set_quest_password_callback(quest_password)

    def start(self):
        self.provider.process(self.params['url'], self.params)
