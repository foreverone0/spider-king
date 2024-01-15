import re
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

    @staticmethod
    def download_file(url: str, headers: dict = {}, cookies: dict = {}) -> [str, bytes]:
        """
        下载文件,并作为内存bytes返回

        :param url:
        :param headers:
        :param cookies:
        :return:
        """

        def get_filename_from_cd(cd):
            """从 Content-Disposition 中提取文件名"""
            if not cd:
                return None
            fname = re.findall(r'filename="([^"]+)"', cd)
            if len(fname) == 0:
                # 如果没有找到，尝试提取 filename*= 后的编码文件名
                fname = re.findall(r"filename\*=UTF-8''([^']+)", cd)

            if len(fname) == 1:
                # 对提取到的文件名进行 URL 解码
                return parse.unquote(fname[0])

            return None

        response = requests.get(url, stream=True, headers=headers, cookies=cookies)
        response.raise_for_status()
        if "Content-Disposition" not in response.headers:
            raise Exception(f"下载失败,未解析到文件名")

        filename = get_filename_from_cd(response.headers.get("Content-Disposition"))
        if filename is None:
            raise Exception(f"下载失败,文件名解析失败")
        data = bytes()
        for chunk in response.iter_content(chunk_size=8192):
            data += chunk
        return filename, data
