"""
@Project   : onepush
@Author    : y1ndan
@Blog      : https://www.yindan.me
"""

from ..core import Provider


class TeleChan(Provider):
    name = 'telechan'

    _params = {'required': ['url', 'sendkey'], 'optional': ['title', 'content']}

    def _prepare_url(self, url: str, **kwargs):
        self.url = url
        return self.url

    def _prepare_data(self, sendkey: str, title: str, content: str = None, **kwargs):
        self.data = {'sendkey': sendkey, 'text': title, 'desp': content}
        return self.data
