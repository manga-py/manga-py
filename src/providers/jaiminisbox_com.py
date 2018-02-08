from src.providers.gomanga_co import GoMangaCo


class JaiminIsBoxCom(GoMangaCo):

    def _get_json_selector(self, content):
        return 'var\\spages\\s*=\\s*(\\[.+\\])'


main = JaiminIsBoxCom
