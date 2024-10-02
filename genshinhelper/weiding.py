"""
@Project   : genshinhelper
@Author    : y1ndan
@Blog      : https://www.yindan.me
@GitHub    : https://github.com/y1ndan
@Modified  : 2022-08-23
"""

# import random
# import time

from .core import Client, get_headers
from .utils import request, log, nested_lookup, extract_subset_of_dict, _


# 未定事件簿
class Weiding(Client):
    def __init__(self, cookie: str = None):
        super().__init__(cookie)
        # constants
        self.act_id = 'e202202251749321'
        self.game_biz = 'nxx_cn'
        self.required_keys.update({
            'total_sign_day', 'today', 'is_sign'
        })

        self.sign_info_url = f'{self.api}/event/luna/info?lang=zh-cn&act_id={self.act_id}' + '&uid={}&region={}'
        self.rewards_info_url = f'{self.api}/event/luna/home?lang=zh-cn&act_id={self.act_id}'
        self.sign_url = f'{self.api}/event/luna/sign'

    @property
    def sign_info(self):
        if not self._sign_info:
            roles_info = self.roles_info
            self._sign_info = [
                self.get_sign_info(i['game_uid'], i['region'])
                for i in roles_info
            ]
        return self._sign_info

    def get_sign_info(self, uid: str, region: str):
        log.info(_('Preparing to get check-in information ...'))
        url = self.sign_info_url.format(uid, region)
        response = request('get', url, headers=self.headers, cookies=self.cookie).json()
        data = nested_lookup(response, 'data', fetch_first=True)
        return extract_subset_of_dict(data, self.required_keys)

    def sign(self):
        user_data = self.user_data
        log.info(_('Preparing to claim daily reward ...'))
        result = []
        for i in range(len(user_data)):
            user_data[i]['status'] = _('👀 You have already checked-in')
            user_data[i]['addons'] = 'From NXX'
            user_data[i]['sign_response'] = None
            user_data[i]['end'] = ''
            total_sign_day = user_data[i]['total_sign_day']
            is_sign = user_data[i]['is_sign']

            if not is_sign:
                payload = {
                    'act_id': self.act_id,
                    'region': user_data[i]['region'],
                    'uid': user_data[i]['game_uid'],
                    'lang': 'zh-cn'
                }
                response = request(
                    'post',
                    self.sign_url,
                    headers=get_headers(with_ds=True),
                    json=payload, cookies=self.cookie).json()

                user_data[i]['status'] = response.get('message', -1)
                user_data[i]['sign_response'] = response
                retcode = response.get('retcode', -1)
                # 0:      success
                # -5003:  already checked in
                if retcode == 0:
                    user_data[i]['total_sign_day'] = total_sign_day + 1
                    user_data[i]['is_sign'] = True
            result.append(user_data[i])

        self._user_data = result
        return result
