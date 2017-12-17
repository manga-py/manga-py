import re
from libs.http import Http


class Extractor(object):

    http_params = {}

    def __init__(self):
        self.http = Http

    # mutated methods /

    def process(self):  # Main method. Required
        pass

    def quest(self, variants, title=''):  #
        pass

    # / mutated methods

    def re_match(self, pattern, string, flags=0):
        return re.match(pattern, string, flags)

    def re_search(self, pattern, string, flags=0):
        return re.search(pattern, string, flags)

    def re(self) -> re:
        return re

    def downloader(self) -> callable:
        return self.http
