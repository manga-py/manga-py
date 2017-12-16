from argparse import ArgumentParser


__downloader_uri__ = 'https://github.com/yuru-yuri/Manga-Downloader'


class Parser:

    params = {}
    progress = None
    logger = None

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

    def get_provider(self):
        pass

    def set_progress_callback(self, callback: callable=None):
        self.progress = callback

    def set_logger_callback(self, callback: callable=None):
        self.logger = callback

    # def
