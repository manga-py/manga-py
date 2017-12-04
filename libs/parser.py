class Parser:

    params = {}

    def __init__(self):
        pass

    def add_params(self, params):
        self.params['url'] = getattr(params, 'url', '')
        self.params['name'] = getattr(params, 'name', '')
        self.params['user_agent'] = getattr(
            params,
            'user_agent',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
        )

    def get_provider(self):
        pass

    def progress(self, callback: callable = None):
        if callback:
            callback()

    def logger(self, callback: callable = None):
        if callback:
            callback()

    def
