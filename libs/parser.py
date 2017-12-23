from argparse import ArgumentParser
from libs.providers import get_provider


__downloader_uri__ = 'https://github.com/yuru-yuri/Manga-Downloader'


class Parser:

    params = {}
    logger = None
    provider = None

    def __init__(self, args):
        self.args = args
        self._add_params(args)

    def _add_params(self, params: ArgumentParser = None):
        if params is None:
            params = self.args.parse_args()
        self.params['url'] = getattr(params, 'url', '')
        self.params['name'] = getattr(params, 'name', '')
        self.params['user_agent'] = getattr(
            params,
            'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        )

    def init_provider(self):
        self.provider = get_provider(self.params.get('url', ''))
        if not self.provider:
            raise AttributeError('Provider not found')

    def set_progress_callback(self, callback: callable=None):
        self.provider.files_progress_callback = callback

    def set_logger_callback(self, callback: callable=None):
        self.logger = callback

    def start(self):
        pass
