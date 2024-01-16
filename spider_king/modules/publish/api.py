from dataclasses import dataclass
from typing import Optional, List
from urllib import parse

import requests


@dataclass
class PublishPostAttachment:
    """
    发布站的帖子附件

    """

    name: str
    content: bytes
    desc: str = ""
    special: str = ""
    ctype: str = "money"
    needrvrc: str = "0"


class PublishApi:
    """
    发布站的api

    """

    def __init__(
        self,
        username: str,
        password: str,
        question: Optional[int] = None,
        answer: Optional[str] = None,
    ):
        """

        :param username: 账号
        :param password: 密码
        :param question: 安全问题,没有为None
        :param answer: 安全答案,如果[question]为None,则无效
        """
        self.username = username
        self.password = password
        self.question = question
        self.answer = answer
        self.cookies = None
        self.url = "https://bbs.187-o.com/"
        self.headers = {
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ("
            "KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
            "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }

    def login(self) -> str:
        """
        登录到发布站

        :return:
        """

        uri = parse.urljoin(self.url, "/2048/login.php")
        data = {
            "jumpurl": parse.urljoin(self.url, "/2048/index.php"),
            "step": 2,
            "cktime": 31536000,
            "pwuser": self.username,
            "pwpwd": self.password,
            "lgt": 0,
            "question": self.question,
            "customquest": "",
            "answer": self.answer,
        }
        response = requests.post(uri, data=data, headers=self.headers)
        response.raise_for_status()

        text = response.content.decode("utf-8")
        self.cookies = response.cookies.get_dict()
        return text

    def get_post_info(self, fid: int) -> str:
        """
        获取发帖信息

        :param fid: 板块id
        :return:
        """
        uri = parse.urljoin(self.url, f"/2048/post.php?fid={fid}")
        response = requests.get(uri, headers=self.headers, cookies=self.cookies)
        response.raise_for_status()

        text = response.content.decode("utf-8")
        return text

    def post(
        self,
        fid: int,
        title: str,
        content: str,
        verify: str,
        hexie: str,
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

        uri = parse.urljoin(self.url, "/2048/post.php?")

        forms = {
            "magicname": (None, ""),
            "magicid": (None, ""),
            "verify": (None, verify),
            "atc_usesign": (
                None,
                1,
            ),
            "atc_autourl": (
                None,
                1,
            ),
            "atc_convert": (
                None,
                1,
            ),
            "atc_newrp": (
                None,
                1,
            ),
            "topped": (
                None,
                0,
            ),
            "replayorder": (
                None,
                0,
            ),
            "atc_money": (
                None,
                0,
            ),
            "atc_credittype": (
                None,
                "money",
            ),
            "atc_rvrc": (
                None,
                "0",
            ),
            "atc_enhidetype": (
                None,
                "money",
            ),
            "atc_title": (
                None,
                title,
            ),
            "atc_iconid": (
                None,
                0,
            ),
            "atc_content": (
                None,
                content,
            ),
            "step": (
                None,
                2,
            ),
            "pid": (
                None,
                "",
            ),
            "atc_convert": (
                None,
                1,
            ),
            "action": (
                None,
                "new",
            ),
            "fid": (
                None,
                fid,
            ),
            "tid": (
                None,
                0,
            ),
            "article": (
                None,
                0,
            ),
            "special": (
                None,
                0,
            ),
            "_hexie": (None, hexie),
        }

        if category_id is not None and category_id != 0:
            forms["p_type"] = (None, category_id)
            forms["p_sub_type"] = (None, 0)

        if attachments is not None:
            for i, attachment in enumerate(attachments):
                forms[f"attachment_{i}"] = (
                    attachment.name,
                    attachment.content,
                    "application/octet-stream",
                )
                forms[f"atc_desc{i}"] = (None, attachment.desc)
                forms[f"att_special{i}"] = (None, attachment.special)
                forms[f"att_ctype{i}"] = (None, attachment.ctype)
                forms[f"atc_needrvrc{i}"] = (None, attachment.needrvrc)

        response = requests.post(
            uri, files=forms, headers=self.headers, cookies=self.cookies
        )
        response.raise_for_status()

        text = response.content.decode("utf-8")
        return text
