from manga_py.crypt import Puzzle
from manga_py.fs import get_temp_path, rename
from manga_py.provider import Provider


class TonariNoYjJp:
    provider = None
    div_num = 4
    multiply = 8
    matrix = None
    temp_path = None

    def __init__(self, provider: Provider):
        self.provider = provider
        self.temp_path = get_temp_path('__image_matrix{}.png')
        matrix = {}
        for i in range(self.div_num * self.div_num):
            matrix[i] = (i % self.div_num) * self.div_num + int(i / self.div_num)
        self.matrix = matrix

    def _chapter_api_content(self, idx) -> dict:
        api = '{}/api/viewer/readable_products?current_readable_product_id={}&' \
              'number_since=99&number_until=-1&read_more_num=100&type=episode'
        content = self.provider.http_get(api.format(self.provider.domain, idx))
        if content[0] == '{':
            return self.provider.json.loads(content)
        return {}

    def _check_need_next_chapter(self, next_url):
        if next_url:
            test = self.provider.re.search('number_since=(\d+)', next_url).group(1)
            if int(test) > 1:
                return True
        return False

    def get_chapters(self, idx) -> list:
        content = self._chapter_api_content(idx)
        items = self.provider.document_fromstring(content.get('html', '<html></html>'), '.series-episode-list-thumb')
        need_more = self._check_need_next_chapter(content.get('nextUrl', None))
        if need_more:
            items += self.get_chapters(content.get('nextUrl'))
        re = self.provider.re.compile(r'/episode-thumbnail/(\d+)')
        return [re.search(i.get('src')).group(1) for i in items]

    def solve_image(self, path, idx):
        try:
            solver = Puzzle(self.div_num, self.div_num, self.matrix, self.multiply)
            solver.need_copy_orig = True
            _ = self.temp_path.format(idx)
            solver.de_scramble(path, _)
            rename(_, path)
        except Exception:
            pass
