import re
from typing import Optional, List

from bs4 import BeautifulSoup
from cachetools import cached, TTLCache

from spider_king.modules.publish.api import PublishApi, PublishPostAttachment


class PublishRepository:
    def __init__(self,
                 username: str,
                 password: str,
                 question: Optional[int] = None,
                 answer: Optional[str] = None):
        self._api = PublishApi(username, password, question, answer)

    def login(self) -> None:
        """
        登录到发布站

        :return:
        """

        html = self._api.login()

        doc = BeautifulSoup(html, 'html.parser')
        info = doc.find('span', class_='f14')
        if info is None:
            raise Exception('登录失败')

        if "您已经顺利登录" not in info.text:
            raise Exception(f'登录失败: {info.text}')

    @cached(cache=TTLCache(maxsize=1, ttl=60 * 60 * 24))
    def get_post_info(self, fid: int) -> str:
        """
        获取发帖信息

        :param fid: 板块id
        :return:
        """
        html = self._api.get_post_info(fid)

        # 正则取出verify和hexie
        verify_pattern = re.compile(r"verifyhash\s*=\s*'(\w+)';")
        verify = verify_pattern.search(html)
        if verify is None:
            raise Exception('获取verify失败')
        verify = verify.group(1)

        hexie_pattern = re.compile(r"_hexie\.value\s*=\s*'(\w+)';")
        hexie = hexie_pattern.search(html)
        if hexie is None:
            raise Exception('获取hexie失败')
        hexie = hexie.group(1)

        return verify, hexie

    def post(
            self,
            fid: int,
            title: str,
            content: str,
            category_id: Optional[int] = None,
            attachments: Optional[List[PublishPostAttachment]] = None,
    ) -> str:
        """
        发帖

        :param fid:
        :param title:
        :param content:
        :param verify:
        :param hexie:
        :param category_id:
        :param attachments:
        :return:
        """
        hexie, verify = self.get_post_info(fid)

        html = self._api.post(
            fid, title, content, verify, hexie, category_id, attachments
        )
        doc = BeautifulSoup(html, "html.parser")
        if "发帖完毕点击进入主题列表" not in html and "请等待管理员审核" not in html:
            info = doc.find("span", class_="f14")
            if info is not None:
                raise Exception(f"发帖失败: {info.text}")
            else:
                raise Exception(f'发帖失败" {html}')

        a = doc.find(
            "a",
            attrs={
                "href": re.compile(r"^read.php"),
                "class": re.compile(r"show-back fl"),
            },
        )
        if a is None:
            raise Exception("发帖失败: 未找到返回链接")
        url = a["href"]
        return url
