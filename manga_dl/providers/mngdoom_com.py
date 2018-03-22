from .funmanga_com import FunMangaCom


class MngDoomCom(FunMangaCom):
    def get_files(self):
        content = self.http_get(self.chapter)
        items = self.re.search(r' images = (\[{[^;]+}\])', content)
        if not items:
            return []
        try:
            images = self.json.loads(items.group(1))
            return [i['url'] for i in images]
        except self.json.JSONDecodeError:
            return []


main = MngDoomCom
