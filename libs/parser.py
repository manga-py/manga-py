from argparse import ArgumentParser

from libs.providers import get_provider

__downloader_uri__ = 'https://github.com/yuru-yuri/manga-dl'


class Parser:

    params = {}
    provider = None
    _logger_callback = None
    _progress_callback = None
    _quest_callback = None

    def __init__(self, args):
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
            progress_callback: callable = None,
            logger_callback: callable = None,
            quest_callback: callable = None
    ):
        provider = get_provider(self.params.get('url', ''))
        self.provider = provider()  # provider __init__
        if not self.provider:
            raise AttributeError('Provider not found')

        self.provider.set_progress_callback(progress_callback)
        self.provider.set_logger_callback(logger_callback)
        self.provider.set_quest_callback(quest_callback)

    def start(self):
        self.provider.process(self.params['url'], self.params)
