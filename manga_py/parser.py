from argparse import ArgumentParser

from .providers import get_provider
from .info import Info


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
        provider = get_provider(self.params.get('url', ''))
        if isinstance(provider, bool):
            raise AttributeError('Provider not found')
        self.provider = provider(info)  # provider __init__

        self.provider.set_progress_callback(progress)
        self.provider.set_log_callback(log)
        self.provider.set_quest_callback(quest)
        self.provider.set_quest_password_callback(quest_password)

    def start(self):
        self.provider.process(self.params['url'], self.params)
