from manga_py.provider import Provider
from .helpers.std import Std


class FireCrossJp(Provider, Std):
    def get_chapter_index(self) -> str:
        pass

    def get_archive_name(self) -> str:
        pass

    def get_content(self):
        self.http_get(self.get_url())

    def get_manga_name(self) -> str:
        return self.text_content(self.content, '.ebook-series-title')

    def get_chapters(self) -> list:
        elements = self._elements(
            'li.shop-item--episode'
        )
        return [(
            x.get('data-id'),
            x.cssselect('.shop-item-info-name')[0].text.strip,
        ) for x in elements][::-1]

    def get_files(self) -> list:
        # scramble
        """
        <Scramble>0,9,3,12,8,6,13,1,11,2,15,5,14,4,7,10</Scramble>
        curl
         'https://firecross.jp/celsys/diazepam_hybrid.php?mode=8&file=0000.xml&reqtype=0&vm=4&param=1T6XoHEliHqVjZKvm%2FobiMljUv7qhn0Dv%2FVWs8eky6CduoTZYSjUWMmaxE4Kcf2GxFWkkyiFaDvRS3r6Mnd6U3%2Bh1d5IzmxcKX2rGPsU%2F2BuZyQfoazlp%2BUWX09AbIb6eo8RqoPSv7am128jP%2Bd0jg%3D%3D&time=379934'
         -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
         -H 'Accept: */*' -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
         -H 'Accept-Encoding: gzip, deflate, br'
         -H 'Referer: https://firecross.jp/reader/3349?trial=0&token=0be2513c-8cc7-434d-8afd-e9bc389cfa9e'
         -H 'DNT: 1'
         -H 'Connection: keep-alive'
         -H 'Cookie: XSRF-TOKEN=%3D; _s=%3D'
         -H 'Sec-Fetch-Dest: empty'
         -H 'Sec-Fetch-Mode: cors'
         -H 'Sec-Fetch-Site: same-origin'
         -H 'Sec-GPC: 1'
         -H 'TE: trailers'
        :return:
        """

        # total pages
        """
        <TotalPage>26</TotalPage>
        https://firecross.jp/celsys/diazepam_hybrid.php?mode=7&file=face.xml&reqtype=0&vm=4&param=1T6XoHEliHqVjZKvm%2FobiMljUv7qhn0Dv%2FVWs8eky6CduoTZYSjUWMmaxE4Kcf2GxFWkkyiFaDvRS3r6Mnd6U3%2Bh1d5IzmxcKX2rGPsU%2F2BuZyQfoazlp%2BUWX09AbIb6eo8RqoPSv7am128jP%2Bd0jg%3D%3D&time=379934
        """

        # image
        """
        https://firecross.jp/celsys/diazepam_hybrid.php?mode=1&file=0001_0000.bin&reqtype=0&vm=4&param=1T6XoHEliHqVjZKvm%2FobiMljUv7qhn0Dv%2FVWs8eky6CduoTZYSjUWMmaxE4Kcf2GxFWkkyiFaDvRS3r6Mnd6U3%2Bh1d5IzmxcKX2rGPsU%2F2BuZyQfoazlp%2BUWX09AbIb6eo8RqoPSv7am128jP%2Bd0jg%3D%3D&time=379934
        """

        content_html = self.http_get(self.chapter[0])

        reader = self.document_fromstring(content_html, '#meta', 0)

        cgi_value = reader.cssselect('input[name="cgi"]')
        param_value = reader.cssselect('input[name="param"]')

        mode_value = 8
        file_value = '%04d.xml'
        reqtype_value = '0'
        vm_value = 4
        time_value = '6889374'  # ?

        return []

    def _get_chapter_url(self):
        """
        curl 'https://firecross.jp/api/reader'
            -X POST
            -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
            -H 'Accept: application/json'
            -H 'Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
            -H 'Accept-Encoding: gzip, deflate, br'
            -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8'
            -H 'X-Requested-With: XMLHttpRequest'
            -H 'Origin: https://firecross.jp'
            -H 'DNT: 1'
            -H 'Connection: keep-alive'
            -H 'Referer: https://firecross.jp/ebook/series/440'
            -H 'Cookie: XSRF-TOKEN=%3D; _s=%3D'
            -H 'Sec-Fetch-Dest: empty'
            -H 'Sec-Fetch-Mode: cors'
            -H 'Sec-Fetch-Site: same-origin'
            -H 'Sec-GPC: 1'
            --data-raw '_token=MQbdBgUC1bo3CQDL3g3iJ5sPGrxjjgJ0NGlRwXH3&ebook_id=3349'
        :return:
        """

        url = self.http().post(
            url=f'{self.domain}/api/reader',
            headers={
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
        )

        return url.json()['redirect']


main = FireCrossJp
