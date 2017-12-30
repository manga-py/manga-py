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
        self.params['url'] = getattr(params, 'url', '')
        self.params['name'] = getattr(params, 'name', '')
        self.params['user_agent'] = getattr(
            params,
            'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        )

    def init_provider(self):
        provider = get_provider(self.params.get('url', ''))
        self.provider = provider()
        if not self.provider:
            raise AttributeError('Provider not found')

        self.provider.set_progress_callback(self._progress_callback)
        self.provider.set_logger_callback(self._logger_callback)
        self.provider.set_quest_callback(self._quest_callback)

    def set_progress_callback(self, callback: callable=None):
        self._progress_callback = callback

    def set_logger_callback(self, callback: callable=None):
        self._logger_callback = callback

    def set_quest_callback(self, callback: callable=None):
        self._quest_callback = callback

    def start(self):
        self.provider.process(self.params['url'], self.params)
