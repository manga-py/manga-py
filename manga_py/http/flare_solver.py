from typing import Optional
from requests import post, Response
from . import Http as Http_
from base64 import b64decode


class Http:
    sid: str = None

    def __init__(self, solver_url: str, user_agent: str):
        self.headers = {'Content-Type': 'application/json'}
        self.solver_url = solver_url
        self.user_agent = user_agent
        self.cookies = {}

    def create_session(self, sid: str = None) -> Optional[str]:
        self.sid = post(self.solver_url, json={
            'cmd': 'sessions.create',
            'userAgent': self.user_agent,
            'session': sid,
        }).json().get('session', None)
        return self.sid

    def destroy_session(self):
        post(self.solver_url, json={
            'session': self.sid,
        })

    def get(self, url, headers: dict = None, cookies: dict = None, **kwargs) -> Response:
        cookies = [{'name': k, 'value': cookies[k]} for k in cookies] if cookies is not None else []
        return post(self.solver_url, json={
            'session': self.sid,
            'cmd': 'request.get',
            'url': url,
            'userAgent': self.user_agent,
            'headers': headers or {},
            'cookies': cookies,
            **kwargs,
        }, headers=self.headers)

    def post(self, url, headers: dict = None, data: dict = None, cookies: dict = None, **kwargs) -> Response:
        cookies = [{'name': k, 'value': cookies[k]} for k in cookies] if cookies is not None else []
        post_data = data or {}
        encoded_data = []
        for k in post_data:
            encoded_data.append(f'{k}={post_data[k]}')
        headers = headers or {}
        headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
        return post(self.solver_url, json={
            'session': self.sid,
            'cmd': 'request.post',
            'url': url,
            'userAgent': self.user_agent,
            'headers': headers,
            'postData': encoded_data,
            'cookies': cookies,
            **kwargs,
        }, headers=self.headers)

    def file(self, url, headers: dict = None, cookies: dict = None, **kwargs) -> bytes:
        response = self.get(url, headers, download=True, cookies=cookies, **kwargs)
        return b64decode(response.json().get('solution', {}).get('response'))
