import sys
import time

from manga_py.provider import Provider
from .helpers.std import Std

_graphql_where = "{deleted: false, published: $isAdmin, manga: {slug: $slug, published: $isAdmin, deleted: false}}"

_grapgql_query = """query chapters($slug: String, $limit: Float, $skip: Float, $order: Float!, $isAdmin: Boolean!) {
  chapters(limit: $limit, skip: $skip, where: %s, order: [{field: "number", order: $order}]) {
    published
    likes
    id
    number
    manga {
      name
      slug
    }
    __typename
  }
}""" % (_graphql_where, )


def _graphql(slug: str, skip: int = 12, is_admin: bool = True) -> dict:
    variables = {"slug": slug, "order": -1, "skip": skip, "limit": 12, "isAdmin": is_admin}
    return {"operationName": "chapters", "variables": variables, "query": _grapgql_query}


class LittleXGardenCom(Provider, Std):
    _name_selector = r'\.\w{2,5}/([^/]+)'
    _images_webroot = 'https://littlexgarden.com/static/images/'
    _api_url = "https://littlexgarden.com/graphql"

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.\w{2,5}/[^/]+/(\d+)', self.chapter).group(1)

    def get_content(self):
        return self._get_content('{}/{}')

    def get_manga_name(self) -> str:
        return self._get_name(self._name_selector)

    def get_chapters(self):
        slug = self._get_name(self._name_selector)
        chapter_offset = 0
        errors_count = 0
        latest_error = None
        chapters = []

        self.log("Please wait...")

        while True:
            if errors_count > 3:
                print(latest_error, file=sys.stderr)
                raise RuntimeError("Too many network errors for chapters")
            chapters_response = self.http().post(self._api_url, headers={
                "Content-Type": "application/json",
            }, json=_graphql(slug, chapter_offset))

            latest_error_code = chapters_response.status_code
            if latest_error_code != 200:
                errors_count += 1
                latest_error = chapters_response.text
                print(f"Bad code: {latest_error_code}", file=sys.stderr)
                time.sleep(3)
                continue

            errors_count = 0

            chapters_ = chapters_response.json().get("data", {}).get("chapters", [])  # type: list

            _len = len(chapters_)

            for ch in chapters_:
                if ch["published"]:
                    chapters.append("{}/{}/{}".format(
                        self.domain, ch["manga"]["slug"], ch["number"]
                    ))

            if _len < 12:
                break

            chapter_offset += _len

        return chapters

    def get_files(self):
        content = self.http_get(self.chapter)
        script_content = None

        scripts = self.document_fromstring(content, 'script')

        nuxt_re = self.re.compile(r'__NUXT__\s?=')
        image_re = self.re.compile(r'"([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.jpg)"')

        for script in scripts:
            source = self.element_text_content_full(script)
            if nuxt_re.search(source):
                script_content = source
                break

        if script_content is None:
            self.log('Images not found')
            return []

        return list(map(self._image_url, image_re.findall(script_content)))

    def _image_url(self, image_id: str):
        if self.http().allow_webp:
            return f'{self._images_webroot}webp/{image_id}.webp'
        return f'{self._images_webroot}{image_id}'


main = LittleXGardenCom
