from typing import Optional
from urllib import parse

import requests


class DataUploader:
    url = 'https://get.datapps.org'

    @staticmethod
    def upload(data: bytes, filename: str = None):
        """
        上传数据

        :param data:
        :param filename:
        :return:
        """

        url = parse.urljoin(DataUploader.url, '/upload.php?a=1')

        files = {
            'file[]': (filename, data),
        }

        response = requests.post(url, files=files)
        response.raise_for_status()
        json = response.json()
        if json['code'] != 0:
            raise Exception(json['msg'])
        return json.get('files')[0].get('url')
