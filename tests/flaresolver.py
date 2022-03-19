import unittest
import json

from manga_py.http.flare_solver import Http


class TestFlareSolverHttp(unittest.TestCase):
    fs_addr = 'http://192.168.2.2:8191/v1'
    http = None
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'

    def setUp(self) -> None:
        self.http = Http(self.fs_addr, self.ua)
        self.http.create_session()

    def tearDown(self) -> None:
        self.http.destroy_session()

    def test_flare_solver(self):
        self.assertIsNotNone(self.http.sid)

        response = self.http.get('https://mangalib.me/jojo-no-kimyou-na-bouken-part-7-steel-ball-run-solored')

        json_content = json.loads(response.content)  # type: dict

        self.assertTrue('error' not in json_content.keys())
        self.assertTrue('status' in json_content.keys())
        self.assertTrue('solution' in json_content.keys())
        self.assertEqual(json_content['status'], 'ok')

        text_response = json_content.get('solution', {}).get('response', '')

        self.assertGreater(text_response.find('"https://mangalib.me/"'), 0)
