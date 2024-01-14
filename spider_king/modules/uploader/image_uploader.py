import re
from datetime import datetime
from io import BytesIO
from typing import Optional
from urllib import parse

import requests
from PIL import Image
from cachetools import cached, TTLCache


class ImageUploader:
    """
    图床上传器
    """

    url = 'https://img.y7mn.com'

    def __init__(self):
        self.cookies = {}

    @cached(cache=TTLCache(maxsize=1, ttl=60 * 30))
    def get_auth_token(self) -> str:
        """
        获取图床的auth_token
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                      'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',

            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ('
                          'KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        }

        response = requests.get(self.url, headers=headers)
        response.raise_for_status()

        auth_token_pattern = r'<input type="hidden" name="auth_token" value="(.+?)">'
        auth_token = re.search(auth_token_pattern, response.text)
        if auth_token is None:
            raise Exception('获取auth_token失败')
        auth_token = auth_token.group(1)

        self.cookies = response.cookies.get_dict()
        return auth_token

    async def upload(self,
                     upload_type: str,
                     source: str | bytes,
                     filename: Optional[str] = None,
                     ) -> str:
        """
        上传图片

        :param upload_type: 上传类型，可选值：url、file
        :param source: 上传源，当upload_type为url时，为图片的url地址；当upload_type为file时，为图片的二进制数据
        :param filename: 上传的文件名,为空时，使用随机文件名
        :return:
        """
        url = parse.urljoin(self.url, '/json')
        auth_token = self.get_auth_token()
        timestamp = int(datetime.now().timestamp() * 1000)
        files = {

            'type': (None, upload_type),
            'action': (None, 'upload'),
            'privacy': (None, 'null'),
            'timestamp': (None, timestamp),
            'auth_token': (None, auth_token),
            'category_id': (None, 'null'),
            'nsfw': (None, 0),
            'album_id': (None, 'null')
        }

        if upload_type == 'url':
            files['source'] = (None, source)
        else:
            # 需要上传文件时,需要先把图片转换成jpg或者gif格式
            filename = filename or 'image.jpg'

            with BytesIO(source) as img_io:
                image = Image.open(img_io)

            if image.format != 'JPEG' and image.format != 'GIF':
                image = image.convert('RGB')
                filename = filename or 'image.jpg'
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG')
                source = img_byte_arr.getvalue()
                img_byte_arr.close()

            elif image.format == 'GIF':
                filename = filename or 'image.gif'

            files['source'] = (filename, source)

        response = requests.post(url,
                                 files=files,
                                 cookies=self.cookies)
        response.raise_for_status()
        json = response.json()
        if json.get('status_code') != 200:
            raise Exception(json['success']['message'])
        return json.get('image').get('url')
